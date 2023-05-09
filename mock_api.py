from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import Optional
import uvicorn
from fastapi.responses import JSONResponse


app = FastAPI()

class RequestServiceData(BaseModel):
    compute_provider_addr: str
    estimated_price: float
    signature: str
    oracle_message: str

class ErrorResponse(BaseModel):
    error: str

@app.post("/request-service", response_model=Optional[RequestServiceData], responses={404: {"model": ErrorResponse}, 503: {"model": ErrorResponse}})
async def request_service():
    """
    Handles POST requests for the /request-service endpoint.

    This function allows the user to choose a response type for the API in the console:
        1. Success - Returns status code 200 and a JSON object containing compute provider address, estimated price, signature, and oracle message.
        2. No peers error - Returns status code 404 and a JSON object containing an error message.
        3. Oracle issue error - Returns status code 503 and a JSON object containing an error message.

    Returns:
        tuple: A tuple containing the response JSON object and the corresponding status code.
    """
    print("\nChoose response type:")
    print("1. Success")
    print("2. No peers error")
    print("3. Oracle issue error")
    choice = input("Enter the number corresponding to your choice: ")

    if choice == "1":
        return {
            "compute_provider_addr": "0x0541422b9e05e9f0c0c9b393313279aada6eabb2",
            "estimated_price": 0.027280000000000002,
            "signature": "36f68dff290d978d132ef7742ee94c559852207e9b7d4640aef5c92548b57e8cd41776cb84d456e19da7b6f21094015953088437010bef16957f42d905dc350e",
            "oracle_message": "funding-582043e57f3ae217de5d9404ed07a7658de6c3b2444e533ce1ee2ff94ac5a4941848",
        }
    elif choice == "2":
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"error": "no peers"})
    elif choice == "3":
        return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"error": "oracle issue"})
    else:
        print("Invalid choice. Please try again.")
        return await request_service()
    
    
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=9999)
