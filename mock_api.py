from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import Optional,List, Dict, Any
import uvicorn
from fastapi.responses import JSONResponse
import asyncio
from fastapi import WebSocket
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Params(BaseModel):
    image_id: str
    model_url: str
    packages: List[str]

class Constraints(BaseModel):
    CPU: int
    RAM: int
    VRAM: int
    power: int
    complexity: str
    time: int

class RequestData(BaseModel):
    address_user: str
    max_ntx: int
    blockchain: str
    service_type: str
    params: Params
    constraints: Constraints

class RequestServiceData(BaseModel):
    compute_provider_addr: str
    estimated_price: float
    signature: str
    oracle_message: str

class ErrorResponse(BaseModel):
    error: str


class RewardData(BaseModel):
    signature: str
    oracle_message: str
    reward_type: str

class RewardErrorResponse(BaseModel):
    error: str

class MessageResponse(BaseModel):
    message: str


@app.post(
    "/api/v1/run/request-service",
    response_model=Optional[RequestServiceData],
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
    },
)
async def request_service(request_data: RequestData):
    """
    Handle the POST request to /run/request-service, simulating a mock API for testing.

    This function receives the incoming POST data in the form of a RequestData object,
    which contains the address_user, max_ntx, blockchain, service_type, machine_type,
    params, and constraints fields. The data is validated against the defined Pydantic
    models, ensuring that the POST data matches the expected format.

    Upon receiving the request data, the function prompts the user to choose one of
    nine response types:

    1. Success
    2. Error - JSON: cannot unmarshal object into Go
    3. Error - Unable to obtain public key
    4. Error - Nunet estimation price is greater than client price
    5. Error - No peers found with matched specs
    6. Error - Cannot connect to oracle
    7. Error - A service is already running; only 1 service is supported at the moment
    8. Error - Cannot write to database
    9. Success with error

    Depending on the chosen response type, the function will return an HTTP response
    with the appropriate status code and JSON data. If the incoming POST data does not
    match the expected format, the function will return a 422 Unprocessable Entity status
    code, along with a JSON object containing detailed error messages for each invalid
    field.

    The function uses a dictionary to map the user's choice to the corresponding response
    function, making it easier to add, remove or modify response types in the future.

    Args:
    request_data (RequestData): The incoming request data as a RequestData object.

    Returns:
    JSONResponse: A JSON response with the appropriate status code and JSON data.
    """
    def success_response():
        return {
            "compute_provider_addr": "0x0541422b9e05e9f0c0c9b393313279aada6eabb2",
            "estimated_price": 0.027280000000000002,
            "signature": "36f68dff290d978d132ef7742ee94c559852207e9b7d4640aef5c92548b57e8cd41776cb84d456e19da7b6f21094015953088437010bef16957f42d905dc350e",
            "oracle_message": "funding-582043e57f3ae217de5d9404ed07a7658de6c3b2444e533ce1ee2ff94ac5a4941848",
            "transaction_status": "success",
        }

    def success_with_error_response():
        response_data = success_response()
        response_data["transaction_status"] = "success_with_error"
        return response_data

    def error_response(status_code, error_message):
        return JSONResponse(status_code=status_code, content={"error": error_message})

    choice_map = {
        "1": success_response,
        "2": lambda: error_response(status.HTTP_400_BAD_REQUEST, "json: cannot unmarshal object into Go"),
        "3": lambda: error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "unable to obtain public key"),
        "4": lambda: error_response(status.HTTP_400_BAD_REQUEST, "nunet estimation price is greater than client price"),
        "5": lambda: error_response(status.HTTP_404_NOT_FOUND, "no peers found with matched specs"),
        "6": lambda: error_response(status.HTTP_503_SERVICE_UNAVAILABLE, "cannot connect to oracle"),
        "7": lambda: error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "a service is already running; only 1 service is supported at the moment"),
        "8": lambda: error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "cannot write to database"),
        "9": success_with_error_response,
    }

    print("\nReceived request data:")
    print(request_data)
    print("\n" + "-" * 50 + "\n")
    print("\nChoose response type:")
    print("1. Success")
    print("2. Error - JSON: cannot unmarshal object into Go")
    print("3. Error - Unable to obtain public key")
    print("4. Error - Nunet estimation price is greater than client price")
    print("5. Error - No peers found with matched specs")
    print("6. Error - Cannot connect to oracle")
    print("7. Error - A service is already running; only 1 service is supported at the moment")
    print("8. Error - Cannot write to database")
    print("9. Success with error")
    choice = input("Enter the number corresponding to your choice: ")

    response_func = choice_map.get(choice)

    if response_func:
        return response_func()
    else:
        print("Invalid choice. Please try again.")
        return await request_service(request_data)


