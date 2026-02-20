from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Movie, Profile, Genre
from .serializers import MovieSerializer, ProfileSerializer, UserAccountSerializer

# 1. Browse Movies
class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

# 2. Manage the different Profiles (Dad, Mom, Kids)
class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return profiles belonging to the logged-in user
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically attach the profile to the current user
        serializer.save(user=self.request.user)

# 3. View/Edit the main User Account
class UserAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserAccountSerializer(request.user)
        return Response(serializer.data)
