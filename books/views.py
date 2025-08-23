from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseServerError
from django.contrib import messages
from django.db.models import Count
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from users.decorators import login_required_session
from products.tasks import slow_add
from .models import Book, Author


def update_author_cache(author):
    """
    Cập nhật Redis cache cho chi tiết tác giả và danh sách tác giả có sách.
    """
    # Cập nhật cache detail_author
    cache.set(
        f'detail_author_{author.id}',
        {
            'id': author.id,
            'name': author.name,
            'age': author.age,
            'created_at': author.created_at,
        },
        timeout=60
    )
    print("Cập nhật cache detail_author")

    # Cập nhật cache authors_has_books nếu có
    authors_has_books = cache.get('authors_has_books')
    if authors_has_books:
        for index, a in enumerate(authors_has_books):
            if a.id == author.id:
                a.name = author.name
                a.age = author.age
                authors_has_books[index] = a
                break
        cache.set('authors_has_books', authors_has_books, timeout=60)
        print("Cập nhật cache authors_has_books")


@login_required_session
def book_list(request):
    """
    Hiển thị danh sách tác giả và sách kèm phân trang.
    - Tối ưu query bằng cách phân trang ở mức Database.
    - Cache tổng số sách và cache từng trang của danh sách tác giả.
    """

    total_book = cache.get('total_book_author_has_book')
    if total_book is None:
        total_book = Book.objects.aggregate(total=Count('id'))['total']
        cache.set('total_book_author_has_book', total_book, timeout=60)
        print("📦 Lấy tổng số sách từ DB")

    # 2. Tạo QuerySet phân trang ở DB (không load hết vào Python)
    authors_qs = Author.objects.has_books().prefetch_related('books').order_by('-book_count')

    # 3. Lấy số trang hiện tại từ query string (?page=2)
    page_number = request.GET.get("page", 1)

    # 4. Tạo đối tượng Paginator (5 tác giả/trang)
    paginator = Paginator(authors_qs, 5)

    # 5. Cache từng trang (key: authors_page_1, authors_page_2, ...)
    cache_key = f"authors_page_{page_number}"
    page_obj = cache.get(cache_key)

    if page_obj is None:
        try:
            page_obj = paginator.get_page(page_number)  
            # Django tự xử lý số trang không hợp lệ
        except (EmptyPage, PageNotAnInteger):
            # Nếu số trang không tồn tại hoặc không phải số → load trang 1
            page_obj = paginator.page(1)
        cache.set(cache_key, page_obj, timeout=60)
        print(f"📦 Lấy authors từ DB cho trang {page_number}")
    else:
        print(f"⚡ Lấy authors từ cache cho trang {page_number}")

    # 6. Ví dụ chạy task Celery (async)
    # print("📨 Task Celery:", slow_add.delay(3, 4))

    return render(request, 'books/home.html', {
        "page_obj": page_obj,
        'total_book': total_book
    })


@login_required_session
def details_author(request, id):
    try:
        cache_key = f'detail_author_{id}'
        author_data = cache.get(cache_key)

        if author_data is None:
            author = get_object_or_404(Author, id=id)
            author_data = {
                'id': author.id,
                'name': author.name,
                'age': author.age,
                'created_at': author.created_at,
            }
            cache.set(cache_key, author_data, timeout=60)
            print(f"Lấy author từ DB: {author_data['name']}")
        else:
            print(f"⚡ Lấy author từ Redis: {author_data['name']}")

        # print("detail = ",slow_add.delay(1,1))

        return render(request, 'books/details_author.html', {
            'author': author_data
        })

    except Exception as e:
        print(f"Lỗi: {e}")
        return HttpResponseServerError("Lỗi máy chủ nội bộ.")


@login_required_session
def update_author(request, id):
    author = get_object_or_404(Author, id=id)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        age = request.POST.get('age', '').strip()

        if not name or not age.isdigit():
            messages.error(request, "Vui lòng nhập đầy đủ và chính xác.")
            return render(request, 'books/update_author.html', {'author': author})

        try:
            author.name = name
            author.age = int(age)
            author.full_clean()
            author.save()
            messages.success(request, "Cập nhật thành công.")

            update_author_cache(author)

            return redirect('books:details-author', id)

        except ValidationError as e:
            messages.error(request, f"Lỗi: {e}")
        except Exception as e:
            messages.error(request, f"Đã xảy ra lỗi: {e}")

    return render(request, 'books/update_author.html', {
        'author': author
    })
