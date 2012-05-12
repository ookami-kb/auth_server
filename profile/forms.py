# -*- coding: utf-8 -*-
from django import forms
from .models import UserProfile

class ProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label=u"Текущий пароль")
    password1 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label=u"Новый пароль", required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=False),
                                label=u'Подтверждение пароля', required=False)
    
    class Meta:
        model = UserProfile
        exclude = ('user',)
        
    def clean_password(self):
        instance = getattr(self, 'instance', None)
        if instance and self.instance.user.check_password(self.cleaned_data['password']):
            return self.cleaned_data['password']
        else:
            raise forms.ValidationError(u"Неправильный пароль")
        
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(u"Введенные пароли не совпадают.")
        return self.cleaned_data