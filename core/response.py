from rest_framework.response import Response

def success_response(message: str, status_code: int = 200, data=None) -> Response:
    body = {
        'success': True,
        'status_code': status_code,
        'message': message,
    }
    if data is not None:
        body['data'] = data

    return Response(body, status=status_code)
