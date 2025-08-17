from django.db import models

"""
📘 LÝ THUYẾT: Custom QuerySet và Manager trong Django
✅ 1. Custom QuerySet
QuerySet là đối tượng đại diện cho tập hợp các bản ghi trong database.

Django cho phép tạo các lớp con của models.QuerySet để thêm các phương thức lọc dữ liệu tùy chỉnh (custom filters).

Việc sử dụng custom QuerySet giúp tái sử dụng logic lọc/phân tích dữ liệu thay vì viết lại cùng một truy vấn ở nhiều nơi.

✅ 2. Custom Manager
Manager là cổng truy cập mặc định để thao tác với database trong Django model (thường gọi là Model.objects).

Ta có thể định nghĩa custom Manager để dùng các phương thức đặc biệt hoặc kết hợp với Custom QuerySet để mở rộng chức năng của .objects.

✅ 3. Kết hợp QuerySet + Manager
models.Manager.from_queryset(QuerySetClass) là cách chuẩn để gộp custom QuerySet vào Manager.

Khi đó ta có thể gọi trực tiếp Author.objects.adults(), Author.objects.age_between() thay vì phải chain thủ công.
"""

class AuthorQuerySet(models.QuerySet):
    def adults(self, age=18):
        # Trả về các tác giả có tuổi >= age (mặc định là 18)
        return self.filter(age__gte=age)
    
    def age_between(self, min_age, max_age):
        # Trả về các tác giả có tuổi nằm trong khoảng min_age đến max_age
        return self.filter(age__gte=min_age, age__lte=max_age)
    
    def name_contains(self, name):
        # Trả về các tác giả có tên chứa chuỗi name (không phân biệt hoa thường)
        return self.filter(name__icontains=name)

    def has_books(self):
        # Trả về các tác giả có ít nhất một cuốn sách
        return self.annotate(book_count=models.Count('books')).filter(book_count__gt=0)

# ✅ Custom Manager kết hợp với Custom QuerySet
# Cho phép dùng các phương thức trên trực tiếp qua Author.objects
AuthorManager = models.Manager.from_queryset(AuthorQuerySet)
