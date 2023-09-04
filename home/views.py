from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
 
# from rest_framework.generics import CreateAPIView
from home.serializer import  UserLoginSerializer, UserProfileSerializer, UserRegistrationSerializer,ProfileCrudSerializer
from django.contrib.auth import authenticate
from home.renderer import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import User

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  # email = user.email
  # id = user.id
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token)
    #   'email':email
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    print(request.FILES,'ffffffffff')
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        profile = serializer.validated_data.get('profile')
        print(profile)
        serializer.save()
        # User.objects.create(
        #   email = serializer.validated_data.get('email'),
        #   name = serializer.validated_data.get('name'),
        #   password = serializer.validated_data.get('password'),
        #   profile = serializer.validated_data.get('profile')
        # )
        return Response({'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
          token = get_tokens_for_user(user)
          return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
        else:
          return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileCrud(APIView):
  permission_classes=[IsAdminUser]
  def get(self,request):
    users = User.objects.all()
    serializer = ProfileCrudSerializer(users,many=True)
    return Response(serializer.data)
  
  def put(self,request,pk=None):
    id = pk 
    print('heloooo',pk)
    if id is not None:
      user = User.objects.get(pk=id)
      serilaizer = ProfileCrudSerializer(user,request.data,partial=True)
      if serilaizer.is_valid():
        serilaizer.save()
        return Response(serilaizer.data,status=status.HTTP_200_OK)
      return Response(serilaizer.errors,status=status.HTTP_400_BAD_REQUEST)


# class InvalidUrl(APIView):
@api_view(['GET','POST','PUT','PATCH','DELETE'])
def InvalidUrl(request, *args, **kwargs):
    return Response({"error": "Invalid URL path"}, status=status.HTTP_404_NOT_FOUND)


