import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://www.amazon.in/s?k=walletss+for+men&crid=1Y7JF1G8ZAAU2&sprefix=walletss+for+men%2Caps%2C504&ref=nb_sb_noss_2"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
}

max_retries = 5
retry_delay = 5  # seconds

for retry in range(max_retries):
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()
        break  # Exit the loop if the request is successful
    except (requests.RequestException, requests.ConnectionError) as e:
        print(f"Request error (Retry {retry + 1}/{max_retries}):", e)
        if retry < max_retries - 1:
            print(f"Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            print("Max retries reached. Exiting.")
            exit()

soup = BeautifulSoup(response.content, "html.parser")
product_cards = soup.find_all("div", class_="s-result-item")

product_data = []

for card in product_cards:
    try:
        product_name_elem = card.find("span", class_="a-text-normal")
        product_name = product_name_elem.text.strip() if product_name_elem else "N/A"
        
        product_price_elem = card.find("span", class_="a-offscreen")
        product_price = product_price_elem.text.strip() if product_price_elem else "N/A"
        
        product_rating_elem = card.find("span", class_="a-icon-alt")
        product_rating = product_rating_elem.text.strip() if product_rating_elem else "N/A"
        
        product_data.append({
            "Name": product_name,
            "Price": product_price,
            "Rating": product_rating
        })
    except Exception as e:
        print("Error in extracting product data:", e)

df = pd.DataFrame(product_data)
df.to_csv("amazon_wallets.csv", index=False)

print("Data successfully extracted and CSV saved.")
