import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser

# Set API key for LLM and Search Engine Scraper
tavily_api_key = os.getenv('TAVILY_API_KEY')
cohere_api_key = os.getenv('COHERE_API_KEY')

# Initialize TavilySearchResults and include maximum results to grab
tavily_tool = TavilySearchResults(max_results=10)

# Initialize LLM model used in grading
llm = ChatCohere(model="command-r")

# Command R summarization tool
def cohere_summarization_tool(text: str, api_key: str) -> str:
    """Summarize the text using the Cohere API"""
    import cohere
    co = cohere.Client(api_key)
    response = co.summarize(text=text, length='Long', model='summarize-xlarge')
    return response.summary

# Retrieve articles and summarize using summarize
def fetch_and_summarize_news(query):
    # Grab search results using Tavily
    search_results = tavily_tool.invoke({"query": query})
    
    articles_content = []

    # Loop through search results and fetch article content
    for result in search_results:
        articles_content.append(result.get('content', ''))

    # Combine all fetched article content
    combined_content = " ".join(articles_content)


    summary = cohere_summarization_tool(combined_content, cohere_api_key)

    return summary

# For grading purposes defining the GradeDocuments class
class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""
    binary_score: str = Field(description="Documents are relevant to the question, 'yes' or 'no'")

# Preamble for grading
preamble = """You are a grader assessing relevance of a retrieved document to a user question. 
If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. 
Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""

# LLM grader setup
structured_llm_grader = llm.with_structured_output(GradeDocuments, preamble=preamble)

grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
    ]
)

retrieval_grader = grade_prompt | structured_llm_grader

# Set Query
query = "Latest advancements in AI"
summary = fetch_and_summarize_news(query)
print("Summary of latest news on AI:\n", summary)

# Set relevance for grading through question
question = "What are the latest advancements in AI?"
docs = [{"page_content": summary}] 
doc_txt = docs[0]["page_content"]
response = retrieval_grader.invoke({"question": question, "document": doc_txt})
print("Relevance grading:\n", response)
