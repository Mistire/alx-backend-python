from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    sender_full_name = serializers.SerializerMethodField()

    def get_sender_full_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_full_name', 'message_body', 'sent_at']

    def validate_message_body(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Message body cannot be empty or whitespace only.")
        return value

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)


    message_count = serializers.SerializerMethodField()

    def get_message_count(self, obj):
        return obj.messages.count()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages', 'message_count']