@app.websocket("/api/v1/run/deploy")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for streaming status updates of a mock job.

    This function sends a series of status updates to the connected client
    in the following sequence:

    1. Immediately after the connection is established, it sends a "connected to mock DMS" message.
    2. Waits for status from the webapp {
                      message: {
                        transaction_status: 'success',
                        transaction_type: 'fund'
                        },
                      action: 'send-status'
                    }
    3. If transaction_status is 'success':
        - After a 10-second delay, it sends a "job-submitted" message.
        - After another 10-second delay, it sends a "deployment-response" message with a success flag and a Gist URL.
        - After another 10-second delay, it sends a "job-is running" message.
        - It then sends 10 "stream response" messages, one every 3 seconds, containing demo stream logs.
    4. If transaction_status is 'error':
        - Sends a "deployment-response" message with a success flag set to False and a Gist URL.
    5. If transaction_status is 'success_with_error':
        - After a 10-second delay, it sends a "job-submitted" message.
        - After another 10-second delay, it sends a "deployment-response" message with a success flag and a Gist URL.
        - After another 10-second delay, it sends a "job-is running" message.
        - It then sends 2 "stream response" messages, one every 3 seconds, containing demo stream logs.
        - Sends an "error" message with the content {"action": "error", "message": "this is a demo error message with error code demo301x"}

    Args:
        websocket (WebSocket): The WebSocket instance for the connection.

    Returns:
        None
    """
    await websocket.accept()
    await websocket.send_json({"action": "connected to mock DMS"})

    webapp_response = await websocket.receive_json()
    transaction_status = webapp_response.get("message", {}).get("transaction_status")
    print('----------------------------------------')
    print(transaction_status)
    print('----------------------------------------')
    if transaction_status == "success":
        await asyncio.sleep(10)
        await websocket.send_json({"action": "job-submitted"})
        await asyncio.sleep(10)
        await websocket.send_json({
            "action": "deployment-response",
            "message": {"success": True, "content": "https://gist.github.com/user/:gistId"}
        })
        await asyncio.sleep(10)
        for i in range(1, 11):
            await asyncio.sleep(3)
            await websocket.send_json({"action": "demo_stream_response", "message": f"Demo stream log {i}"})

        await websocket.send_json({"action": "job_completed"})

    elif transaction_status == "error":
        await websocket.send_json({
            "action": "deployment-response",
            "message": {"success": False, "content": "https://gist.github.com/user/:gistId"}
        })

    elif transaction_status == "success_with_error":
        await asyncio.sleep(10)
        await websocket.send_json({"action": "job-submitted"})
        await asyncio.sleep(10)
        await websocket.send_json({
            "action": "deployment-response",
            "message": {"success": True, "content": "https://gist.github.com/user/:gistId"}
        })
        await asyncio.sleep(10)
        for i in range(1, 3):
            await asyncio.sleep(3)
            await websocket.send_json({"action": "demo_stream_response", "message": f"Demo stream log {i}"})

        await websocket.send_json({"action": "error", "message": "this is a demo error message with error code demo301x"})

        
@app.post(
    "/api/v1/run/request-reward",
    responses={
        503: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def request_reward():
    """
    Handler function for POST requests to '/request-reward' endpoint.
    Displays a menu of response types and returns a JSON response based on the user's choice.

    Returns:
        A JSON response with a signature, oracle_message, and reward_type for a chosen response type.
        If an invalid choice is made, it recursively calls itself until a valid choice is made.
        The response also includes a status code depending on the chosen response type:
        - 200 for successful withdrawal or refund.
        - 500 for an error in connecting to the oracle.
        - 503 for when the job is still running.
        - 404 for when there is no job deployed to request reward for.
    """
    responses = {
        "1": {
            "status": status.HTTP_200_OK,
            "content": {
                "signature": "25a3e1fa95152a0b936999299c62627006fb9d8fda9233e6b78d88cd206a9ea86316cac7729fd356da65812a61f6b3dd4152eb239aaa7a59bbf9a5702ee33209",
                "oracle_message": "withdraw-5820acefd2fd95c34f5a19fb8a304e918533fed977c8cc2d88fc322b7c921c0c172c",
                "reward_type": "withdraw",
            },
        },
        "2": {
            "status": status.HTTP_200_OK,
            "content": {
                "signature": "990a4b1f5eac4a2cefbea95e4678fc2c4f097330942cefc18e5cb9dde42bee7ef0dd085550552d35a99abff1daf4eedea80fc6400e98c74f408928fbb2ea5c01",
                "oracle_message": "withdraw-582095ebcd78b9458e54746f0e2c44bc88d0959a3cdb45143e3ff9571cd527fa0375",
                "reward_type": "refund",
            },
        },
        "3": {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "content": {"error": "connection to oracle failed"},
        },
        "4": {
            "status": status.HTTP_503_SERVICE_UNAVAILABLE,
            "content": {"error": "the job is still running"},
        },
        "5": {
            "status": status.HTTP_404_NOT_FOUND,
            "content": {"error": "no job deployed to request reward for"},
        },
    }

    print("\nChoose response type:")
    print("1. Withdraw")
    print("2. Refund")
    print("3. Error - Connection to oracle failed")
    print("4. Error - The job is still running")
    print("5. Error - No job deployed to request reward for")
    choice = input("Enter the number corresponding to your choice: ")

    if choice in responses:
        response = responses[choice]
        return JSONResponse(status_code=response["status"], content=response["content"])
    else:
        print("Invalid choice. Please try again.")
        return await request_reward()

@app.post(
    "/api/v1/run/send-status",
    response_model=Optional[Dict[str, str]],
    responses={200: {"model": MessageResponse}, 400: {"model": ErrorResponse}},
)
async def send_status():
    """
    Handle the POST request to /api/v1/run/send-status, simulating a mock API for testing.

    This function prompts the user to choose one of two response types:

    1. Success
    2. Error - Cannot read payload body

    Depending on the chosen response type, the function will return an HTTP response
    with the appropriate status code and JSON data.

    Args:
    None

    Returns:
    JSONResponse: A JSON response with the appropriate status code and JSON data.
    """

    def success_response():
        return {"message": "transaction status demo transaction acknowledged"}

    def error_response():
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": "cannot read payload body"})

    choice_map = {
        "1": success_response,
        "2": error_response,
    }

    print("\nChoose response type:")
    print("1. Success")
    print("2. Error - Cannot read payload body")
    choice = input("Enter the number corresponding to your choice: ")

    response_func = choice_map.get(choice)

    if response_func:
        return response_func()
    else:
        print("Invalid choice. Please try again.")
        return await send_status()

    
    
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=9999)
