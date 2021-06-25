from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Nombre', required=True)
    last_name = forms.CharField(label='Apellido', required=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')


class UpdateUserForm(forms.ModelForm):
    is_active = forms.ChoiceField(
        choices=((False, 'Si'), (True, 'No')),
        initial=True,
        widget=forms.RadioSelect(),
        required=True
    )

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'role', 'is_active')
