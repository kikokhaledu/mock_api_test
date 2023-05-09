# FastAPI Mock API for React Application

This mock API is designed for testing a React application when the backend is not yet available. It is built using FastAPI and provides a single `/request-service` endpoint that accepts POST requests.

## Setup

To set up and run the mock API, follow these steps:

1. Install FastAPI and Uvicorn using pip:

```bash
pip install fastapi uvicorn
```

2. Create a new Python file (e.g., `mock_api.py`) and paste the provided code.

3. Run the server:

```bash 
python mock_api.py
```


## Usage

When you send a POST request to the `/request-service` endpoint, you'll be prompted in the console to choose the response type (success, no peers error, or oracle issue error). The response will include a status code and a JSON object based on your choice.

- Success: Returns status code 200 and a JSON object containing compute provider address, estimated price, signature, and oracle message.
- No peers error: Returns status code 404 and a JSON object containing an error message.
- Oracle issue error: Returns status code 503 and a JSON object containing an error message.
