from django.contrib.auth import get_user_model

def create_verified_user_account(phone, password, **extra_args):
    user = get_user_model().objects.create_user(
        phone=phone,
        password=password,
        **extra_args,
        is_active=True,
        is_verified=True,
    )
    
    return user