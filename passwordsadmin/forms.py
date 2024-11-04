from django.forms import ModelForm
from .models import Password
from django import forms
from django.contrib.auth.models import User

class CreatePasswordForm(ModelForm):
    sharedWith = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'shared-with-checkbox'}),
        label='Shared with'
    )
    
    class Meta:
        model = Password
        fields = ['name', 'url', 'password', 'passwordTag', 'shared', 'sharedWith']
        labels = {
            'name': 'Name',
            'url': 'URL',
            'password': 'Password',
            'passwordTag': 'Tag',
            'shared': 'Shared',
        }

    def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super().__init__(*args, **kwargs)

            if user:
                self.fields['sharedWith'].queryset = User.objects.exclude(id=user.id)

            for field in self.fields.values():
                field.widget.attrs.update({'class': 'form-control'}) 