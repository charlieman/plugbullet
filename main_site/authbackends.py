from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
#         if '@' in username:
#             kwargs = {'email': username}
#         else:
#             kwargs = {'username': username}
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
