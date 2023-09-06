from rest_framework import serializers
from .models import Note


class EntriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
