import google.generativeai as genai
import json, time

GOOGLE_API_KEY= "AIzaSyCsFvTtCmtaq71o6F_N60MMGeANx3Twpzk"

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

# function to parse input text into JSON format
def get_parsed_input(text):
  systemPrompt = "Given user text input, your task is to extract relevant travel information such as the trip_type (one-way or round), travel_date, return_date, origin, destination, travel_class (Economy, Business or First) and number_of_passengers, and formats it into JSON. \
      Convert origin and desatination into city abbrevations if they are not. \
      If any information is not given, initialize it as None in JSON. \
      You should understand natural language inputs and accurately identify the required details.\
      Dates should be parsed and formatted in the YYYY-MM-DD format."
  prompt = f"{systemPrompt}. User input is : {text}"
  max_retries = 3
  while max_retries != 0:
    # Include instructions within the query
    try:
      response = model.generate_content(prompt)
      time.sleep(2)
      json_string = response.text
      json_string = json_string.split("JSON")[1].replace("```","")
      json_data = json.loads(json_string)
      # If the JSON is empty, retry
      if not json_data:
        max_retries -= 1
      # If the JSON is not empty, break
      else:
        break
    except:
      pass

  return json_data

# function to parse scraped data from web into readable format
def parse_flight_info(flights_data):
  systemPrompt = "Given a list of flight details, your task is to converts the list into a human-readable format.\
      Each element in the list represents details of a flight, including airline, departure time, departure airport, arrival time, arrival airport, duration, price, and additional information. \
      Details may also be of round trip flights. \
    You should parse each element and format the flight information into a clear and understandable format."
  prompt = f"{systemPrompt}. This is list of flight details : {flights_data}"
  response = model.generate_content(prompt)
  formatted_response = response.text
  return formatted_response