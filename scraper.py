from bs4 import BeautifulSoup
import requests
import re

# Get the compenent the user is looking for from all pages of the given site
pc_component = input("Enter the product you want to find: ")

url = f"https://www.newegg.com/p/pl?d={pc_component}&N=4131"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")

page_number = doc.find(class_="list-tool-pagination-text").strong
pages = int(str(page_number).split("/")[-2].split(">")[-1][:-1])

items_found = {}

# Get links and pricing for all of the given compenent that are currently available
for page in range(1, pages + 1):
    url = f"https://www.newegg.com/p/pl?d={pc_component}&N=4131&page={page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")
    inner_content = doc.find(
        class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    items = inner_content.find_all(text=re.compile(pc_component))

    for item in items:
        parent = item.parent

        if parent.name != "a":
            continue

        link = parent['href']
        parent_price = item.find_parent(class_="item-container")
        try:
            price = parent_price.find(
                class_="price-current").find("strong").string
            items_found[item] = {"price": int(
                price.replace(",", "")), "link": link}
        except:
            pass

# Sort all found products by price and print
sort_items = sorted(items_found.items(), key=lambda x: x[1]['price'])

for item in sort_items:
    print(item[0])
    print(f"${item[1]['price']}")
    print(item[1]['link'])
    print("")
