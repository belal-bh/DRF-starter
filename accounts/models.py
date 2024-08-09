from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse
from model_utils import FieldTracker
from phonenumber_field.modelfields import PhoneNumberField

from accounts.helpers import UploadTo


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, email, password, **extra_fields):
        """
        Create and save a user with the given phone, email, and password.
        """
        if not phone:
            raise ValueError('The given phone must be set')
        email = self.normalize_email(email)
        # phone = self.model.normalize_phone(phone)
        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, email, password, **extra_fields)

    def create_superuser(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, email, password, **extra_fields)

    def create_staffuser(self, phone, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staffuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not False:
            raise ValueError('Staffuser must have is_superuser=False.')

        return self._create_user(phone, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    This is User Model is inheriting from two abstruct class AbstractBaseUser and PermissionsMixin.
    There are some predefined fields and methods. If developer want to update something he/she should
    see the details of those abstruct class.
    [NOTE] [How add group for custom user in django?]
    (https://stackoverflow.com/questions/36961180/how-add-group-for-custom-user-in-django)
    """
    class Role(models.TextChoices):
        """
        According to the given instruction User Role List are given bellow:
        1.  Super adminstrator: Somebody with access to site network 
            administration features and all other features of Adminstrator.
        2.  Adminstrator: Somebody who has access to all the administration 
            features within a single site 
        3.  Editor: Somebody who can Publish and manage store and marchent 
            including post/content of user
        4.  Moderator: Somebody who can handle and help to the marchent if 
            they faces any small issue and communicate with them if needed
        5.  Sub Moderator: Somebody who can access and create Ad campaign 
            and do Accounts management.
        6.  Analyst/Auditor: Somebody who can check and Advise about whole 
            operation/management but can’t do a single change to anything to the site.
        """
        SUPER_ADMIN = 'SUPER_ADMIN', 'Super adminstrator'
        ADMIN = 'ADMIN', 'Adminstrator'
        EDITOR = 'EDITOR', 'Editor'
        MODERATOR = 'MODERATOR', 'Moderator'
        SUB_MODERATOR = 'SUB_MODERATOR', 'Sub Moderator'
        ANALYST = 'ANALYST', 'Analyst'

    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_OTHER = 'O'
    GENDER_CHOICES = [
        ('', 'Select Gender'),
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHER, 'Other'),
    ]

    phone = PhoneNumberField(null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
    )
    email = models.EmailField(blank=True, null=True)
    image = models.ImageField(
        default='accounts/user/image/default.png',
        upload_to=UploadTo('image', plus_id=True),
        null=True,
        blank=True,
        width_field="width_field",
        height_field="height_field"
    )
    height_field = models.IntegerField(default=0, null=True)
    width_field = models.IntegerField(default=0, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)  # can login
    is_staff = models.BooleanField(default=False)  # staff user non superuser
    # is_superuser => This is already defined in PermissionsMixin abstruct class
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    # to track field changes using FieldTracker
    tracker = FieldTracker()

    USERNAME_FIELD = 'phone'  # username
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = []  # ['first_name', 'last_name'] #python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.phone.as_e164

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.phone.as_e164

    def get_short_name(self):
        return self.phone.as_e164

    # custom functions
    def get_profile_url(self):
        try:
            url = self.profile.get_absolute_url()
        except:
            url = '#get_profile_url'
        return url

    def get_profile_update_url(self):
        try:
            url = self.profile.get_update_url()
        except:
            url = '#get_profile_update_url'
        return url


# Try to import Profile models here after the User model defined
# because Profile model used User model
# if we try to import Profile before defined User it will raise:
# raise ImproperlyConfigured(django.core.exceptions.ImproperlyConfigured:
# AUTH_USER_MODEL refers to model 'accounts.User' that has not been installed


@receiver(pre_save, sender=User)
def pre_save_user_receiver(sender, instance, *args, **kwargs):
    if instance:
        if instance.tracker.has_changed('phone'):
            # if phone number changed, need to verify that number
            # so that firstly set False to is_verified
            # [BUG]: When a new User is creating it also detect as  phone number changed
            # so that it New User are forcely setting to is_verified = False
            # But we only create a User after phone verification
            # That means New User always should is_verified = True
            # instance.is_verified = False
            # print(f"[PRE_SAVE] instance:{instance} , is_verified:{instance.is_verified}")
            pass


@receiver(post_save, sender=User)
def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if instance:
        if created:
            # create a profile of this user
            from profiles.models import Profile  # isort:skip
            profile_obj, profile_created = Profile.objects.get_or_create(
                user=instance)
            # print(f"instance:{instance}\nprofile_obj:{profile_obj}\nprofile_created:{profile_created}")
        else:
            pass
            # if instance.tracker.has_changed('phone'):
            # if phone number changed, need to verify that number
            # so that firstly set False to is_verified
            # [BUG]: When a new User is creating it also detect as  phone number changed
            # so that it New User are forcely setting to is_verified = False
            # But we only create a User after phone verification
            # That means New User always should is_verified = True
            # print(f"[POST_SAVE] instance:{instance} , is_verified:{instance.is_verified}")
            # instance.is_verified = False
            # instance.save() # never do it, it is a recursive loop
            # SO THAT WE CAN NOT UPDATE USER HERE
            # WE CAN UPDATE USER ONLY IN PRE-SAVE
            # BUT THERE WAS A PROBLEM OF TRACKING PHONE CHANGED AT CREATION TIME
            # THEREFORE, WE HAVE TO DO THIS OUTSIDE PRE-SAVE AND POST-SAVE
            # print(f"[POST_SAVE] instance:{instance} , is_verified:{instance.is_verified}")
