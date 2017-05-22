from activities.models import Activity
from rest_framework import serializers


class  PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ("id", "user", "name","route","description",
                  "is_active","category","telephone","likes")