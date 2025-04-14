from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status, generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import UpdateUserInfoSerializer, UserSerializer, RegisterSerializer, CustomTokenObtainPairSerializer



User = get_user_model()
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "succeeded": True,
                "message": "Registration successful.",
                "user": self.get_serializer(user).data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            "succeeded": False,
            "message": "Registration failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated , )

    def get_object(self):
      return self.request.user
    



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



@api_view(['PATCH'])
def update_user_info(request):
    try:
        user = request.user

        # Serialize the data and update the user info
        serializer = UpdateUserInfoSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "succeeded": True,
                "message": "User information updated successfully.",
                "user": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "succeeded": False,
                "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({
            "succeeded": False,
            "message": str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
