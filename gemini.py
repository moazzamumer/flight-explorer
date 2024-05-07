import textwrap
import google.generativeai as genai
import textwrap
from markdown2 import Markdown
import json

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

GOOGLE_API_KEY= "AIzaSyCsFvTtCmtaq71o6F_N60MMGeANx3Twpzk"

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')

def get_parsed_input(text):
  systemPrompt = "Given user text input, your task is to create an AI model that extracts relevant travel information such as the date, origin, destination, and number of passengers, and formats it into JSON. \
      The AI should be able to understand natural language inputs and accurately identify the required details.\
      Dates should be parsed and formatted in the YYYY-MM-DD format."
  prompt = f"{systemPrompt}. User input is : {text}"
  max_retries = 3
  while max_retries != 0:
    # Include instructions within the query
    try:
      response = model.generate_content(prompt)
      json_string = response.text
      json_string = json_string.split("JSON")[1].replace("```","")
      json_data = json.loads(json_string)
    except:
      pass

    return json_data


def parse_flight_info(flights_data):
  systemPrompt = "Given a list of flight details, your task is to converts the list into a human-readable format.\
      Each element in the list represents details of a flight, including airline, departure time, departure airport, arrival time, arrival airport, duration, price, and additional information. \
      You should parse each element and format the flight information into a clear and understandable format."
  prompt = f"{systemPrompt}. This is list of flight details : {flights_data}"
  response = model.generate_content(prompt)
  formatted_response = to_markdown(response.text)
  return formatted_response

# l = [
#   "Best\nCheapest\nPakistan International Airlines\n11:00 am\nLHE\nKHI\n5:55 pm\nISB\n6h 55m\n$191\nPakistan International Airlines\nView Deal",
#   "Pakistan International Airlines\n7:00 am\nLHE\nUET, KHI\n5:55 pm\nISB\n10h 55m\n$241\nPakistan International Airlines\nView Deal",
#   "Pakistan International Airlines\n10:00 pm\nLHE\nKHI, KDU\n10:15 am +1\nISB\n12h 15m\nOnly 1 seat left at this price\n$377\nPakistan International Airlines\nView Deal",
#   "Pakistan International Airlines\n5:00 pm\nLHE\nKHI, KDU\n10:15 am +1\nISB\n17h 15m\nOnly 1 seat left at this price\n$377\nPakistan International Airlines\nView Deal",
#   "Pakistan International Airlines\n10:00 pm\nLHE\nKHI\n5:55 pm +1\nISB\n19h 55m\nOnly 1 seat left at this price\n$225\nPakistan International Airlines\nView Deal",
#   "SAUDIA\n10:45 am\nLHE\nJED\n1:20 am +1\nISB\n14h 35m\n$745\nSAUDIA\nView Deal"
# ]

# x = parse_flight_info(l)
# print(to_markdown(x.text))