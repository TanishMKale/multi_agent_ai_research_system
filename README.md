# Multi-Agent AI Research System

A small multi-agent pipeline that researches a topic and writes a report on it, using LangChain + OpenAI.

You give it a topic, and it goes: search the web → read the best source → write a report → critique the report.

## How it works

1. **Search Agent** - looks up the topic on the web using Tavily search
2. **Reader Agent** - picks the most relevant link from the search results and scrapes it for more detail
3. **Writer Chain** - takes everything gathered and writes a structured report (intro, key findings, conclusion, sources)
4. **Critic Chain** - reviews the report and scores it out of 10 (accuracy, clarity, completeness, structure, sources), plus gives feedback

The first two are actual LangChain agents (they decide which tool to use and how). The writer and critic are simpler prompt chains — they just take input and generate output, no decision-making involved.

## Tech used

- LangChain (agents + chains)
- OpenAI (gpt-4o-mini)
- Tavily API for web search
- BeautifulSoup for scraping
- Streamlit for the UI

## Running it

```bash
pip install -r requirements.txt
```

Create a `.env` file with:
```
OPENAI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

Then run:
```bash
streamlit run streamlit_app.py
```

Enter a topic, hit "Run Research Pipeline", and watch it go through each step live. You get the final report plus the critic's feedback, and you can download the report as markdown.

You can also run it from the terminal without the UI:
```bash
python pipeline.py
```

## Notes

- `practise.py` is just a scratch file I used while building the scraper tool, not part of the actual app.
- Web search results depend on what Tavily returns, so answer quality varies a bit topic to topic.
- Because it's 2 real agents + 2 chains rather than "4 agents," it's a good example of when to use an agent (needs to decide/act) vs a plain prompt chain (just needs to transform input to output).

