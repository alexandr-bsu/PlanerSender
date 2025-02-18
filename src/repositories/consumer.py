from src.config import client, settings

class ConsumerRepo:
    def __init__(self):
        self.client = client.schema('pgmq_public')
        self.queue_name = settings.db.QUEUE_NAME

    def pop(self) -> dict | None:
        result = self.client.rpc('pop', {'queue_name': self.queue_name}).execute().data
        return result if result else None

    def send(self, payload: dict, sleep_seconds: int = 0) -> int:
        return self.client.rpc('send',
                          {'queue_name': self.queue_name,
                           'message': payload,
                           'sleep_seconds': sleep_seconds}).execute().data[0]

    def send_batch(self, list_payloads: list[dict], sleep_seconds: int = 0) -> list[int]:
        return self.client.rpc('send_batch',
                          {'queue_name': self.queue_name,
                           'messages': list_payloads,
                           'sleep_seconds': sleep_seconds}).execute().data

    def archive(self, message_id) -> bool:
        return self.client.rpc('archive', {'queue_name': self.queue_name, 'message_id': message_id}).execute().data

    def delete(self, message_id) -> bool:
        return self.client.rpc('delete', {'queue_name': self.queue_name, 'message_id': message_id}).execute().data

    def read(self, sleep_seconds=0, n=0) -> list[dict]:
        result = self.client.rpc('read', {'queue_name': self.queue_name,
                                    'sleep_seconds': sleep_seconds,
                                    'n': n}).execute().data
        return result


