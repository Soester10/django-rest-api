from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError

from .models import DataModel, Tag


UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"

        def create(self, clean_data):
            user_obj = UserModel.objects.create_user(
                email=clean_data["email"],
                password=clean_data["password"],
                username=clean_data["username"],
            )
            # user_obj.username = clean_data["username"]
            user_obj.set_password(clean_data["password"])
            user_obj.save()
            return user_obj


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, clean_data):
        user = authenticate(
            username=clean_data["username"], password=clean_data["password"]
        )
        if not (user):
            raise ValidationError("User Not Found!")
        return user


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)


class DataSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = DataModel
        fields = ("SKU", "name", "category", "tags", "stock_status", "available_stock")

    # map and save each tag
    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        data_instance = DataModel.objects.create(**validated_data)

        for tag_data in tags_data:
            tag_name = tag_data.get("name")
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            data_instance.tags.add(tag)

        return data_instance
