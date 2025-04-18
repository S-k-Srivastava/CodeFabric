import json
import time
import threading
from typing import List
import redis
from modules.core.utils.data_conversion import deserialize_data
from modules.implementations.nodejs.team.team import NodeJsTeam
from modules.logging.logger import setup_logger
from modules.core.llms.llms import deep_infra_with_temperature
from modules.core.persistence.my_redis_memory import Input, REQUEST_CHANNEL, RESPONSE_CHANNEL

def render_dynamic_form(inputs: List[Input], redis_conn):
    print("\n--- Human Input Required ---")
    responses = []
    for input_item in inputs:
        if input_item.description:
            print(f"{input_item.description}",end=" ")
        responses.append(input("> "))
    redis_conn.publish(RESPONSE_CHANNEL, json.dumps(responses))
    return responses

def start_team(team: NodeJsTeam):
    import asyncio
    asyncio.run(team.start_working())

def main():
    process_id = input("Enter Process ID: ").strip()
    setup_logger(process_id)

    redis_conn = redis.Redis(host='localhost', port=6379, db=0)
    # redis_conn.flushdb()
    pubsub = redis_conn.pubsub()
    pubsub.subscribe(REQUEST_CHANNEL)

    # Start the team in a background thread
    team = NodeJsTeam(process_id, llm=deep_infra_with_temperature)
    team_thread = threading.Thread(target=start_team, args=(team,), daemon=True)
    team_thread.start()

    print("Listening for input requests on Redis...")
    while True:
        try:
            message = pubsub.get_message()
            if message and message['type'] == 'message':
                inputs_raw = json.loads(message['data'])
                inputs = [deserialize_data(input) for input in inputs_raw]
                render_dynamic_form(inputs, redis_conn)
        except Exception as e:
            print("Error:", e)
        time.sleep(1)

if __name__ == "__main__":
    main()
