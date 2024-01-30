# scraping RatoPati and extracting news 
import requests
from bs4 import BeautifulSoup
from keywords import keywords
from postgres import sendtodb

Ratonewsdict = {}
for keyword in keywords():
    news_portal_url = f'https://english.ratopati.com/search?query={keyword}'

    response = requests.get(news_portal_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        main_div = soup.find('div', class_='grid')

    if main_div:
        innerdiv = main_div.find_all('div',class_ = 'post-card__more-secondary-story')
        
        ratonewslst = []
        for div in innerdiv:
            a_tags = div.find_all('a')
            day = div.find('time', class_ = 'post-card__time')
            str = day.text
            lst = str.split(' ')
            if(lst[1]== 'hours'):
                ratonewslst.extend([(a.text).replace('\n', '') for a in a_tags])
                ratonewslst.extend([a.get('href') for a in a_tags])
         
            if ( lst[1] == 'days'):
                if(int(lst[0])<20):
                    ratonewslst.extend([a.text.replace('\n', '') for a in a_tags])
                    ratonewslst.extend([a.get('href') for a in a_tags])

            if ( lst[1] == 'weeks'):
                if(int(lst[0])<10):
                    ratonewslst.extend([a.text.replace('\n','') for a in a_tags])
                    ratonewslst.extend([a.get('href') for a in a_tags])
            Ratonewsdict[keyword] = ratonewslst
               
                    
    else:
        print("Failed to retrieve the page. Status code:", response.status_code)
print(Ratonewsdict)

sendtodb(Ratonewsdict, 'Ratopati')