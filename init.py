from fastapi import FastAPI, HTTPException
import base_models, gemini, scrap
import uvicorn

app = FastAPI()

@app.post("/parse")
async def parse_user_text_endpoint(user_input: base_models.UserTextInput):

    # Parse given text input into JSON using AI model
    parsed_info = gemini.get_parsed_input(user_input.text)
    print(parsed_info)

    # Scrap flights information from internet
    flights = scrap.get_flight_info(json_data=parsed_info)
    print(flights)
    if flights:
        response = gemini.parse_flight_info(flights)
        print(response)
        return response
    else:
        raise HTTPException(status_code=404, detail="No flights found")
    


if __name__ == "__main__":
    
    uvicorn.run("init:app", host = "127.0.0.1", port = 8000, reload = True)
