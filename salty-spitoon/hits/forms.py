from django import forms

from utils.helpers import get_hitman_choices

from .models import Hit


class HitCreateForm(forms.ModelForm):
    class Meta:
        model = Hit
        fields = ('hitman', 'target', 'description')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('current_user')
        super(HitCreateForm, self).__init__(*args, **kwargs)
        self.fields['hitman'].label = "Sicario"
        # Only show as options manager's lackeys
        if not user.role == 'boss':
            self.fields['hitman'].widget.choices = get_hitman_choices(user)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })


class HitUpdateForm(forms.ModelForm):
    class Meta:
        model = Hit
        fields = ('hitman', 'target', 'description', 'status', 'requester')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('current_user')
        super(HitUpdateForm, self).__init__(*args, **kwargs)
        is_manager = user.role == 'manager'
        manager_is_hitman = user == self.instance.hitman
        if is_manager and not manager_is_hitman:
            self.fields['hitman'].widget.choices = get_hitman_choices(user)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })


class HitListBulkForm(forms.ModelForm):
    class Meta:
        model = Hit
        fields = ('hitman', 'target', 'description', 'status', 'requester')

    def __init__(self, *args, **kwargs):
        super(HitListBulkForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            if not field == 'hitman':
                self.fields[field].widget = forms.HiddenInput()
        self.fields['hitman'].widget.attrs.update({'class': 'form-control'})
