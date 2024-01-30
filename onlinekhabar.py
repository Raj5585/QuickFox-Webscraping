# scraping onlinekhabar and extracting news 
import requests
from bs4 import BeautifulSoup
from keywords import keywords
from postgres import sendtodb

text_content_list = []
newsdict = {}
print(keywords)
for keyword in keywords():
    print(keyword)
    
    text_content_list.append(f"for {keyword}: ")
    news_portal_url = f'https://english.onlinekhabar.com/?s={keyword}'

    response = requests.get(news_portal_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        main_div = soup.find('div', class_='listical-news-big')

    if main_div:
        innerdiv = main_div.find_all('div',class_ = 'ok-post-contents')
        
        newslst = []
        for div in innerdiv:
            a_tags = div.find_all('a')
            day = div.find('span', class_ = 'ok-post-hours')
            str = day.text
            lst = str.split(' ')
            if(lst[1]== 'hours'):
                    #newsdict[keyword]:[[a.text for a in a_tags], [a.get('href') for a in a_tags]]
                    #newsdict[f'{keyword}']:[[a.text for a in a_tags],[a.get('href') for a in a_tags]]
                    #text_content_list.append(f"{lst[0]} hours ago:")
                        #text_content_list.extend([a.text for a in a_tags])
                    # text_content_list.extend([a.get('href') for a in a_tags])
                    newslst.extend([a.text for a in a_tags])
                    newslst.extend([a.get('href') for a in a_tags])
         
            if ( lst[1] == 'days'):
                if(int(lst[0])<10):
                    newslst.extend([a.text for a in a_tags])
                    newslst.extend([a.get('href') for a in a_tags])
                   # newsdict[keyword]:[[a.text for a in a_tags], [a.get('href') for a in a_tags]]
                    #newsdict[f'{keyword}']:[f'{[a.text for a in a_tags]}',f"{[a.get('href') for a in a_tags]}"]
                    #text_content_list.append(f"{lst[0]} days ago:")
                    # text_content_list.extend([a.text for a in a_tags])
                    # text_content_list.extend([a.get('href') for a in a_tags])
            newsdict[keyword] = newslst
               
                    
    else:
        print("Failed to retrieve the page. Status code:", response.status_code)

sendtodb(newsdict, "Online khabar")
