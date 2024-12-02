# from django.shortcuts import render, redirect
# from django.core.mail import send_mail
# from creator.models import Creator
# from django.conf import settings

# def index(request):
#     creators = Creator.objects.all()

#     if request.user.is_authenticated:
#         try:
#             creator = request.user.creator
#         except Exception:
#             return redirect('create_app:admin_home')
        
#     return render(request, 'core/index.html', {
#         'creators': creators
#     })
    
# def admin_home(request):
#     return render(request, 'creator_app/admin_home.html')

# def send_welcome_email(user_email, username):
#     subject = "Welcome to Our Platform"
#     message = f"Hi {username},\n\nWelcome to our platform! We're glad to have you."
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [user_email]
#     send_mail(subject, message, from_email, recipient_list)


from django.shortcuts import render, redirect

from creator.models import Creator


def index(request):
    creators = Creator.objects.all()

    if request.user.is_authenticated:
        try:
            creator = request.user.creator
        except Exception:
            return redirect('create_app:admin_home')
        
    return render(request, 'core/index.html', {
        'creators': creators
    })
    
def admin_home(request):
    return render(request, 'creator_app/admin_home.html')        