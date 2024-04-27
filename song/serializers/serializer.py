from rest_framework import serializers
from song.models import *


# User serializer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

# Song serializer
class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = "__all__"

# playlist serializer
class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = "__all__"
