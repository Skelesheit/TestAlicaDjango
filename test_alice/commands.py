from asgiref.sync import sync_to_async

from test_alice.models import Session, ChatHistory


@sync_to_async
def close_session(session: Session) -> None:
    session.close()


@sync_to_async
def delete_session(session: Session) -> None:
    session.delete()


@sync_to_async
def get_messages_from_session(session) -> list[ChatHistory]:
    return list(ChatHistory.objects.filter(session=session))


@sync_to_async
def get_or_create_session(user_id: str) -> Session:
    session, _created =  Session.objects.get_or_create(user_id=user_id, is_open=True)
    return session


@sync_to_async
def write_message(session: Session, message: str, role: str) -> None:
    print("Тип session:", type(session))
    ChatHistory.objects.create(message=message, session=session, role=role)

@sync_to_async
def check_session(user_id: str) -> bool:
    return Session.objects.filter(is_open=True, user_id=user_id).exists()
