# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.core.mail import send_mail
# from django.conf import settings
# from .models import CustomUser1


# # Utility function to send welcome email
# def send_welcome_email(user_email, username):
#     subject = "Welcome to Our Platform"
#     message = f"Hi {username},\n\nWelcome to our platform! We're glad to have you."
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [user_email]
#     send_mail(subject, message, from_email, recipient_list)


# # Custom UserAdmin class
# @admin.register(CustomUser1)
# class CustomUserAdmin(UserAdmin):
#     model = CustomUser1
#     list_display = ('username', 'email', 'is_staff')

#     def save_model(self, request, obj, form, change):
#         # Send welcome email only for newly created users
#         if not change:  # `change` is False when creating a new user
#             send_welcome_email(obj.email, obj.username)
#         super().save_model(request, obj, form, change)
