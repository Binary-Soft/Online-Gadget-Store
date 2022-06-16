from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 
        'class':'newpassword', 'placeholder': 'New Password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirm New password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
        'class':'confirmnewpassword', 'placeholder': 'Confirm Password'}),
    )