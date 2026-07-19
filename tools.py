from langchain.tools import tool
import os
from tavily import TavilyClient
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()
import requests
from rich import print #this gives a better print for terminal

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY")) 

#refer the diagram in notes, first we will create tool 1 for web_sesrches
#below we have used tool decorator to make the below function a tool
# there is a doc string which tells llm in a good way """that one"""
@tool
def web_search(query:str)-> str:
    """Search the web for the most accurate results on the requested topic. Return Titles, URLs and Snippets"""
    results=tavily.search(query=query,max_results=5)
    #results will contain 'results' list conataining many results
    #create another list to store these results, it contains title, url and content
    out=[]
    #remember results has 'results' ie the major list
    for r in results['results']:
        out.append(f"Title: {r['title']}\nURL: {r['url']}\ncontent: {r['content'][:300]}")

    return "\n-----------\n".join(out) 
    

#tool 1 finished

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
    
    
