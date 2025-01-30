from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .auth_client import get_user_details

class ConversationListCreateView(generics.ListCreateAPIView):
    """
        List all user conversations or create a new conversation.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants__contains=[self.request.user.id])

    def post(self, request, *args, **kwargs):
        """
            Create a new conversation between users.
        """
        participants_ids = request.data.get("participants", [])

        # Check if the user is trying to create a conversation with themselves
        if request.user.id in participants_ids:
            return Response({"error": "You cannot create a conversation with yourself"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if there are at least two participants
        if len(participants_ids) < 2:
            return Response({"error": "At least two participants are required to create a conversation"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate users in auth_service
        valid_users = [get_user_details(user_id) for user_id in participants_ids]
        if None in valid_users:
            return Response({"error": "Invalid participant ID"}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create(participants=participants_ids)
        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)

class MessageListCreateView(generics.ListCreateAPIView):
    """
        List and send messages within a conversation.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs["conversation_id"]
        return Message.objects.filter(conversation_id=conversation_id)

    def post(self, request, *args, **kwargs):
        """
            Send a message in a conversation.   
        """
        conversation = Conversation.objects.get(id=self.kwargs["conversation_id"])

        if request.user.id not in conversation.participants:
            return Response({"error": "You are not a participant in this conversation"}, status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(
            conversation=conversation,
            sender_id=request.user.id,
            content=request.data.get("content"),
        )
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
