from rest_framework import serializers
from home.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = User
    fields=['email', 'name', 'password', 'password2','profile']
    extra_kwargs={
      'password':{'write_only':True}
    }
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    name = attrs.get('name')

    if len(password)<=4:
      raise serializers.ValidationError("password must contain atleast 5 characters")
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    if len(name)<=4:
      raise serializers.ValidationError("name must contain atleast 5 characters")
    
    return attrs
  def create(self, validate_data):
    return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'name','profile']

class ProfileCrudSerializer(serializers.ModelSerializer):
  email = serializers.ReadOnlyField()
  profile = serializers.ImageField(required = False)
  # email = serializers.EmailField(read_only = True)
  class Meta:
    model = User
    fields = ['id', 'email', 'name','profile']