# scraping Setopati and extracting news 

import requests
from bs4 import BeautifulSoup
from keywords import keywords
from postgres import sendtodb
from datetime import datetime, timedelta

#filter by date present day - next day 
current_datetime = datetime.now()
presentformatted_date = current_datetime.strftime("%Y-%m-%d")
next_day = current_datetime - timedelta(days=1) 
nextformatted_date = next_day.strftime("%Y-%m-%d")
presentday = str(presentformatted_date).split('-')
nextday = str(nextformatted_date).split('-')

setonewsdict = {}
for keyword in keywords():

    news_portal_url = f" https://en.setopati.com/search?from={nextday[0]}%2F{nextday[1]}%2F{nextday[2]}&to={presentday[0]}%2F{presentday[1]}%2F{presentday[2]}&keyword={keyword}"

    response = requests.get(news_portal_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        main_div = soup.find('div', class_='news-cat-list')

    if main_div:
        innerdiv = main_div.find_all('div',class_ = 'items')
        
        ratonewslst = []
        for div in innerdiv:
            a_tags = div.find_all('a')
            ratonewslst.extend([(a.text).replace('\n', '') for a in a_tags])
            ratonewslst.extend([a.get('href') for a in a_tags])
            setonewsdict[keyword] = ratonewslst
               
                    
    else:
        print("Failed to retrieve the page. Status code:", response.status_code)

print(setonewsdict)

sendtodb(setonewsdict, "Setopati")