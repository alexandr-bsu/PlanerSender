from repositories.consumer import ConsumerRepo
from repositories.log import QueueLogRepository

class PlanerService:
    def __init__(self):
        self.consumer = ConsumerRepo()
        self.logs = QueueLogRepository()

    def plan_batch(self, task_id, message, recipients: list[str]):
        for recipient in recipients:
            task = {"task_id": task_id, "message": message, "username": recipient}
            recipient_in_logs = self.logs.client.select('username, state').eq('task_id', task_id).eq('username', recipient).execute().data
            if recipient_in_logs:
               if recipient_in_logs[0]['state'] == 'stopped':
                   queue_id = self.consumer.send(task)
                   self.logs.client.update({'queue_id': queue_id, 'state':'in queue'}).eq('task_id', task_id).eq('username', recipient).execute()
            else:
                queue_id = self.consumer.send(task)
                self.logs.create(task_id, queue_id, recipient)

    def stop_task(self, task_id):
        # После выполнения команды остаются старые невалидные номера из очереди
        logs = self.logs.client.update({'state': 'stopped'}).eq('task_id', task_id).neq('state', 'successful').execute().data
        for log in logs:
            self.consumer.delete(log['queue_id'])
