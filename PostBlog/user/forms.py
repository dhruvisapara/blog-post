from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm, AuthenticationForm
from django.contrib.auth.models import Group
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from user.models import User


class SignUpForm(UserCreationForm):
    """this form includes User model field and also have UserCreationForm fields"""

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'mobile_number',
            'birth_date',
            'address',
            'age',
            'profession',
            'profile_image',

        ]

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password1"])
        user.profile_image = self.cleaned_data.get('profile_image')
        if commit:
            user.save()

        return user


class UpdateForm(UserChangeForm):
    """if user wants to update the information or edit the information"""

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'mobile_number',
            'birth_date',
            'address',
            'age',
            'profession',
            'profile_image',
        ]


class SetNewPasswordForm(SetPasswordForm):
    """this form is override from SetPasswordForm to remove helptext from the password"""
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    new_password1 = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,

    )
    new_password2 = forms.CharField(
        label=_("Confirm password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )


class GroupForm(ModelForm):
    """This form is for permission delete and update"""

    class Meta:
        model = Group
        fields = '__all__'
