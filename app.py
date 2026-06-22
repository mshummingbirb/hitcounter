import os
import socket
from flask import Flask
from redis import Redis
from redis.exceptions import ConnectionError

app = Flask(__name__)

# Fetch Redis configuration from environment variables (crucial for Kubernetes)
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

# Connect to Redis
redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.route("/")
def index():
    # Get the unique hostname of the container (Pod name in Kubernetes)
    pod_name = socket.gethostname()
    
    try:
        # Increment the hit counter in Redis
        hits = redis_client.incr("hits")
        message = f"Hello World! This page has been BOOPED {hits} times. ¯\_(ツ)_/¯ "
    except ConnectionError:
        message = "Hello World! (Could not connect to Redis database)"

    # Simple HTML structure to display the data clearly
    return f"""
    <html>
        <head><title>Hit Counter</title></head>
        <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 50px;">
            <h1>{message}</h1>
            <p style="color: gray;">Served by Pod: <strong>{pod_name}</strong></p>
        </body>
    </html>
    """

if __name__ == "__main__":
    # Run on port 5000 and allow external connections
    app.run(host="0.0.0.0", port=5000)