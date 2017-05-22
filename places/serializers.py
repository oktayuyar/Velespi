from places.models import Place
from rest_framework import serializers


class  PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ("id", "user", "name","is_active","coordinates",
                  "category","has_wifi","telephone","description","likes")