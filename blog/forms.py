from allauth.account.forms import LoginForm as AllauthLoginForm

from django import forms

from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


class LoginForm(AllauthLoginForm):
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            attrs={
                'data-theme': 'light',
                'data-size': 'normal',
            }
        )
    )