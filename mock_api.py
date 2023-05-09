from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import Optional,List, Dict, Any
import uvicorn
from fastapi.responses import JSONResponse


app = FastAPI()

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
    machine_type: str
    params: Params
    constraints: Constraints

class RequestServiceData(BaseModel):
    compute_provider_addr: str
    estimated_price: float
    signature: str
    oracle_message: str

class ErrorResponse(BaseModel):
    error: str

@app.post(
    "/request-service",
    response_model=Optional[RequestServiceData],
    responses={404: {"model": ErrorResponse}, 503: {"model": ErrorResponse}},
)
async def request_service(request_data: RequestData):
    """
    Handle the POST request to /request-service, simulating a mock API for testing.

    This function receives the incoming POST data in the form of a RequestData object,
    which contains the address_user, max_ntx, blockchain, service_type, machine_type,
    params, and constraints fields. The data is validated against the defined Pydantic
    models, ensuring that the POST data matches the expected format.

    Upon receiving the request data, the function prompts the user to choose one of
    three response types:

    1. Success
    2. No peers error
    3. Oracle issue error
    
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
        }

    def no_peers_error():
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": "no peers"})

    def oracle_issue_error():
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"error": "oracle issue"})

    choice_map = {
        "1": success_response,
        "2": no_peers_error,
        "3": oracle_issue_error,
    }

    print("\nReceived request data:")
    print(request_data)
    print("\n" + "-" * 50 + "\n")  #separator
    print("\nChoose response type:")
    print("1. Success")
    print("2. No peers error")
    print("3. Oracle issue error")
    choice = input("Enter the number corresponding to your choice: ")

    response_func = choice_map.get(choice)

    if response_func:
        return response_func()
    else:
        print("Invalid choice. Please try again.")
        return await request_service(request_data)


    
    
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=9999)
