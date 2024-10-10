from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer

# Client ViewSet
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

# Project ViewSet
class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        client_id = self.kwargs.get('client_id', None)

        if client_id:
            # Return projects related to a specific client
            client = get_object_or_404(Client, id=client_id)
            return Project.objects.filter(client=client)
        else:
            # Return all projects or projects assigned to the logged-in user
            return Project.objects.all()  # Change this to filter based on user if required

    def perform_create(self, serializer):
        client_id = self.request.data.get('client')  # Extract client ID from the request
        if client_id:
            client = get_object_or_404(Client, id=client_id)
            serializer.save(client=client, created_by=self.request.user)
        else:
            serializer.save(created_by=self.request.user)
