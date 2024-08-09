# Accounts

## Q [What's the best way to store Phone number in Django models](https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models)

```
    1. Phone by PhoneNumberField
    You can use phonenumber_field library. It is port of Google's libphonenumber library, which powers Android's phone number handling https://github.com/stefanfoulis/django-phonenumber-field

    In model:

    from phonenumber_field.modelfields import PhoneNumberField

    class Client(models.Model, Importable):
        phone = PhoneNumberField(null=False, blank=False, unique=True)
    In form:

    from phonenumber_field.formfields import PhoneNumberField
    class ClientForm(forms.Form):
        phone = PhoneNumberField()
    Get phone as string from object field:

        client.phone.as_e164 
    Normolize phone string (for tests and other staff):

        from phonenumber_field.phonenumber import PhoneNumber
        phone = PhoneNumber.from_string(phone_number=raw_phone, region='RU').as_e164
```

Installation
```bash
    pip install django-phonenumber-field[phonenumbers]
```

## PROBLEM Q [AUTH_USER_MODEL refers to model 'accounts.User' that has not been installed](https://stackoverflow.com/questions/48077112/auth-user-model-refers-to-model-accounts-user-that-has-not-been-installed/56133886#56133886)

## Q [When saving, how can you check if a field has changed?
](https://stackoverflow.com/questions/1355150/when-saving-how-can-you-check-if-a-field-has-changed/28094442#28094442)

-   [ans for using django-model-utils](https://stackoverflow.com/a/26026613)

There are huge discusion about this topic. I am selecting solution which is suitable for my application.


## PROBLEM Q [How add group for custom user in django?](https://stackoverflow.com/questions/36961180/how-add-group-for-custom-user-in-django)
-   [Custom users and permissions](https://docs.djangoproject.com/es/3.1/topics/auth/customizing/#custom-users-and-permissions)
```python
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ...
```
BUT IMPORTANT COMMENT: 
Thank you. This answer was helpful. Just I want to add one more in here for newbie. If you inherit PermissionsMixin after you already have done migration and migrate with your custom user model, It doesn't create relationship between your custom user model and group or permissions. I was confused for awhile because after inheriting PermissionMixin, I couldn't find tables in db for relationship between user and Group or user and Permission.

