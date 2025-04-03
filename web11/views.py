from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

def send_password_reset_email(request):
    email = request.POST.get("email")
    user = get_object_or_404(User, email=email)
    token = default_token_generator.make_token(user)
    reset_link = f"http://localhost:8000/reset-password/{token}"
    
    send_mail(
        "Скидання пароля",
        f"Натисніть тут, щоб скинути пароль: {reset_link}",
        "your@email.com",
        [email],
    )
    return JsonResponse({"message": "Лист надіслано!"})
