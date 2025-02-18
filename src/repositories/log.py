from src.repositories.repository import SupabaseRepository
from src.config import settings, Mode


def get_table_name():
    return 'test_hraniteli_queue_log' if settings.mode == Mode.TEST else 'hraniteli_queue_log'


class QueueLogRepository(SupabaseRepository):
    def __init__(self):
        super().__init__(table=get_table_name())

    def create(self, task_id: str, queue_id: int, username: str) -> dict:

       return self.client.insert({'task_id': task_id,
                                  'queue_id': queue_id,
                                  'state': 'in queue',
                                  'username': username}).execute().data[0]

    # def create_batch(self, task_id: str, queue_ids: list[int]) -> list[dict]:
    #     logs = []
    #     for queue_id in queue_ids:
    #         log = self.create(task_id, queue_id)
    #         logs.append(log)
    #
    #     return logs

    def find_by_task_id(self, task_id: str) -> list[dict]:
        return self.client.select('*').eq('task_id', task_id).execute().data

    def update_by_task_id(self, task_id: str, payload: dict) -> list[dict]:
        return self.client.update(payload).eq('task_id', task_id).execute().data

    def delete_by_task_id(self, task_id: str) -> list[dict]:
        return self.client.delete().eq('task_id', task_id).execute().data

    def find_by_queue_id(self, queue_id: int) -> list[dict]:
        return self.client.select('*').eq('queue_id', queue_id).execute().data

    def update_by_queue_id(self, queue_id: int, payload: dict) -> list[dict]:
        return self.client.update(payload).eq('queue_id', queue_id).execute().data

    def delete_by_queue_id(self, queue_id: int) -> list[dict]:
        return self.client.delete().eq('queue_id', queue_id).execute().data

    def find_by_username(self, username: str) -> list[dict]:
        return self.client.select('*').eq('username', username).execute().data

    def update_by_username(self, username: str, payload: dict) -> list[dict]:
        return self.client.update(payload).eq('username', username).execute().data

    def delete_by_username(self, username: str) -> list[dict]:
        return self.client.delete().eq('username', username).execute().data


