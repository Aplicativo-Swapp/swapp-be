from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Conversation, Message

User = get_user_model()

class ChatTests(TestCase):
    def setUp(self):
        """
            Setup runs before every test case.
        """
        self.client = APIClient()

        # Creating test users
        self.user1 = User.objects.create_user(username="user1", password="testpass123")
        self.user2 = User.objects.create_user(username="user2", password="testpass123")
        self.user3 = User.objects.create_user(username="user3", password="testpass123")  # Usuário sem conversa

        # Authenticating user1 by default
        self.client.force_authenticate(user=self.user1)

        # Creating a conversation between the users
        self.conversation = Conversation.objects.create()
        self.conversation.participants.set([self.user1, self.user2])
        self.conversation.save()

    def test_create_conversation(self):
        """
            Test the creation of a new conversation between users.
        """
        response = self.client.post("/conversations/", {"participants": [self.user2.id]}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)

    # def test_create_conversation_invalid_user(self):
    #     """
    #     Test error when creating a conversation with an invalid user ID.
    #     """
    #     response = self.client.post("/conversations/", {"participants": [999]}, format="json")  # Usuário inexistente
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn("error", response.data)

    # def test_get_conversations(self):
    #     """
    #     Test the listing of conversations for the authenticated user.
    #     """
    #     response = self.client.get("/conversations/")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)  # Deve conter pelo menos a conversa inicial

    # def test_send_message(self):
    #     """
    #     Test the sending of a message in a conversation.
    #     """
    #     response = self.client.post(
    #         f"/conversations/{self.conversation.id}/messages/",
    #         {"content": "Hello, this is a test message."},
    #         format="json",
    #     )

    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertIn("content", response.data)
    #     self.assertEqual(response.data["content"], "Hello, this is a test message.")

    # def test_send_message_without_content(self):
    #     """
    #     Test error when sending a message without content.
    #     """
    #     response = self.client.post(f"/conversations/{self.conversation.id}/messages/", {}, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn("error", response.data)

    # def test_get_messages(self):
    #     """
    #     Test the retrieval of messages from a conversation.
    #     """
    #     # Creating a message before the test
    #     Message.objects.create(conversation=self.conversation, sender=self.user1, content="Test message")

    #     response = self.client.get(f"/conversations/{self.conversation.id}/messages/")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)
    #     self.assertEqual(response.data[0]["content"], "Test message")

    # def test_get_messages_unauthorized_user(self):
    #     """
    #     Test that a user who is not part of a conversation cannot access its messages.
    #     """
    #     self.client.force_authenticate(user=self.user3)  # Autenticar como user3 (não está na conversa)
    #     response = self.client.get(f"/conversations/{self.conversation.id}/messages/")
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertIn("error", response.data)

    # def test_get_messages_invalid_conversation(self):
    #     """
    #     Test error when retrieving messages from a non-existing conversation.
    #     """
    #     response = self.client.get("/conversations/999/messages/")  # ID inexistente
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertIn("error", response.data)

    # def test_send_message_invalid_conversation(self):
    #     """
    #     Test error when sending a message to a non-existing conversation.
    #     """
    #     response = self.client.post(
    #         "/conversations/999/messages/",
    #         {"content": "This should not work."},
    #         format="json",
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    #     self.assertIn("error", response.data)
