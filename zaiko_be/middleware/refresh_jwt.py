from rest_framework_simplejwt.tokens import AccessToken
from django.utils.deprecation import MiddlewareMixin


class RefreshJWTMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated:
            # create new jwt token
            token = AccessToken.for_user(request.user)
            response["X-Access-Token"] = f"{str(token)}"
        return response
