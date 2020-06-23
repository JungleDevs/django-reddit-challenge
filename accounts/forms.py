"""
Accounts Form
"""
###
# Libraries
###
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings


###
# Forms
###
class CustomResetPasswordForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        reset_url = '{}/change-password/{}/{}'.format(
            settings.FE_URL,
            context.get('uid'),
            context.get('token')
        )
        context.update({
            'reset_url': reset_url,
        })
        return super().send_mail(
            subject_template_name=subject_template_name,
            email_template_name=email_template_name,
            context=context,
            from_email=from_email,
            to_email=to_email,
            html_email_template_name=html_email_template_name
        )
