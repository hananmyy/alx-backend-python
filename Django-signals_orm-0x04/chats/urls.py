from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Define main router
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename="conversations")

# Define nested router for messages within conversations
nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename="conversation-messages")

urlpatterns = [
    path('', include(router.urls)),  # Include main router
    path('', include(nested_router.urls)),  # Include nested routes
    path('unread-count/', unread_count, name='unread-count'),
]