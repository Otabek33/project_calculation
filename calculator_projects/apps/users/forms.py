from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        error_messages = {
            "username": {"unique": _("This username has already been taken.")},
        }


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """


class UserUpdateForm(forms.ModelForm):
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=True
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=True
    )
    mid_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=True
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=True
    )

    class Meta:
        model = User
        fields = ( "last_name", "first_name", "mid_name", "email")
