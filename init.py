from fastapi import FastAPI, HTTPException
import base_models, gemini, scrap
import uvicorn

app = FastAPI()

@app.post("/parse")
async def parse_user_text_endpoint(user_input: base_models.UserTextInput):
    try:
        parsed_info = gemini.get_parsed_input(user_input.text)
        print(parsed_info)
        flights = scrap.get_flight_info(json_data=parsed_info)
        print(flights)
        response = gemini.parse_flight_info(flights)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    
    uvicorn.run("init:app", host = "127.0.0.1", port = 8000, reload = True)
