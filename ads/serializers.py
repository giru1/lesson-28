from rest_framework import serializers

from ads.models import Ads, Category


class AdsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ads
        fields = '__all__'


class AdsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
