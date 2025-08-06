import time
from collections import defaultdict
from django.http import JsonResponse, HttpResponseForbidden
import logging
from datetime import datetime, time

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger("request_logger")
        handler = logging.FileHandler("requests.log")
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)

        response = self.get_response(request)
        return response
    

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        allowed_start = time(18, 0)  
        allowed_end = time(21, 0)   

        if request.path.startswith('/api/messages/') or request.path.startswith('/chats'):
            if not (allowed_start <= now <= allowed_end):
                return HttpResponseForbidden("Chat access is only allowed between 6PM and 9PM.")

        return self.get_response(request)
    


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_counts = defaultdict(list)

    def __call__(self, request):
        # Only monitor POST requests to messaging endpoints
        if request.method == 'POST' and request.path.startswith('/api/v1/messages/'):
            ip = self.get_client_ip(request)
            current_time = time.time()

            self.message_counts[ip] = [t for t in self.message_counts[ip] if current_time - t < 60]

            if len(self.message_counts[ip]) >= 5:
                return JsonResponse(
                    {"error": "Message rate limit exceeded. Only 5 messages allowed per minute."},
                    status=429
                )

            self.message_counts[ip].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


