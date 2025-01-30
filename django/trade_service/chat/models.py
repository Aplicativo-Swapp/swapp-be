from django.db import models

class Conversation(models.Model):
    """
        A conversation between two or more users.
    """
    participants = models.JSONField()  # Storage of participants' IDs as a JSON list
    # participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation between {self.participants}"
        # return f"Conversation between {', '.join(user.username for user in self.participants.all())}"

class Message(models.Model):
    """
        A message sent in a conversation.
    """
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender_id = models.IntegerField() # Stores the ID of the auth_service user
    # sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User {self.sender_id}: {self.content[:30]}"
