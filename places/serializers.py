from rest_framework.fields import SerializerMethodField

from places.models import Place,Category,Review,Media
from rest_framework import serializers


class  PlaceSerializer(serializers.ModelSerializer):
    category=SerializerMethodField()
    class Meta:
        model = Place
        fields = ("id", "user", "name","is_active","coordinates",
                  "category","has_wifi","telephone","description","likes")


    def get_category(self, obj):
        return str(obj.category.name)


class  CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class  ReviewSerializer(serializers.ModelSerializer):
    user = SerializerMethodField()
    place = SerializerMethodField()
    class Meta:
        model = Review
        fields = ("id", "user", "place","comment","vote")

    def get_user(self, obj):
        return str(obj.user.username)


    def get_place(self, obj):
        return str(obj.place.name)


class  MediaSerializer(serializers.ModelSerializer):
    place = SerializerMethodField()
    class Meta:
        model = Media
        fields = ("id", "place","image")

    def get_place(self, obj):
        return str(obj.place.name)