from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter

User = get_user_model()

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """ Ensure users can only see their own conversations """
        return Conversation.objects.filter(participants__in=[self.request.user])

    def create(self, request, *args, **kwargs):
        """ Custom create method for new conversations """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['sent_at']
    filterset_class = MessageFilter
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination

    def get_queryset(self):
        """ Ensure users can retrieve messages they sent or received """
        conversation_id = self.kwargs.get('conversation_pk')  # Get conversation ID from URL
        if not conversation_id:
            return Response({"error": "Conversation ID is required"}, status=status.HTTP_403_FORBIDDEN)

        return Message.objects.filter(conversation__participants__in=[self.request.user])

    def create(self, request, *args, **kwargs):
        """ Custom create method for sending messages """
        conversation_id = self.kwargs.get('conversation_pk')
        if not conversation_id:
            return Response({"error": "Conversation ID is required"}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)