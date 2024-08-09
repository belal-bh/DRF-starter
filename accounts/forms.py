import phonenumbers
from django import forms
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.safestring import mark_safe
from phonenumber_field.formfields import PhoneNumberField

User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gender',
                  'phone', 'email', 'image',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gender', 'phone',
                  'email', 'image', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class ImagePreviewWidget(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs={'label': ""}, **kwargs)
        img_html = mark_safe(
            f'<br><img src="{value.url}" style="height:200px; width:200px; margin:0 auto; display:flex;" id="imgUpload" /><br><br>')
        return f'{img_html}{input_html}'


class UserUpdateForm(forms.ModelForm):
    # There was a BUG in pre_save and post_save for updating phone
    # So that we will not allow user to update their phone
    # That means we have to remove phone from this form
    # IF we need to change phone we have to do it another form
    # with some constrains
    image = forms.ImageField(label=('Product Image'), required=True, error_messages={
                             'invalid': ("Image files only")}, widget=forms.FileInput,)
    image = forms.ImageField(widget=ImagePreviewWidget,)

    class Meta:
        model = User
        fields = ('image', 'first_name', 'last_name', 'gender', 'email', )
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': "First name",
                'required': True,
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': "Last name",
                'required': True,
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': "Email",
                'required': False,
            }),
            'gender': forms.Select(attrs={
                'required': True,
                'class': 'form-control mb-30 custom-select',
                'style': 'height:50px ;border-radius:0px',
            })

        }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({
            'class': '',
            'id': 'imageUpload',
        })
        self.fields['image'].label = "User Image"

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        if commit:
            user.save()
        return user
