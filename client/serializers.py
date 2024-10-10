from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# Client Serializer
class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by']

# Project Serializer
class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(queryset=Client.objects.all())
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'created_at', 'created_by']

# Project Create/Update Serializer (if you want different behavior for creating/updating)
class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_name', 'client', 'users']
