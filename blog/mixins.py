from django.shortcuts import redirect


class LoginBlogRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account:login")
        return super(LoginBlogRequiredMixin, self).dispatch(request, *args, **kwargs)