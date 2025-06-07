import datetime
import logging
from django.http import HttpResponseForbidden
import time

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        logging.basicConfig(filename='requests.log',level=logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.datetime.now()} - User: {user} - Path: {request.path}"

        logging.info(log_message)

        response = self.get_response(request)
        return response
    

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.datetime.now().time()
        restricted_hours = (datetime.time(21, 0), datetime.time(6, 0))  # 9 PM - 6 AM

        if restricted_hours[0] <= current_time or current_time <= restricted_hours[1]:
            return HttpResponseForbidden("Access to chat is restricted outside 9 PM - 6 AM.")

        response = self.get_response(request)
        return response
    

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_tracker = {}  # Stores IP and timestamps

    def __call__(self, request):
        if request.method == 'POST':  # Only monitor chat messages
            ip = self.get_client_ip(request)
            current_time = time.time()

            # Initialize the tracking for new IPs
            if ip not in self.message_tracker:
                self.message_tracker[ip] = []

            # Filter out timestamps older than 1 minute
            self.message_tracker[ip] = [
                t for t in self.message_tracker[ip] if current_time - t < 60
            ]

            # Restrict message count to 5 per minute
            if len(self.message_tracker[ip]) >= 5:
                return HttpResponseForbidden("Too many messages sent in a short time. Please slow down.")

            # Log this message request timestamp
            self.message_tracker[ip].append(current_time)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Extracts IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin") or request.path.startswith("/moderate"):
            user = request.user
            if not user.is_authenticated or user.role not in ["admin", "moderator"]:
                return HttpResponseForbidden("You do not have permission to access this page.")

        response = self.get_response(request)
        return response