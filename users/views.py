from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def role_redirect(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if profile.is_seller:
        return redirect("/orders/seller/dashboard/")
    return redirect("/products/")
