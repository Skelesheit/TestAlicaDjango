from rest_framework import serializers


class InterfacesSerializer(serializers.Serializer):
    screen = serializers.DictField(required=False)
    payments = serializers.DictField(required=False)
    account_linking = serializers.DictField(required=False)


class MetaSerializer(serializers.Serializer):
    locale = serializers.CharField()
    timezone = serializers.CharField()
    client_id = serializers.CharField()
    interfaces = InterfacesSerializer()


class SessionUserSerializer(serializers.Serializer):
    user_id = serializers.CharField()


class ApplicationSerializer(serializers.Serializer):
    application_id = serializers.CharField()


class SessionSerializer(serializers.Serializer):
    message_id = serializers.IntegerField()
    session_id = serializers.CharField()
    skill_id = serializers.CharField()
    user = SessionUserSerializer()
    application = ApplicationSerializer()
    new = serializers.BooleanField()
    user_id = serializers.CharField()


class MarkupSerializer(serializers.Serializer):
    dangerous_context = serializers.BooleanField()


class NluSerializer(serializers.Serializer):
    tokens = serializers.ListField(child=serializers.CharField())
    entities = serializers.ListField(child=serializers.DictField())
    intents = serializers.DictField()


class RequestBlockSerializer(serializers.Serializer):
    command = serializers.CharField(allow_blank=True)
    original_utterance = serializers.CharField(allow_blank=True)
    type = serializers.CharField()
    nlu = NluSerializer()
    markup = MarkupSerializer()


class AliceWebhookSerializer(serializers.Serializer):
    meta = MetaSerializer()
    session = SessionSerializer()
    request = RequestBlockSerializer()
    version = serializers.CharField()


class ResponseContentResponse(serializers.Serializer):
    text = serializers.CharField(default='')
    end_session = serializers.BooleanField(default=False)
    tts = serializers.CharField(required=False)
    buttons = serializers.ListField(child=serializers.DictField(), required=False)


class AliceWebhookResponseSerializer(serializers.Serializer):
    response = ResponseContentResponse()
    version = serializers.CharField(default='v0.1')
    session = serializers.DictField(required=False)
