from rest_framework.renderers import JSONRenderer

class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_status = True
        message = ''
        status_code = 200

        if renderer_context:
            response = renderer_context.get("response")
            request = renderer_context.get("request")
            status_code = response.status_code if response else 200

            if status_code >= 400:
                response_status = False
                message = "Something went wrong"
            else:
                method = request.method if request else ''
                if method == 'GET':
                    message = "Fetched successfully"
                elif method == 'POST':
                    message = "Created successfully"
                elif method == 'PUT':
                    message = "Updated successfully"
                elif method == 'PATCH':
                    message = "Patched successfully"
                elif method == 'DELETE':
                    message = "Deleted successfully"

        final_response = {
            "status": response_status,
            "message": message,
            "data": data if isinstance(data, (dict, list)) else None,
        }

        # Nếu data là chuỗi hoặc None (ví dụ HTTP_204_NO_CONTENT), giữ nguyên
        if not isinstance(data, (dict, list)):
            final_response["data"] = None
            final_response["message"] = str(data) if data else message

        return super().render(final_response, accepted_media_type, renderer_context)
