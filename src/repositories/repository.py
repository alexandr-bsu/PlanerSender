from config import settings
from supabase import Client

class SupabaseRepository:
    def __init__(self, table: str, schema: str = 'public'):
        self.client = Client(supabase_url=settings.db.DB_HOST, supabase_key=settings.db.DB_SECRET_KEY).schema(schema).table(table)

    def create(self, payload: dict):
        return self.client.insert(payload).execute().data[0]

    def create_batch(self, payload: list[dict]):
        results = []
        for p in payload:
            result =  self.create(p)
            results.append(result)

        return results

    def find(self, id) -> dict | None:
        result = self.client.select('*').eq('id', id).execute().data
        if not result:
            return

        return result[0]

    def update(self, id, payload) -> dict | None :
        result = self.client.update(payload).eq('id', id).execute().data
        if not result:
            return

        return result[0]

    def delete(self, id) -> dict | None:
        result = self.client.delete().eq('id', id).execute().data
        if not result:
            return

        return result


