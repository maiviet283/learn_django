Ok, để bạn hiểu **toàn bộ quan hệ giữa các file trong project Django và hệ thống Nginx + Gunicorn**, mình sẽ giải thích từng phần và cách chúng liên kết với nhau, từ browser tới database, với cả socket và service.

---

## 1️⃣ **Các thành phần trong project Django**

Giả sử project của bạn là `my_shop`:

```
my_shop/
├── my_shop/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── home/
├── products/
├── staticfiles/
├── media/
├── manage.py
└── venv/
```

* **`settings.py`**: cấu hình Django (DB, static, media…).
* **`wsgi.py`**: điểm bắt đầu WSGI, Gunicorn gọi biến `application` ở đây.
* **`staticfiles/`**: nơi collectstatic gom toàn bộ CSS/JS/images từ các app.
* **`media/`**: file người dùng upload.
* **`venv/`**: môi trường ảo chứa Python packages, Gunicorn cũng nằm ở đây.

---

## 2️⃣ **Gunicorn service (`.service`)**

File `gunicorn.service` nằm trong `/etc/systemd/system/`:

```ini
[Service]
User=maiviet
Group=www-data
WorkingDirectory=/home/maiviet/my_shop
ExecStart=/home/maiviet/venv/bin/gunicorn \
          --bind unix:/run/gunicorn/gunicorn.sock \
          my_shop.wsgi:application
RuntimeDirectory=gunicorn
```

### Mối quan hệ:

* **Gunicorn đọc project Django** qua:

  * `WorkingDirectory`: thư mục project chứa `manage.py`.
  * `my_shop.wsgi:application`: điểm entry để Gunicorn gọi Django app.

* **Gunicorn tạo socket Unix**:

  * `--bind unix:/run/gunicorn/gunicorn.sock` → Gunicorn tạo file `/run/gunicorn/gunicorn.sock`.
  * `RuntimeDirectory=gunicorn` → systemd tự tạo thư mục `/run/gunicorn/` khi start service.

* Socket này **giống như “cổng nội bộ”** cho Nginx kết nối đến Gunicorn.

---

## 3️⃣ **Nginx**

File `/etc/nginx/sites-available/my_shop`:

```nginx
location /static/ {
    alias /home/maiviet/my_shop/staticfiles/;
}
location /media/ {
    alias /home/maiviet/my_shop/media/;
}
location / {
    proxy_pass http://unix:/run/gunicorn/gunicorn.sock;
}
```

### Mối quan hệ:

1. `/static/` → Nginx trực tiếp đọc file từ `staticfiles/` trên disk.
2. `/media/` → Nginx đọc từ `media/`.
3. Các URL còn lại → Nginx **proxy tới Gunicorn qua socket** `/run/gunicorn/gunicorn.sock`.

> Gunicorn nhận request từ Nginx → gọi Django → Django trả response → Nginx gửi lại client.

---

## 4️⃣ **Unix socket `/run/gunicorn/gunicorn.sock`**

* Là **file đặc biệt** do Gunicorn tạo ra.
* Nginx “mở” file này như một cổng để gửi HTTP request tới Gunicorn.
* `User=maiviet` + `Group=www-data` → Nginx (chạy group `www-data`) có quyền đọc/ghi socket.

---

## 5️⃣ **Flow request tổng thể**

```
Browser
   │
   ▼
HTTP Request -> Nginx (port 80)
   │
   ├─ /static/* → serve file trực tiếp từ /home/maiviet/my_shop/staticfiles/
   ├─ /media/* → serve file trực tiếp từ /home/maiviet/my_shop/media/
   └─ other URLs → proxy_pass http://unix:/run/gunicorn/gunicorn.sock
                        │
                        ▼
                 Gunicorn worker
                        │
                        ▼
                 Django wsgi.application
                        │
                        ▼
                 Database / ORM
                        │
                        ▼
                 Response trả về Gunicorn
                        │
                        ▼
                 Nginx → Browser
```

---

## 6️⃣ **Tóm tắt mối quan hệ**

| Thành phần                  | Nơi lưu / file liên quan               | Vai trò                                      |
| --------------------------- | -------------------------------------- | -------------------------------------------- |
| Django project (`my_shop/`) | `/home/maiviet/my_shop/`               | Chứa code, wsgi.py, settings.py              |
| Virtualenv (`venv/`)        | `/home/maiviet/venv/`                  | Chứa Python packages, Gunicorn               |
| Gunicorn service            | `/etc/systemd/system/gunicorn.service` | Quản lý Gunicorn, start/stop khi boot        |
| Gunicorn socket             | `/run/gunicorn/gunicorn.sock`          | Nginx kết nối tới Gunicorn                   |
| Nginx config                | `/etc/nginx/sites-available/my_shop`   | Chỉ định static/media + proxy tới Gunicorn   |
| Static files                | `/home/maiviet/my_shop/staticfiles/`   | CSS/JS/images, được Nginx phục vụ trực tiếp  |
| Media files                 | `/home/maiviet/my_shop/media/`         | User-uploaded files, Nginx phục vụ trực tiếp |

---