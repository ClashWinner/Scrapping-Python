# Required Librearies
from bs4 import BeautifulSoup
import requests
import csv

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'device-memory': '4',
    'downlink': '10',
    'dpr': '0.75',
    'ect': '4g',
    'rtt': '50',
    'sec-ch-device-memory': '4',
    'sec-ch-dpr': '0.75',
    'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-ch-viewport-width': '823',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'viewport-width': '823',
}

# CSV file for Scrap 20 pages
file_one = 'Scrap_20_Pages.csv'
with open(file_one,"w",encoding="utf-8") as f:
    f.write = csv.writer(f)
    f.write.writerow(['Hit Count','Page No', 'Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews'])

# CSV file for data of each URL
file_two = 'Hit_Product_URL.csv'
with open(file_two,"w",encoding="utf-8") as f2:
    f2.write = csv.writer(f2)
    f2.write.writerow(['Hit Count','Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'Description', 'ASIN', 'Product Description', 'Manufacturer'])

hit_count=1

# Function to Extract and Save data to CSV
def product_data(url, headers):
    html = requests.get(url=url,headers=headers)
    soup = BeautifulSoup(html.content, 'html.parser')
    bags = soup.find_all('div' , {'class':"sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16"})
    for j in range(0,len(bags)):
        bag = bags[j]
        try:
            product_url = "https://www.amazon.in/"+bag.find('a', class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")['href']
            product_name = bag.find('span', class_="a-size-medium a-color-base a-text-normal").text
            product_price = bag.find('span', class_="a-price-whole").text
            product_rating = bag.find('span', class_="a-size-base").text
            number_of_reviews = bag.find('span', class_="a-size-base s-underline-text").text[1:-1]
        except:
            pass

        product_page = requests.get(url=product_url,headers=headers)
        product_page_soup = BeautifulSoup(product_page.content, 'html.parser')
        details = product_page_soup.find('div', id="dp")
        try:
            description = details.find('ul', class_="a-unordered-list a-vertical a-spacing-mini").text
        except:
            pass

        try:
            product_description = details.find(id="productDescription").text.strip()
        except:
            pass
        try:
            product_details = details.find('ul', class_="a-unordered-list a-nostyle a-vertical a-spacing-none detail-bullet-list").find_all('span', class_="a-list-item")

            for ele in range(1,len(product_details)):
                if "Manufacturer" in product_details[ele].text:
                    manufacturer = product_details[ele].text.split('                                 ')[-1]
                    break

            for ele in range(len(product_details)):
                if "ASIN" in product_details[ele].text:
                    asin = product_details[ele].text.split()[-1]
                    break
        except:
            manufacturer = ""
            asin = ""
        
        global hit_count
        f=open('Scrap_20_Pages.csv','a',newline='')
        writer = csv.writer(f)
        try:
            writer.writerow([hit_count, i, product_url, product_name, product_price, product_rating, number_of_reviews])
        except:
            pass
        f2=open('Hit_Product_URL.csv','a',newline='')
        writer = csv.writer(f2)
        try:
            writer.writerow([hit_count,product_url, product_name, product_price, product_rating, number_of_reviews, description, asin, product_description, manufacturer])
        except:
            pass
        hit_count+=1

# Iterate the all 20 pages appeared in search results
for i in range(1,21):

    if i == 1:
        url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
        product_data(url,headers)
    else:
        url = f'https://www.amazon.in/s?k=bags&page={i}&crid=2M096C61O4MLT&qid=1679396405&sprefix=ba%2Caps%2C283&ref=sr_pg_{i}'
        product_data(url,headers)



 

