from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ChatbotInputSerializer, ChatbotResponseSerializer
from .chatbot_logic import chatbot_response

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ChatbotInputSerializer, ChatbotResponseSerializer
from .chatbot_logic import chatbot_response

@api_view(['POST'])
def chatbot(request):
    serializer = ChatbotInputSerializer(data=request.data)
    if serializer.is_valid():
        message = serializer.validated_data['message']
        response = chatbot_response(message)
        response_serializer = ChatbotResponseSerializer(data={'response': response})
        if response_serializer.is_valid():
            return Response(response_serializer.data)
    return Response(serializer.errors, status=400)



