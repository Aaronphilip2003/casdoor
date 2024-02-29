from fastapi import FastAPI, HTTPException
import httpx
import json
from models import User

app = FastAPI()

# Casdoor API information
CASDOOR_URL = "http://localhost:8000"
CLIENT_ID = "ace744d845dd5353b265"
CLIENT_SECRET = "cf59a286e59e2f68fc31b7fb6617a29b5fedc123"
ORGANIZATION_NAME = "your-organization"

def construct_request_url(endpoint: str) -> str:
    return f"{CASDOOR_URL}/api/{endpoint}?clientId={CLIENT_ID}&clientSecret={CLIENT_SECRET}&owner={ORGANIZATION_NAME}"


# Endpoint to get users from Casdoor
@app.get("/users/")
async def get_users():
    async with httpx.AsyncClient() as client:
        # Construct the request URL for getting users
        request_url = f"{CASDOOR_URL}/api/get-users?clientId={CLIENT_ID}&clientSecret={CLIENT_SECRET}&owner={ORGANIZATION_NAME}"
        

        # Make the request
        response = await client.get(request_url, timeout=30)
        print(request_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Attempt to decode the JSON response
            try:
                return response.json()
            except json.decoder.JSONDecodeError:
                # The response was not valid JSON
                raise HTTPException(status_code=500, detail="Invalid JSON response received")
        else:
            # The request failed; provide details based on the response status code
            error_detail = "Failed to retrieve users from Casdoor"
            try:
                # Attempt to include error details from the response if it's JSON
                error_info = response.json()
                error_detail += f": {error_info.get('detail', 'No additional error info')}"
            except json.decoder.JSONDecodeError:
                # Fallback if the error response is also not valid JSON
                error_detail += ": The error response was not in JSON format."
            raise HTTPException(status_code=response.status_code, detail=error_detail)

@app.post("/add-user/")
async def add_user(user: User):
    async with httpx.AsyncClient() as client:
        # Construct the request URL for adding a user
        request_url = construct_request_url("add-user")

        # Prepare the request data, converting the Pydantic model to a dictionary
        request_data = user.dict()

        # Include additional authentication or header parameters as required by your Casdoor setup
        headers = {
            "Content-Type": "application/json",
            # Include other headers or authentication tokens as needed
        }

        # Make the POST request
        response = await client.post(request_url, json=request_data, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Return the response from Casdoor
            return response.json()
        else:
            # Something went wrong, raise an HTTPException with the status code and detail
            error_detail = "Failed to add user to Casdoor"
            try:
                # Attempt to include error details from the response if it's JSON
                error_info = response.json()
                error_detail += f": {error_info.get('detail', 'No additional error info')}"
            except json.decoder.JSONDecodeError:
                # Fallback if the error response is also not valid JSON
                error_detail += ": The error response was not in JSON format."
            raise HTTPException(
                status_code=response.status_code, detail=error_detail)