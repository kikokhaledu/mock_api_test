# FastAPI Mock API for React Application

This mock API is designed for testing a React application it provied a CLI to choose form the responses.

## Setup

To set up and run the mock API, follow these steps:

1. Install FastAPI and Uvicorn using pip:

```bash
pip install -r requirements.txt
```
2. Run the server:

```bash 
python mock_api.py
```
### WebSocket Endpoint

The `/api/v1/run/deploy` WebSocket endpoint sends a series of status updates to the connected client based on the received transaction status:

1. Immediately after the connection is established, it sends a "connected to mock DMS" message.
2. Waits for status from the web app:
    ```json
    {
        "message": {
            "transaction_status": "success",
            "transaction_type": "fund"
        },
        "action": "send-status"
    }
    ```
3. If the `transaction_status` is 'success':
    - After a 10-second delay, it sends a "job-submitted" message.
    - After another 10-second delay, it sends a "deployment-response" message with a success flag and a Gist URL.
    - After another 10-second delay, it sends a "job-is running" message.
    - It then sends 10 "stream response" messages, one every 3 seconds, containing demo stream logs.
    - After all logs have been sent, it sends a "job_completed" message.
4. If the `transaction_status` is 'error':
    - Sends a "deployment-response" message with a success flag set to False and a Gist URL.
5. If the `transaction_status` is 'success_with_error':
    - After a 10-second delay, it sends a "job-submitted" message.
    - After another 10-second delay, it sends a "deployment-response" message with a success flag and a Gist URL.
    - After another 10-second delay, it sends a "job-is running" message.
    - It then sends 2 "stream response" messages, one every 3 seconds, containing demo stream logs.
    - Sends an "error" message with the content `{"action": "error", "message": "this is a demo error message with error code demo301x"}`




### POST /api/v1/run/request-reward

This POST endpoint simulates the process of requesting a reward. When a POST request is sent to `/api/v1/run/request-reward`, you'll be prompted in the console to choose the reward type (Withdraw, Refund) or a mock error response. The response will include a JSON object containing a signature, oracle message, and the chosen reward type or an error message with the corresponding status code.

- Withdraw: Returns a JSON object containing the signature, oracle message, and "withdraw" as the reward type.
- Refund: Returns a JSON object containing the signature, oracle message, and "refund" as the reward type.
- Error - Connection to oracle failed: Returns status code 500 and a JSON object containing an error message.
- Error - The job is still running: Returns status code 102 and a JSON object containing an error message.
- Error - No job deployed to request reward for: Returns status code 404 and a JSON object containing an error message.

 

### POST /run/request-service

When you send a POST request to the `/run/request-service` endpoint, the incoming data is validated against the defined Pydantic models to ensure it matches the expected format. If the incoming data is valid, you'll be prompted in the console to choose the response type among the following options:

- Success
- Success with error
- Error - JSON: cannot unmarshal object into Go
- Error - Unable to obtain public key
- Error - Nunet estimation price is greater than client price
- Error - No peers found with matched specs
- Error - Cannot connect to oracle
- Error - A service is already running; only 1 service is supported at the moment
- Error - Cannot write to database

The response will include a status code and a JSON object based on your choice. If the incoming POST data does not match the expected format, the function will return a 422 Unprocessable Entity status code, along with a JSON object containing detailed error messages for each invalid field.

- Success: Returns status code 200 and a JSON object containing compute provider address, estimated price, signature, and oracle message.
- Success with error: Returns status code 200 and a JSON object containing compute provider address, estimated price, signature, and oracle message. The WebSocket endpoint will send two logs before returning an error message.
- Error responses: Returns an appropriate status code (400, 404, 500, or 503) and a JSON object containing an error message.




### POST /api/v1/run/send-status

When you send a POST request to the `/api/v1/run/send-status` endpoint, you'll be prompted in the console to choose the response type (success or error). The response will include a status code and a JSON object based on your choice.

- Success: Returns status code 200 and a JSON object containing the message "transaction status demotransaction acknowledged".
- Error: Returns status code 400 and a JSON object containing the error message "cannot read payload body".


And when you connect to the Websocket you will get mock responses with time delays  