from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('phone', 'email', 'is_superuser', 'is_verified')
    list_filter = ('is_superuser', 'is_staff', 'is_active', 'is_verified')
    fieldsets = (
        ('Secret Info', {'fields': ('phone', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name',
                           'gender', 'image')}),
        # ('Full name', {'fields': ()}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff',
         'is_active', 'groups', 'user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2')}
         ),
    )
    search_fields = ('phone', 'email', 'first_name', 'last_name',)
    ordering = ('phone', 'email')
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

# Remove Group Model from admin. We're not using it.
# admin.site.unregister(Group)
