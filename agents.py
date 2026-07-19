from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from tools import web_search,url_scrapper
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini",temperature=0)



#1st model
def search_agent():
    return create_agent(
        model= llm,
        tools= [web_search]
    )

#2nd model
def reader_agent():
    return create_agent(
        model= llm,
        tools= [url_scrapper]
    )


# create a search chain

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert AI Research Writer.

Write a well-structured, factual, and professional research report using ONLY the provided research data.

Report Structure:
1. Introduction
2. Key Findings (Minimum 3 detailed findings)
3. Conclusion
4. Sources (List all source URLs exactly as provided)

Do not fabricate information.
Keep the report clear, concise, and properly formatted.
"""
    ),
    (
        "human",
        """
Research Topic:
{topic}

Research Data:
{research}

Generate the research report following the specified structure.
"""
    )
])

parser_1 = StrOutputParser()
writer_chain = writer_prompt | llm | parser_1


# create a critic chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert AI Research Critic.

Review the research report based on the following criteria and Evaluate as:
1. Accuracy (2 marks)
2. Clarity (2 marks)
3. Completeness (2 marks)
4. Structure (2 marks)
5. Sources & Citations (2 marks)

Provide:
- Overall Score: X/10
- Strengths
- Weaknesses
- Suggested Improvements

If improvements are needed, clearly mention them. Otherwise, state that the report meets all requirements.
"""
    ),
    (
        "human",
        """
Research Topic:
{topic}

Research Report:
{report}

Review the report and provide constructive feedback.
"""
    )
])

parser_2 = StrOutputParser()
critic_chain = critic_prompt | llm | parser_2

