
import pandas as pd
def keywords():
    df = pd.read_csv('WebcrapingTopics.csv')
    keywords = df['Topics'].tolist()
    return keywords

keywords()