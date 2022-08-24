# from django.template.loader import render_to_string
# from django.core.mail import EmailMessage
# from django.conf import settings
#
# from user.models import User
#
# def send_confirmation_mail(username, email):
#     user = User.objects.filter(email=email)
#     current_site = User.objects.get_current().domain
#     message={
#         'username': username,
#         'email': email,
#         'domain': current_site,
#
#     }
#     email_subject = 'Activation Mail'
#     email_body = render_to_string('activation_mail.html', message)
#
#     email = EmailMessage(
#         email_subject, email_body,
#         settings.DEFAULT_FROM_EMAIL, [email, ],
#     )
#     return email.send(fail_silently=False)
#
#
#
