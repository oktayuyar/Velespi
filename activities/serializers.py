from activities.models import Activity,Review,Media,Category
from rest_framework import serializers
import activities

class  ActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = ("id", "user", "name","route","description",
                  "is_active","category","telephone","likes")


class  CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class  ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("id", "user", "activity","comment")


class  MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ("id", "activity","image")
