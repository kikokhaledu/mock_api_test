# FastAPI Mock API for React Application

This mock API is designed for testing a React application when the backend is not yet available. It is built using FastAPI and provides a single `/request-service` endpoint that accepts POST requests.

## Setup

To set up and run the mock API, follow these steps:

1. Install FastAPI and Uvicorn using pip:

```bash
pip install fastapi uvicorn websockets
```

2. Create a new Python file (e.g., `mock_api.py`) and paste the provided code.

3. Run the server:

```bash 
python mock_api.py
```

### WebSocket Endpoint

The `/send-status` WebSocket endpoint sends a series of status updates to the connected client:

1. Immediately after the connection is established, it sends a "connected to mock DMS" message.
2. After a 10-second delay, it sends a "job-submitted" message.
3. After another 10-second delay, it sends a "job-is running" message.
4. It then sends 10 "stream response" messages, one every 3 seconds, containing demo stream logs.
5. Finally, after a 15-second delay, it sends a "deployment-response" message with a success flag and a Gist URL.


## Usage

When you send a POST request to the `/request-service` endpoint, the incoming data is validated against the defined Pydantic models to ensure it matches the expected format. If the incoming data is valid, you'll be prompted in the console to choose the response type (success, no peers error, or oracle issue error). The response will include a status code and a JSON object based on your choice. If the incoming POST data does not match the expected format, the function will return a 422 Unprocessable Entity status code, along with a JSON object containing detailed error messages for each invalid field.

- Success: Returns status code 200 and a JSON object containing compute provider address, estimated price, signature, and oracle message.
- No peers error: Returns status code 404 and a JSON object containing an error message.
- Oracle issue error: Returns status code 503 and a JSON object containing an error message.


And when you connect to the Websocket you will get mock responses with time delays  