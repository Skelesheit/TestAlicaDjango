from rest_framework import viewsets, status
from rest_framework.response import Response

from test_alice import serializers


# Create your views here.


class AliceWebhookHi(viewsets.ViewSet):
    serializer_class = serializers.AliceWebhookSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        utterance = serializer.validated_data["request"]["original_utterance"]
        print(utterance)
        # is_new = serializer.validated_data['session']['new']
        response_data = serializers.AliceWebhookResponseSerializer(data={
            "response": {
                "text": f"{utterance} - сказала она!",
                "end_session": False,
                "buttons": [
                    {"title": "Начать", "hide": True},
                    {"title": "Выход", "hide": True}
                ]
            },
            "version": "1.0"
        })
        print(response_data)
        response_data.is_valid(raise_exception=True)
        return Response(data=response_data.data, status=status.HTTP_200_OK)
