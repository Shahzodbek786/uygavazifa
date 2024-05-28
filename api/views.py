from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from app_main.models import Note
from .serializers import NoteSerializer, UserSerializer
from .permissions import IsSelfOrReadOnly, IsOwner

User = get_user_model()

class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(owner=request.user)
        serializer = NoteSerializer(instance=queryset, many=True)
        return Response(serializer.data)

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSelfOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        if self.get_object() == self.request.user:
            serializer.save()

    def perform_destroy(self, instance):
        if instance == self.request.user:
            instance.delete()
