import requests
import redis
from rest_framework import serializers
from .models import Wine
from django.conf import settings



def get_thumbnail_url(varietal):
    print("in get_thumbnail_url")
    key = settings.MY_API_KEY
    url = f"https://api.pexels.com/v1/search?query={varietal}&per_page=1"
    response = requests.get(url, headers={"Authorization": key})
    response_json = response.json()
    return response_json["photos"][0]["src"]["medium"]


class WineSerializer(serializers.Serializer):
    wine_name = serializers.CharField(max_length=120)
    price = serializers.CharField()
    varietal = serializers.CharField()
    description = serializers.CharField()
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    img_url = serializers.URLField(read_only=True)
    img_fetch_src = serializers.CharField(read_only=True)

    def create(self, validated_data):
        varietal = "wine " + validated_data["varietal"]
        r = redis.Redis(host="redis", port=6379, decode_responses=True)
        cached_img = r.get(varietal)
        if cached_img:
            validated_data["img_url"] = cached_img
            validated_data["img_fetch_src"] = "from redis cache"
        else:
            img_url = get_thumbnail_url(varietal)
            r.set(varietal, img_url)
            validated_data["img_url"] = img_url
            validated_data["img_fetch_src"] = "from API call"
        return Wine.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.wine_name = validated_data.get('wine_name', instance.wine_name)
        instance.price = validated_data.get('price', instance.price)
        instance.varietal = validated_data.get('varietal', instance.varietal)
        instance.id = validated_data.get('id', instance.id)
        instance.description = validated_data.get('description', instance.description)
        instance.img_url = validated_data.get("img_url", instance.img_url)
        instance.img_fetch_src = validated_data.get("img_fetch_src", instance.img_fetch_src)
        instance.save()
        return instance
