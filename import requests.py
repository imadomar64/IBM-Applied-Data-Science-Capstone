import requests
from bs4 import BeautifulSoup
import csv

# URL of the Wikipedia page
url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find the tables containing the launch data (from table[2] to table[7])
    tables = soup.find_all("table")[2:8]

    # Extract data from each table and concatenate
    data = []
    for table in tables:
        for row in table.find_all("tr")[1:]:  # Skip the header row
            # Exclude rows with td elements having colspan="9"
            if not row.find("td", colspan="9"):
                columns = row.find_all(["th", "td"])
                launch_data = [column.get_text(strip=True) for column in columns]
                # Convert Flight No. to integer
                if launch_data[0].isdigit():
                    launch_data[0] = int(launch_data[0])
                data.append(launch_data)

    # Define column headers
    headers = ["Flight No.", "Date and time (UTC)", "Version, Booster [b]", "Launch site", 
               "Payload[c]", "Payload mass", "Orbit", "Customer", "Launch outcome", "Booster landing"]

    # Save data to a CSV file with headers
    filename = "falcon_launches.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write column headers
        writer.writerows(data)

    print(f"Data from tables 2 to 7 has been saved to {filename}")
else:
    print("Failed to retrieve the webpage")


