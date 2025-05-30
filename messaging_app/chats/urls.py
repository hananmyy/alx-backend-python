from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter  # Import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename="conversations")

# Create nested router for messages within conversations
conversation_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename="conversation-messages")

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversation_router.urls)),  # Include nested routes
]