from bs4 import BeautifulSoup
import requests

url = "https://www.newegg.com/amd-ryzen-7-5800x/p/N82E16819113665?quicklink=true"

results = requests.get(url)
doc = BeautifulSoup(results.text, "html.parser")

product = doc.find_all("h1")
product_parent = product[1].parent
product_heading = product_parent.find(class_="product-title")

prices = doc.find_all(text="$")
parent = prices[0].parent
strong = parent.find("strong")

for heading in product_heading:
    print(f"Current price of", heading.strip(), ": $", strong.string)