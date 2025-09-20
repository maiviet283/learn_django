import base64
import zlib
from django.core.signing import loads

# Đây là chuỗi session_data demo của bạn
signed_session = '.eJxVjDsOwjAQBe_iGllZ_4gp6XMGy7ve4ACypTipEHcHSylAetWb0bxEiPuWw954DUsSFwHi9PthpAeXDtI9lluVVMu2Lii7Ig_a5FQTP6-H-xfIseWeNe7M3_EAbGzS0WB0yMrYERBw9qPVOJNX3g3gHYFKxhER2IRWKyfeH9w0N5w'

# 1. Cắt bỏ dấu chấm đầu
session_payload = signed_session[1:]

# 2. Base64 decode
compressed = base64.urlsafe_b64decode(session_payload + '==')  # thêm padding nếu thiếu

# 3. Zlib decompress
decompressed = zlib.decompress(compressed)

# 4. Xem kết quả (dạng bytes)
print(decompressed)
