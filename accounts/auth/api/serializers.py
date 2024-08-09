import phonenumbers
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from phone_verify.serializers import SMSVerificationSerializer

from accounts.sms_backends.utils import check_verified_phone_number

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
                "id",
                "phone",
                "first_name",
                "last_name",
                "gender",
                "email",
                "image",
                "height_field",
                "width_field",
                "is_verified",
                "is_active",
            ]


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(style={'input_type': "password"}, trim_whitespace=False, required=True)

    def validate(self, attrs):
        phone = attrs.get("phone")
        password = attrs.get("password")

        try:
            phone_instance = phonenumbers.parse(phone, "BD")
            if not phonenumbers.is_possible_number(phone_instance):
                raise serializers.ValidationError(
                    "Invalid phone number (is_possible_number: False)")
            if not phonenumbers.is_valid_number(phone_instance):
                raise serializers.ValidationError(
                    "Invalid phone number (is_valid_number: False)")
        except phonenumbers.phonenumberutil.NumberParseException:
            raise serializers.ValidationError("Invalid phone number")
        user = authenticate(request=self.context.get('request'),
                            username=phone_instance, password=password)
        
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        attrs['user'] = user

        return super().validate(attrs)

        
class CreateUserSerializer(serializers.ModelSerializer):
    """A serializer for creating new users after phone verification. Includes all the required
    fields, plus a repeated password."""
    phone = serializers.CharField(required=True)
    password = serializers.CharField(style={'input_type': "password"}, trim_whitespace=False, required=True)
    phone_otp = serializers.CharField(required=True)
    phone_token = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gender',
                  'email', 'phone', 'password', 'phone_otp', 'phone_token')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_phone(self, value):
        phone = value
        try:
            phone_instance = phonenumbers.parse(phone, "BD")
            if not phonenumbers.is_possible_number(phone_instance):
                raise serializers.ValidationError("Invalid phone number")
                # (is_possible_number: False)
            if not phonenumbers.is_valid_number(phone_instance):
                raise serializers.ValidationError("Invalid phone number")
                # (is_possible_number: False)
        except phonenumbers.phonenumberutil.NumberParseException:
            raise serializers.ValidationError("Invalid phone number")
        # check is it (account of this phone) already exist or not
        # probably this field is uneditable but we will check it
        existed_user = User.objects.filter(phone=phone_instance).first()
        if existed_user:
            raise serializers.ValidationError(
                "Invalid phone. Account already exist!")

        # in this case we will return phonenumbers phone_instance
        # because it will store in databse as an phone_instance
        # but if we want to use this phone_instance in views then
        # we need to convert it as str (phone_as_e164)
        return phone_instance
    
    def validate(self, attrs):
        attrs = super().validate(attrs)
        is_verified_phone_number = check_verified_phone_number(
                attrs.get('phone'), attrs.get('phone_otp'), attrs.get('phone_token')
            )
        if not is_verified_phone_number:
            raise serializers.ValidationError("Phone number is not verified. Phone verification is required.")
        return attrs
    

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('phone_otp')
        validated_data.pop('phone_token')

        user = User(**validated_data)

        user.set_password(password)
        user.is_active = True
        # set is_verified = True because user already verified
        user.is_verified = True
        user.save()
        return user
    


class UserSignUpSerializer(serializers.Serializer):
    """A serializer for creating new users after phone verification. Includes all the required
    fields."""
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    gender = serializers.ChoiceField(User.GENDER_CHOICES, required=True)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(style={'input_type': "password"}, trim_whitespace=False, required=True)



class PhoneVerifyAndSignUpSerializer(UserSignUpSerializer, SMSVerificationSerializer):
    def validate_phone_number(self, value):
        phone = value
        # check is it (account of this phone) already exist or not
        # probably this field is uneditable but we will check it
        existed_user = User.objects.filter(phone=phone).first()
        if existed_user:
            raise serializers.ValidationError(
                "Invalid phone. Account already exist!")

        return phone


class ResetPasswordSerializer(serializers.Serializer):
    """A serializer for resetting password after phone verification. Includes all the required
    fields."""
    password = serializers.CharField(style={'input_type': "password"}, trim_whitespace=False, required=True)



class PhoneVerifyAndResetPasswordSerializer(ResetPasswordSerializer, SMSVerificationSerializer):
    def validate_phone_number(self, value):
        phone = value
        # check is it (account of this phone) already exist or not
        # probably this field is uneditable but we will check it
        existed_user = User.objects.filter(phone=phone).first()
        if not existed_user:
            raise serializers.ValidationError(
                "Invalid phone. Account does not exist!")

        return phone