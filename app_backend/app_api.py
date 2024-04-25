
from contextlib import asynccontextmanager
import uvicorn
from fastapi import  FastAPI, status
from pydantic import BaseModel, Field
from langchain.agents import AgentExecutor
from agentwiki.retriever_agent import agent_chain,search
from agentwiki.output_parser import extract_between_tags

@asynccontextmanager
async def lifespan(app: FastAPI): 
    """
    Initializes the application on startup.
    Sets the global variables `assistant` and `df` to their initial values.
    """
    global assistant  # pylint: disable=global-statement
    assistant = AgentExecutor(agent=agent_chain, tools=[search], verbose=False)
    yield


app = FastAPI(
    title="Backend API",
    description="Backend API",
    version="0.1",
    lifespan=lifespan,
)


class ChatbotRequest(BaseModel):
    """
    A model representing the chatbot request
    Attributes:
    query: str
        The user query.
    """

    question: str = Field(..., description="The user's question")

class ChatbotResponse(BaseModel):
    """
    A model representing the chatbot response

    Attributes:
    query: str
         The user question.
    response: str
        The llm response.
    """
    question: str 
    llm_response: str



@app.post("/chat", status_code=status.HTTP_200_OK, tags=["chatbot"], response_model=ChatbotResponse)
async def chat(chatbot_request: ChatbotRequest)-> ChatbotResponse:
    """
    Main endpoint for the chatbot API. It receives a user question, processes it,
    and returns the chatbot's response.

    ### Arguments
    - **chatbot_request**: The chatbot's request.

    ### Returns
    - **chatbot_response**: The chatbot's response to the user question.
    """
    global assistant  # pylint: disable=global-statement, global-variable-not-assigned

    question = chatbot_request.question
    response  = assistant.invoke({"query": question})
    llm_response = extract_between_tags('information', response['output'])

    return  ChatbotResponse(question=question, llm_response=llm_response)
      

if __name__ == "__main__":
    uvicorn.run("app_api:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")

