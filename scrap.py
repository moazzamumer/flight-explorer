from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def get_flight_info(json_data: dict):

    # Extract origin, destination, and departure date from JSON data
    origin = json_data['origin']
    destination = json_data['destination']
    departure_date = json_data['date']
    
    # Construct the URL with the extracted data
    url = f"https://booking.kayak.com/flights/{origin}-{destination}/{departure_date}"

    # Configure Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    # Initialize the WebDriver (assuming you have Chrome WebDriver installed)
    driver = webdriver.Chrome(options=chrome_options)

    # Load the HTML page
    driver.get(url)

    try:
        # Find all elements with the specified class name
        elements = driver.find_elements(By.CLASS_NAME, "Base-Results-HorizonResult")
        
        # Extract information from the found elements
        flights = []
        max_flight_count = 5
        for element in elements:
            flights.append(element.text)
            max_flight_count -= 1
            if max_flight_count == 0:
                break
    except Exception as e:
        print("Error:", e)

    # Close the WebDriver
    driver.quit()
    return flights

# json_data = {
#     "date": "2024-06-07",
#     "origin": "LHE",
#     "destination": "ISB",
#     "num_passengers": "1"
# }

# x = get_flight_info(json_data)
# print(x)