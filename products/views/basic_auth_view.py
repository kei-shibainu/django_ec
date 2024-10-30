import base64
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse

class BasicAuthMixIn(UserPassesTestMixin):
    def test_func(self):
        auth = self.request.META.get('HTTP_AUTHORIZATION')
        if auth:
            try:
                auth_type, auth_info = auth.split(' ', 1)
                if auth_type.lower() == 'basic':
                    decoded = base64.b64decode(auth_info).decode('utf-8')
                    username, password = decoded.split(':', 1)
                    user = authenticate(username=username, password=password)
                    if user is not None and user.is_superuser:
                        self.request.user = user
                        return True
            except (ValueError, base64.binascii.Error):
                return False
        return False

    def handle_no_permission(self):
        response = HttpResponse('Unauthorized: Access Denide', status=401)
        response['WWW-Authenticate'] = 'Basic realm="Protected Area"'
        return response