from django.forms import ModelForm
from .models import Password
from django import forms
from django.contrib.auth.models import User

class CreatePasswordForm(ModelForm):
    sharedWith = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'shared-with-checkbox'}),
        label='Compartir con:'
    )
    
    class Meta:
        model = Password
        fields = ['name', 'url', 'password', 'passwordTag', 'shared', 'sharedWith']
        labels = {
            'name': 'Nombre de usuario o correo utilizado',
            'url': 'URL del sitio',
            'password': 'Contraseña',
            'passwordTag': 'Etiqueta (opcional - 12 caracteres máx.)',
            'shared': 'Compartir contraseña',
        }

    def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super().__init__(*args, **kwargs)

            if user:
                self.fields['sharedWith'].queryset = User.objects.exclude(id=user.id)

            for field in self.fields.values():
                field.widget.attrs.update({'class': 'form-control'}) 