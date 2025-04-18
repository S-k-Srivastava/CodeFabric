import json
from typing import Any, Type

from pydantic import BaseModel
from modules.core.utils.data_conversion import serialize_data,deserialize_data
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

class MyRedisMemory:
    def __init__(self, process_id: str):
        self.process_id = process_id
        r.hset(f"process_id:{process_id}", "id", process_id)
    
    def delete(self):
        r.delete(f"process_id:{self.process_id}")

    def get_memory(self, scope: str) -> 'ScopedMemory':
        return ScopedMemory(self.process_id, scope)
    
    def save(self) -> None:
        r.save()

class ScopedMemory(MyRedisMemory):
    def __init__(self, id: str, scope: str):
        super().__init__(id)
        self.scope = scope

    def add(self, key: str, value: Any) -> None:
        data = serialize_data(value)
        r.hset(f"process_id:{self.process_id}:{self.scope}", key, data)

    def get(self, key: str) -> Any:
        value = r.hget(f"process_id:{self.process_id}:{self.scope}", key)
        if value is None:
            return None
        data = deserialize_data(json.dumps(json.loads(value)))
        return data
    
    def delete(self, key: str) -> None:
        r.hdel(f"process_id:{self.process_id}:{self.scope}", key)
    
    def save(self) -> None:
        r.save()


class Input(BaseModel):
    title: str
    description: str
    multiline: bool
    
REQUEST_CHANNEL = "input_requests"
RESPONSE_CHANNEL = "input_responses"

class InputHanlder():
    def __init__(self, process_id: str):
        self.process_id = process_id
        self.pubsub = r.pubsub()
        self.pubsub.subscribe(RESPONSE_CHANNEL)

    def request_input(self, inputs: list[Input]) -> str:
        inputs = [serialize_data(input) for input in inputs]
        
        # Publish Input Request
        r.publish(REQUEST_CHANNEL, json.dumps(inputs))
        
        # Listen for Input Response
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                datas = json.loads(message['data'])
                return datas

        