import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

headers = ["Title", "Link", "Type", "Asking", "Notes", "Where",
           "Size (garden)", "Rooms", "Rating", "Plan", "Agent", "Status"]

with open("data/idealista_urls.txt", "r") as url_file:
    urls = [line.strip() for line in url_file if line.strip()]

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_filename = f"output/idealista_{timestamp}.csv"

    with open(output_filename, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(headers)

        for url in urls:
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Title
                title = soup.find("span", class_="main-info__title-main").text.strip()

                # Price
                span_element = soup.find("span", class_="info-data-price").text.strip()
                price = span_element.find("span", class_="txt-bold").text.strip()

                # Rooms & Size
                div_element = soup.find("div", class_="info-features")
                spans = div_element.find_all("span")
                size = spans[0].text.strip()
                rooms = spans[1].text.replace("locali", "").strip()

                # Type
                div_element = soup.find("div", class_="details-property_features")
                li_elements = div_element.find_all("li")
                property_type = li_elements[0].text.strip()

                # Agent
                a_element = soup.find("a", class_="about-advertiser-name")
                agent = a_element.text.strip()

                # Print the extracted data
                print("Url", url)
                print("Title:", title)
                print("Price:", price)
                print("Size:", size)
                print("Rooms:", rooms)
                print("Type:", property_type)
                print("Agent:", agent)
                print("-------")

                writer.writerow([title, url, property_type, price, "", "", size, rooms, "", "", agent, ""])

            else:
                print("Failed to retrieve the webpage. Status code:", response.status_code)

print(f"CSV file '{output_filename}' has been created with all the extracted values and headers.")
