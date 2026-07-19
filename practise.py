from tavily import TavilyClient
import requests
from rich import print
import langchain
from langchain.tools import tool
from bs4 import BeautifulSoup


#create tool2 to scrape the url above tool will bring with the help of search agent
@tool
def url_scrapper(url:str)-> str:
    """Scrape the URLs in order to get clean text for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent":"Mozilla/5.0"})
        #the above will return raw text including the tags
        soup = BeautifulSoup(resp.text,"html.parser")#get the text and parse with its func htmlparser
        #time to remove tags
        for tag in soup(['script','nav','footer','style']):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]#max 3000 words
    except Exception as e:
        return f"Cant read URL: {str(e)}"
    
    
print(url_scrapper.invoke("https://www.hindustantimes.com/world-news/either-make-deal-or-finish-job-donald-trump-warning-to-iran-khamenei-funeral-nuclear-weapons-oil-prices-white-house-101783350291671.html"))
