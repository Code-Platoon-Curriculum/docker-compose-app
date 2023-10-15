import requests
from rest_framework import serializers
from .models import Wine
from django.conf import settings



def get_thumbnail_url(photo_id):
    print("in get_thumbnail_url")
    key = settings.MY_API_KEY
    url = settings.MY_PHOTO_URL
    base_url = f"{url}/{photo_id}"
    response = requests.get(base_url, headers={"Authorization": f"Token {key}"})
    response_json = response.json()
    return response_json["thumbnailUrl"]


class WineSerializer(serializers.Serializer):
    wine_name = serializers.CharField(max_length=120)
    price = serializers.CharField()
    varietal = serializers.CharField()
    description = serializers.CharField()
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    img_url = serializers.URLField(read_only=True)

    def create(self, validated_data):
        # This method becomes more convoluted since the url is dependent on the
        # id, which we can only get once it's saved to the db.
        Wine.objects.create(**validated_data)
        wine = Wine.objects.get(wine_name=validated_data["wine_name"])
        url = get_thumbnail_url(wine.id)
        wine.img_url = url
        wine.save()
        return Wine.objects.get(id=wine.id)


    def update(self, instance, validated_data):
        instance.wine_name = validated_data.get('wine_name', instance.wine_name)
        instance.price = validated_data.get('price', instance.price)
        instance.varietal = validated_data.get('varietal', instance.varietal)
        instance.id = validated_data.get('id', instance.id)
        instance.description = validated_data.get('description', instance.description)
        instance.img_url = validated_data.get("img_url", instance.img_url)
        instance.save()
        return instance
