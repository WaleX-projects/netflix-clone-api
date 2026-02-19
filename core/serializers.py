from rest_framework import serializers
from .models import Movie, Genre, Profile, Watchlist
from django.contrib.auth.models import User

# Existing Serializers
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date', 'genres', 'thumbnail', 'video_file']

# The Account Serializer
class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# The "Netflix Profile" Serializer (for switching viewers)
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'name', 'profile_image', 'is_kids']
