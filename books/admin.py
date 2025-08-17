# admin.py
from django.contrib import admin
from .models import Author, Book

# Inline cho Book để hiển thị trong trang Author
class BookInline(admin.StackedInline):
    model = Book                         # Model con cần hiển thị
    extra = 1                            # Hiển thị 1 dòng trống để thêm mới
    fields = ('title', 'description', 'created_at')  # Các trường hiển thị
    readonly_fields = ('created_at',)   # created_at là chỉ đọc
    show_change_link = True             # Cho phép nhấp vào để chỉnh sửa riêng Book
    can_delete = True                   # Cho phép xóa Book trong inline
    verbose_name = "Tác phẩm"
    verbose_name_plural = "Các tác phẩm"

# Tùy chỉnh trang quản trị của Author
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'created_at')  # Hiển thị các cột trong danh sách
    list_filter = ('age', 'created_at')                # Bộ lọc bên phải
    search_fields = ('name',)                          # Thanh tìm kiếm theo tên
    inlines = [BookInline]                             # Chèn inline Book vào Author
    readonly_fields = ('created_at',)                  # Trường không cho chỉnh sửa
    ordering = ('-created_at',)                        # Sắp xếp theo ngày tạo mới nhất
    date_hierarchy = 'created_at'                      # Bộ lọc theo ngày ở đầu trang

# Tùy chỉnh trang quản trị của Book
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'short_description', 'created_at')
    list_filter = ('author__name', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    # Hiển thị mô tả rút gọn trong list_display
    def short_description(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    short_description.short_description = 'Mô tả ngắn'
