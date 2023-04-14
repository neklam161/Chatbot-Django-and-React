from rest_framework import serializers

class ChatbotInputSerializer(serializers.Serializer):
    message = serializers.CharField()

class ChatbotResponseSerializer(serializers.Serializer):
    response = serializers.CharField()
