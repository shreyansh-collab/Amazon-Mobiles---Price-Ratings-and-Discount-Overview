from bs4 import BeautifulSoup
import pandas as pd
import os

# List of all HTML files from page 1 to 7
html_files = [
    "Amazon_Electronics.html",       # Page 1
    "Amazon_Electronics_2.html",     # Page 2
    "Amazon_Electronics_3.html",     # Page 3
    "Amazon_Electronics_4.html",     # Page 4
    "Amazon_Electronics_5.html",     # Page 5
    "Amazon_Electronics_6.html",     # Page 6
    "Amazon_Electronics_7.html"      # Page 7
]

all_products = []

# Loop through each HTML file
for file_name in html_files:
    if not os.path.exists(file_name):
        print(f" File not found: {file_name}")
        continue

    with open(file_name, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        products = soup.find_all("div", {"data-component-type": "s-search-result"})

        for product in products:
            name_tag = product.find("h2", class_="a-size-base-plus a-spacing-none a-color-base a-text-normal")
            price_tag = product.find("span", class_="a-price-whole")

            # Extract and shorten Product Name
            full_name = name_tag.get_text(strip=True) if name_tag else None
            short_name = " ".join(full_name.split()[:3]) if full_name else None

            # Extract and shorten Brand
            brand = None
            h2_tag = product.find("h2")
            if h2_tag and h2_tag.has_attr("aria-label"):
                full_brand = h2_tag["aria-label"]
                brand = full_brand.split()[0]

            discount_tag = product.find("span", string=lambda x: x and "%" in x)
            review_tag = product.find("span", class_="a-size-base s-underline-text")
            rating_tag = product.find("i", class_="a-icon-star-small")
            rating = None
            if rating_tag:
                rating_span = rating_tag.find("span", class_="a-icon-alt")
                if rating_span:
                    rating = rating_span.get_text(strip=True).split()[0]

            all_products.append({
                "Product Name": short_name,
                "Price": price_tag.get_text(strip=True) if price_tag else None,
                "Brand": brand,
                "Discount": discount_tag.get_text(strip=True) if discount_tag else None,
                "Reviews": review_tag.get_text(strip=True) if review_tag else None,
                "Rating": rating
            })

# Create DataFrame and export to CSV
df = pd.DataFrame(all_products)
output_csv = "amazon_electronics_all_pages.csv"
df.to_csv(output_csv, index=False)

print(f" Scraped data from {len(html_files)} pages saved to: {os.path.abspath(output_csv)}")
