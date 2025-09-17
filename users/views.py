from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

# Create your views here.
class ActivateUserView(View):
    """View to handle user account activation via email link."""
    template_success = "users/activation_success.html"
    template_invalid = "users/activation_invalid.html"

    def get(self, request, uid, token, *args, **kwargs):
        User = get_user_model()
        user = None
        try:
            uid_str = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid_str)
        except Exception:
            pass

        if user and default_token_generator.check_token(user, token):
            if not user.is_active:
                user.is_active = True
                user.save(update_fields=["is_active"])
            return render(request, self.template_success, status=200)

        return render(request, self.template_invalid, status=400)