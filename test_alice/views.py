from rest_framework import viewsets, status
from rest_framework.response import Response
from asgiref.sync import sync_to_async, async_to_sync
from test_alice import serializers

from test_alice.services import AliceGameService
# Create your views here.


class AliceGame(viewsets.ViewSet):
    serializer_class = serializers.AliceWebhookSerializer
    response_serializer_class = serializers.AliceWebhookResponseSerializer
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        utterance = serializer.validated_data["request"]["original_utterance"]
        user_id = serializer.validated_data["session"]["user_id"]
        service = AliceGameService()
        response_llm = async_to_sync(service.get_completion)(user_id, utterance)
        response_data = self.response_serializer_class(data={
            "response": {
                "text": f"{response_llm}",
                "end_session": False,
                "buttons": [
                    {"title": "Выход", "hide": True},
                ]
            },
            "version": "1.0"
        })
        response_data.is_valid(raise_exception=True)
        return Response(data=response_data.data, status=status.HTTP_200_OK)
