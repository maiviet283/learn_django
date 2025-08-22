from rest_framework.views import exception_handler
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # Xử lý riêng cho MethodNotAllowed
    if isinstance(exc, MethodNotAllowed):
        # Lấy method từ args (nếu có), fallback sang detail
        method = exc.args[0] if exc.args else ""
        return Response(
            {
                "status": False,
                "message": f"Method {method} not allowed on this endpoint",
                "data": None,
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    # Các exception khác
    if response is not None:
        detail = response.data.get("detail") if isinstance(response.data, dict) else "Something went wrong"
        return Response(
            {
                "status": False,
                "message": detail,
                "data": None,
            },
            status=response.status_code,
        )

    return response
