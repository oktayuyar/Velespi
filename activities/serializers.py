from rest_framework import serializers
from rest_framework.fields import SerializerMethodField, CharField

from activities.models import Activity,Review,Media,Category


class  ActivitySerializer(serializers.ModelSerializer):
    category=SerializerMethodField()
    class Meta:
        model = Activity
        fields = ("id", "user", "name","route","description",
                  "is_active","category","telephone","likes")

    def get_category(self,obj):
        return str(obj.category.name)

    def get_user(self, obj):
        return str(obj.user.username)

class  CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class  ReviewSerializer(serializers.ModelSerializer):
    user = SerializerMethodField()
    activity = SerializerMethodField()
    class Meta:
        model = Review
        fields = ("id", "user", "activity","comment")


    def get_user(self, obj):
        return str(obj.user.username)

    def get_activity(self, obj):
        return str(obj.activity.name)

class  MediaSerializer(serializers.ModelSerializer):
    activity = SerializerMethodField()
    class Meta:
        model = Media
        fields = ("id", "activity","image")

    def get_activity(self, obj):
        return str(obj.activity.name)