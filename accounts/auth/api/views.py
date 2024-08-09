from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED
from django.contrib.auth import get_user_model, login
from knox.views import LoginView as KnoxLoginView
from phone_verify.api import VerificationViewSet

from .serializers import (
        LoginSerializer,
        PhoneVerifyAndResetPasswordSerializer,
        UserSerializer,
        CreateUserSerializer,
        PhoneVerifyAndSignUpSerializer,
    )
from .services import create_verified_user_account

User = get_user_model()


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request=request, user=user)
            response = super().post(request, format)
        else:
            return Response({'errors': serializer.errors}, status=HTTP_400_BAD_REQUEST)
        return Response(response.data, status=HTTP_200_OK)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing users.

    * Only admin users are able to access this view.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserSignUpView(APIView):
    """
    View to sign up a user in the system.
    """
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response({'errors': serializer.errors}, status=HTTP_400_BAD_REQUEST)
        
        return Response({"message": "User creation success"}, status=HTTP_201_CREATED)
    


class PhoneVerifyAuthViewSet(VerificationViewSet):
    @action(detail=False, methods=['POST'], url_path='signup', permission_classes=[AllowAny], serializer_class=PhoneVerifyAndSignUpSerializer)
    def signup(self, request):
        """Function to verify phone number and register a user

        Most of the code here is corresponding to the "verify" view already present in the package.

        """
        serializer = PhoneVerifyAndSignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone = serializer.validated_data.pop('phone_number')
            serializer.validated_data.pop('security_code')
            serializer.validated_data.pop('session_token')
            password = serializer.validated_data.pop('password')
            user = create_verified_user_account(
                phone=phone,
                password=password,
                **serializer.validated_data,
            )
        else:
            return Response({'errors': serializer.errors}, status=HTTP_400_BAD_REQUEST)

        return Response({"message": "User creation success"}, status=HTTP_201_CREATED)
    


    @action(detail=False, methods=['POST'], url_path='reset-password', permission_classes=[AllowAny], serializer_class=PhoneVerifyAndResetPasswordSerializer)
    def reset_password(self, request):
        """Function to verify phone number and reset user password

        Most of the code here is corresponding to the "verify" view already present in the package.

        """
        serializer = PhoneVerifyAndResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone = serializer.validated_data.pop('phone_number')
            serializer.validated_data.pop('security_code')
            serializer.validated_data.pop('session_token')
            password = serializer.validated_data.pop('password')

            existed_user = User.objects.filter(phone=phone).first()
            if existed_user:
                # so we are ready to reset password
                existed_user.set_password(password)
                # save changes to database by calling save() method
                existed_user.save()
            else:
                return Response({"message": "Password reset failed."}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({'errors': serializer.errors}, status=HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Password reset successful."}, status=HTTP_200_OK)
