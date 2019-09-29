from django import forms
from django.contrib import admin

import iban.models


class AdminIBANForm(forms.ModelForm):
    iban = iban.models.IBANFormField(widget=forms.TextInput(attrs={'size': iban.models.IBAN_LENGTH * 2}))

    class Meta:
        model = iban.models.IBAN
        fields = '__all__'


class IBANAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, change=False, **kwargs):
        if request.user.is_superuser:
            return AdminIBANForm
        return super(IBANAdmin, self).get_form(request, obj, change, **kwargs)


admin.site.register(iban.models.IBAN, IBANAdmin)
