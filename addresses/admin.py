from django.contrib import admin

import addresses.models


class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('name', 'full_address', 'user')
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        if not change:
            cleaned_data = {k: v for k, v in form.cleaned_data.items() if v is not None and k != 'full_address'}
            existed_obj = addresses.models.UserAddress.find(user=request.user, **cleaned_data)
            if existed_obj:
                form = type(form)(data=request.POST or None, instance=existed_obj)
                form.is_valid()
                obj = form.save(commit=False)
                change = True
        super().save_model(request, obj, form, change)


admin.site.register(addresses.models.UserAddress, UserAddressAdmin)
