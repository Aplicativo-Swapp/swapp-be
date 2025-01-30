from rest_framework import serializers
from .models import Conversation, Message
from .auth_client import get_user_details

class MessageSerializer(serializers.ModelSerializer):
    """
        Serializer for the Message model
    """
    sender_details = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ["id", "conversation", "sender_id", "sender_details", "content", "timestamp"]
        read_only_fields = ["id", "timestamp"]

    def get_sender_details(self, obj):
        """Obtém informações do usuário pelo auth_service"""
        return get_user_details(obj.sender_id)  # Retorna {'id': 1, 'name': 'John Doe', ...}

class ConversationSerializer(serializers.ModelSerializer):
    """
        Serializer for the Conversation model
    """
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ["id", "participants", "messages", "created_at"]
