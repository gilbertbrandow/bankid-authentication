from rest_framework.exceptions import AuthenticationFailed

class CustomAuthentication():
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        token = auth_header.split(' ')[1]
        if not self.validate_token(token):
            raise AuthenticationFailed('Invalid token')

        return (self.get_user(token), None)

    def validate_token(self, token):
        return True

    def get_user(self, token):
        return CustomUser(token=token)

class CustomUser:
    def __init__(self, token):
        self.token = token
        self.username = 'custom_user'
