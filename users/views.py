from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def role_redirect(request):
    user = request.user

    if hasattr(user, "userprofile") and user.userprofile.is_seller:
        return redirect("seller_dashboard")
    else:
        return redirect("home")  # student products page
