from bs4 import BeautifulSoup
import requests,lxml
import pandas as pd
url_list = []
for i in range(1,26):
   url_list.append('https://www.walmart.com/browse/beverages/soda-pop/976759_976782_1001680/?page=' + str(i) + '&cat_id=976759_976782_1001680') 
item_names = []
price_list = []
item_ratings = []
item_reviews = []
shipping_details_list = []

for url in url_list:
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c, 'html')
    summary = soup.find('div', {'class':'search-product-result', 'id':'searchProductResult'})
    land_list = summary.findAll('li')
    
    for land in land_list:
        
        # to get the item name
        item_names.append(land.find('a', {'class': 'product-title-link line-clamp line-clamp-2'}).get('aria-label'))
        
        # to get the item price
        price_summary = land.find('span', {'class' : 'price display-inline-block arrange-fit price price-main'})
        if price_summary is None:
            price_list.append('In-store purchase only')
        else:
            if price_summary.find('span', {'class': 'price-group'}) is not None:
                price_list.append(price_summary.find('span', {'class': 'price-group'}).get('aria-label'))
            else:
                price_list.append('In-store purchase only')
        
        # to get the item ratings 
        item_ratings.append(land.find('span', {'class':'stars-container'}).get('aria-label').split(' ')[2])
        
        # to get the item reviews
        item_reviews.append(land.find('span', {'class':'stars-container'}).get('aria-label').split(' ')[9])
        
        
        
# creating a dataframe 
df = pd.DataFrame({'Product_Name':item_names, 'Price':price_list, 'Rating':item_ratings,'No_Of_Reviews':item_reviews}, columns=['Product_Name', 'Price', 'Rating', 'No_Of_Reviews'])
df.head(10)