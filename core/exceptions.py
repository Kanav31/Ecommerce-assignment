from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def global_exception_handler(exc, context):
    """Normalises all errors to { error: true, message: '...' }"""
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            'error':   True,
            'message': _extract_message(response.data),
        }
        return response

    return Response(
        {'error': True, 'message': 'An unexpected error occurred.'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


def _extract_message(data):
    if isinstance(data, str):
        return data

    if isinstance(data, dict):
        if 'detail' in data:
            return str(data['detail'])
        for field, messages in data.items():
            if isinstance(messages, list) and messages:
                return f'{field}: {messages[0]}'
            if isinstance(messages, str):
                return f'{field}: {messages}'

    if isinstance(data, list) and data:
        return str(data[0])

    return 'An error occurred.'
