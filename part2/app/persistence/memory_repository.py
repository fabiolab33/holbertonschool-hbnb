# app/persistence/memory_repository.py
import uuid
from datetime import datetime

class InMemoryRepository:
    def __init__(self):
        # Diccionario para almacenar objetos {id: obj}
        self.storage = {}

    def create(self, obj):
        # Asignar un ID único
        obj.id = str(uuid.uuid4())
        obj.created_at = datetime.utcnow()
        obj.updated_at = datetime.utcnow()
        self.storage[obj.id] = obj
        return obj

    def get(self, obj_id):
        return self.storage.get(obj_id)

    def list(self):
        return list(self.storage.values())

    def update(self, obj_id, **kwargs):
        obj = self.storage.get(obj_id)
        if not obj:
            return None
        # Actualizar atributos
        for k, v in kwargs.items():
            setattr(obj, k, v)
        obj.updated_at = datetime.utcnow()
        return obj

    def delete(self, obj_id):
        return self.storage.pop(obj_id, None)
