from places.models import Place,Category,Review,Media
from rest_framework import serializers


class  PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ("id", "user", "name","is_active","coordinates",
                  "category","has_wifi","telephone","description","likes")


class  CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class  ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("id", "user", "place","comment","vote")


class  MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ("id", "place","image")
