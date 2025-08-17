from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Book, Author
import threading
import time


# === Hàm gửi email (chạy nền) ===
def send_welcome_email(author):
    try:
        time.sleep(2)
        print(f"Đã gửi email chào mừng đến {author.name} - {author.age} tuổi")
    except Exception as e:
        print(f"Gửi email thất bại cho {author.name}: {e}")


# === Signal cho Book ===
@receiver(pre_save, sender=Book)
def book_pre_save_handler(sender, instance, **kwargs):
    try:
        if instance.pk:
            print("Bạn đã thay đổi dữ liệu trong Book (update).")
        else:
            print("Bạn đã thêm dữ liệu mới vào Book (create).")
    except Exception as e:
        print(f"Lỗi trong signal Book: {e}")


# === Signal cho Author ===
@receiver(pre_save, sender=Author)
def send_email_pre_save_handler(sender, instance, **kwargs):
    try:
        if not instance.pk:
            thread = threading.Thread(target=send_welcome_email, args=(instance,))
            thread.start()
        else:
            print("Bạn đã thay đổi dữ liệu trong Author (update).")
    except Exception as e:
        print(f"Lỗi trong signal Author: {e}")