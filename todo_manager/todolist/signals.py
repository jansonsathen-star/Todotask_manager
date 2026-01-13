from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import LoginHistory
from django.db import models


@receiver(user_logged_in)
def track_user_login(sender, request, user, **kwargs):
    """Track user login with IP address and user agent"""
    # Get IP address
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    # Create login history record
    LoginHistory.objects.create(
        user=user,
        ip_address=ip,
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
    )
