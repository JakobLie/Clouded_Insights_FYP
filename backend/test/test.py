import os
import time
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis

load_dotenv()

# SQL Alchemy Setup
engine = create_engine(os.environ.get("DATABASE_URL"), pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Redis Consumer Setup
REDIS_URL = os.environ.get("REDIS_URL").split(":")
REDIS_TOPIC = os.environ.get("REDIS_TOPIC")
r = redis.Redis(host=REDIS_URL[0], port=REDIS_URL[1])
consumer = r.pubsub()

# App Functionality
def runConsumer():
    try:
        consumer.subscribe(REDIS_TOPIC)
        while True:
            message = consumer.get_message(timeout=1.0) # Polls for new messages at interval of 1 second
            if message == None:
                continue
            if message['type'] == 'subscribe': # Indicates successful subscription
                print(f" * Subscribed to Redis topic successfully:", message['channel'].decode(), 
                        "\n * Listening for messages...")
                continue
            print(" * Received message:", message)
            if message['type'] == 'message':
                processMessage(message['data'].decode())
            time.sleep(0.1) # Apparently avoids some error
    except KeyboardInterrupt:
        print(" * Service interrupted manually by user")
    finally:
        consumer.unsubscribe()
        

# Business Logic
def processMessage(message):
    print(" * Processing message:", message)
    session = SessionLocal()
    pass
    # try:
    #     # Your DB logic here
    #     # e.g., session.add(some_model_instance)
    #     session.commit()
    # except Exception:
    #     session.rollback()
    #     raise
    # finally:
    #     session.close()

if __name__ == '__main__':
    print("Test service running:" + os.path.basename(__file__) + "...")
    runConsumer()