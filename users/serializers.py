from users.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class UserRegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
	password2 = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = User
		fields = ('email', 'password', 'password2',)
		extra_kwargs = {
			'first_name': {'required': True},
			'last_name': {'required': True}
		}

	def validate(self, attrs):
		if attrs['password'] != attrs['password2']:
			raise serializers.ValidationError({"password": "Password fields didn't match."})
		return attrs

	def create(self, validated_data):
		user = User.objects.create(email=validated_data['email'])
		user.set_password(validated_data['password'])
		user.save()
		return user


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		exclude = ('password',)
