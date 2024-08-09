import datetime
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.timezone import utc
from phone_verify.models import SMSVerification

# Settings for phone_verify utils
try:
    phone_verification_utils_settings = settings.PHONE_VERIFICATION_UTILS
except AttributeError:
    raise ImproperlyConfigured(
        "Please define PHONE_VERIFICATION_UTILS in settings")

SCHEME = phone_verification_utils_settings.get('SCHEME')
HOST = phone_verification_utils_settings.get('HOST')
PHONE_VERIFY_REGISTER_PATH = phone_verification_utils_settings.get(
    'PHONE_VERIFY_REGISTER_PATH')
PHONE_VERIFY_VERIFY_PATH = phone_verification_utils_settings.get(
    'PHONE_VERIFY_VERIFY_PATH')


def get_time_diff_second(time_since):
    """
        [TIME DIFF]: https://stackoverflow.com/a/16016130/8520849
        Return time difference in seconds
    """
    if time_since:
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        timediff = now - time_since
        return timediff.total_seconds()


def check_verified_phone_number(phone_number, security_code, session_token, expire_time_from_modified_at=5):
    smsv_instance = SMSVerification.objects.filter(
        phone_number=phone_number,
        security_code=security_code,
        session_token=session_token,
        is_verified=True
    ).first()
    if smsv_instance:
        # check expire_time_from_modified_at limit exit or not
        diff_second = get_time_diff_second(smsv_instance.modified_at)
        if (int(diff_second)//60) > expire_time_from_modified_at:
            # that means time limit exit
            # delete this smsv_instance and return False
            smsv_instance.delete()
            return False
        else:
            return True
    else:
        False
