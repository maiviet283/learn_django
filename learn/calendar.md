Chúc mừng bạn có lịch phỏng vấn! 🚀

---

## 1. Ôn lại kiến thức chuyên môn (theo JD)

👉 Những mảng bạn chắc chắn sẽ bị hỏi:

* **Django**:

  * Cách tổ chức project (apps, settings, urls, views, models).
  * Django ORM (select, filter, annotate, prefetch, select\_related).
  * Middleware, signals, authentication.
  * Django REST Framework (serializer, viewset, permission, JWT/OAuth2).
* **API**: RESTful principles, cách thiết kế endpoint rõ ràng, pagination, error handling.
* **Database**: Quan hệ 1-nhiều, nhiều-nhiều, index, transaction, migration. Có thể hỏi SQL query tối ưu.
* **Testing**: Unit test trong Django, pytest, mock.
* **Deployment**: Gunicorn/Uvicorn + Nginx, Docker, CI/CD cơ bản.

👉 JD có nhắc thêm:

* **IoT, Websocket, Message Broker, Microservices**

  * Websocket: cách làm realtime trong Django (Django Channels).
  * Message broker: RabbitMQ, Kafka, hoặc Redis pub/sub – bạn nên nắm cách dùng trong bối cảnh microservice.
  * Microservices: hiểu kiến trúc, tại sao tách, ưu & nhược điểm, cách giao tiếp (REST, gRPC, Message Queue).
  * IoT: không cần quá sâu, nhưng nên hiểu luồng dữ liệu từ thiết bị → server → xử lý → lưu trữ.

* **Cloud (AWS/GCP)**

  * Nắm khái niệm cơ bản: EC2/Compute Engine, S3/Cloud Storage, RDS/CloudSQL, IAM.
  * Deploy Django app lên cloud (dùng Docker thì càng tốt).

---

## 2. Chuẩn bị tình huống thực tế

Phỏng vấn thường có 2 dạng câu hỏi:

* **Technical**:

  * Viết nhanh 1 API đơn giản với Django/DRF.
  * Giải thích cách bạn thiết kế hệ thống realtime chat (Websocket + Redis + Django Channels).
  * Tình huống: API đang chậm, bạn xử lý thế nào? (Index DB, caching, queue background job).

* **Behavioral (HR)**:

  * “Hãy kể về một project bạn từng làm với Django?”
  * “Bạn xử lý khi team conflict như thế nào?”
  * “Bạn học công nghệ mới ra sao?”

👉 Bạn nên chuẩn bị 1-2 dự án cá nhân/thực tập/làm nhóm có thật để kể (có API, có DB, có triển khai).

---

## 3. Chuẩn bị trước ngày phỏng vấn

* **Ôn lại project cá nhân**: Biết rõ kiến trúc, bạn dùng Redis/Django REST/JWT ra sao.
* **Nắm chắc keyword trong JD**: Django, REST API, Websocket, Microservice, AWS.
* **Thực hành code ngắn**: Viết CRUD API trong 15 phút.
* **Chuẩn bị câu hỏi cho interviewer**: Ví dụ:

  * “Team mình có đang dùng microservices hay monolith?”
  * “Message broker hiện tại bên mình đang chọn Kafka hay RabbitMQ?”
  * “Với IoT data, bên mình xử lý realtime thế nào?”

Điều này giúp bạn ghi điểm là người quan tâm & chủ động.

---

👉 Gợi ý timeline ôn tập (vì còn 3 ngày):

* **23/08**: Ôn Django + DRF (model, serializer, viewset, auth).
* **24/08**: Websocket (Channels), Message Broker (RabbitMQ/Redis), Microservices concepts.
* **25/08 sáng**: Review project cá nhân, chuẩn bị câu trả lời ngắn gọn, luyện nói.

---

Bạn có muốn mình giúp bạn **soạn bộ 15 câu hỏi + đáp án mẫu (technical + behavioral)** để luyện tập trước ngày phỏng vấn không?
