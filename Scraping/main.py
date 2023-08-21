import csv
import requests
from bs4 import BeautifulSoup

# Define the base URL and headers
base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2
C283&ref=sr_pg_1"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

# Define the search parameters
params = {
    "k": "bags",
    "crid": "2M096C61O4MLT",
    "qid": "1653308124",
    "sprefix": "ba"
}

# Send a GET request to the URL
response = requests.get(base_url, headers=headers, params=params)

# Parse the response content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find all product containers on the page
product_containers = soup.find_all("div", class_="s-result-item")

# Initialize an empty list to store scraped data
products = []

# Loop through each product container and extract information
for container in product_containers:
    product_url = container.find("a", class_="a-link-normal")["href"]
    product_name = container.find("span", class_="a-text-normal").text
    product_price = container.find("span", class_="a-offscreen").text
    rating = container.find("span", class_="a-icon-alt").text.split()[0]
    num_reviews = container.find("span", class_="a-size-base").text.split()[0]

    products.append({
        "Product URL": product_url,
        "Product Name": product_name,
        "Product Price": product_price,
        "Rating": rating,
        "Number of Reviews": num_reviews
    })

# Define the CSV filename
csv_filename = "amazon_products.csv"

# Write the scraped data to a CSV file
with open(csv_filename, mode="w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Product URL", "Product Name", "Product Price", "Rating", "Number of Reviews"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for product in products:
        writer.writerow(product)

print(f"Scraped data saved to {csv_filename}")
