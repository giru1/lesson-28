from rest_framework import serializers

from users.models import User, Location


class UserListSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = User
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    locations = serializers.SlugRelatedField

    class Meta:
        model = User
        exclude = ['locations']

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop()
        return super().is_valid(raise_exception=raise_exception)


class LocationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
