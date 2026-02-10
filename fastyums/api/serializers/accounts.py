from rest_framework import serializers
from accounts.models import User, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'address_id', 'name', 'street',
            'city', 'state', 'country',
            'is_default', 'created_at',
            'updated_at'
        ]
        read_only_fields = ['address_id']


class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)
    password = serializers.CharField(
        write_only=True,
        style={'input_type': "password"}
    )
    password2 = serializers.CharField(
        write_only=True,
        style={'input_type': "password"}
    )

    class Meta:
        model = User
        fields = [
            'user_id', 'email', 'username',
            'password', 'password2',
            'first_name', 'last_name', 'phone',
            'role', 'addresses', 'vendors', 'payments'
        ]
        read_only_fields = ['user_id', 'addresses', 'payments']

    def validate(self, attrs):
        """Validates that passwords match."""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': "Passwords do not match."
            })
        return attrs

    def create(self, validated_data):
        """Create a <User> instance and sets password."""
        password = validated_data.pop('password')
        validated_data.pop('password2')

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
