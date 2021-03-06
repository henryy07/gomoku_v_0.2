"""Serializers handling User and UserProfile objects"""
import re
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from gomoku_app.api.serializers import GomokuRecordSerializer
from core import models


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users objects"""

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        required=True,
        help_text="password needs to be at least 8 ",
        style={"input_type": "password", "placeholder": "Password"},
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=get_user_model().objects.all(),
                message="That email address is already taken.",
            )
        ]
    )
    users_games = serializers.SerializerMethodField("paginated_users_games")

    class Meta:
        """Defining model and fields for serializer"""
        model = get_user_model()
        fields = ("id", "username", "email", "first_name", "password", "users_games")

    def create(self, validated_data):
        """create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def paginated_users_games(self, obj):
        """method to get paginated results from serializer"""
        try:
            page_size = self.context["request"].query_params.get("size") or 20
            paginator = Paginator(obj.users_games.all(), page_size)
            page = self.context["request"].query_params.get("page") or 1
            words_in_book = paginator.page(page)
            serializer = GomokuRecordSerializer(words_in_book, many=True)
            return serializer.data
        except EmptyPage:
            raise serializers.ValidationError("no further content")


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for the profile objects"""

    class Meta:
        """Defining model and fields for serializer"""
        model = models.UserProfile
        fields = ("id", "user", "picture")
        read_only_fields = ("id",)

    def validate(self, attrs):
        """picture image validation"""
        # allowed_formats = ("jpg", "jpeg", "gif")
        regex = r"([.]jpg$)|([.]jpeg$)|([.]gif$)"
        pic = str(attrs["picture"])
        pic_check = re.search(regex, pic)
        print(pic_check)
        if pic_check:
            return attrs
        raise serializers.ValidationError(
            "Invalid format of the file, allowed formats: jpg, jpeg, gif"
        )


class UserProfilePictureSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to user profile"""

    class Meta:
        """Defining model and fields for serializer"""
        model = models.UserProfile
        fields = ("id", "picture")
        read_only_fields = ("id",)


# class UserPasswordChangeSerializer(serializers.Serializer):
#     current_password = serializers.CharField(
#         label='Current password',
#         style={'input_type': 'password', 'placeholder': 'Password'})
#     new_password = serializers.CharField(
#         label='New password',
#         style={'input_type': 'password', 'placeholder': 'Password'})
#     re_new_password = serializers.CharField(
#         label='New password',
#         style={'input_type': 'password', 'placeholder': 'Password'})
