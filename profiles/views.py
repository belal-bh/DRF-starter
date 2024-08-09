# forms
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .serializers import ProfileSerializer

@login_required
@api_view(['GET'])
def get_user_profile(request):
    return JsonResponse(ProfileSerializer(request.user.profile).data, safe=False)
