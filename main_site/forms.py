from django import forms
from django.utils.translation import ugettext_lazy as _
import re
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    username = forms.CharField(label=_(u'Username'), max_length=30)
    email = forms.EmailField(label=_(u'Email'))
    password1 = forms.CharField(
        label=_(u'Password'),
        widget=forms.PasswordInput(render_value=False)
    )
    password2 = forms.CharField(
        label=_('Password (Again)'),
        widget=forms.PasswordInput(render_value=False)
    )

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data.get("password1", "")
            password2 = self.cleaned_data["password2"]
            if password1 == password2:
                return password2
        raise forms.ValidationError(_("Password didn't match."))

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError(_("Username can only contain alphanumeric characters and underscore."))
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with that username already exists."))
