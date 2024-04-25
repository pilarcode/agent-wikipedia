from langchain.agents import AgentExecutor
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_community.chat_models import BedrockChat
from dotenv import load_dotenv
import boto3
from agentwiki.agent_scratchpad import format_agent_scratchpad
from agentwiki.output_parser import parse_output
from agentwiki.prompts import retrieval_prompt
from agentwiki.retriever import retriever_description, search

# Load env variables
_ = load_dotenv()

prompt = ChatPromptTemplate.from_messages(
    [
        ("user", retrieval_prompt),
        ("ai", "{agent_scratchpad}"),
    ]
)

prompt = prompt.partial(retriever_description=retriever_description)

#model = BedrockChat(model_id="anthropic.claude-3-sonnet-20240229-v1:0",region_name="us-east-1")

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

model = BedrockChat(
    client=bedrock_runtime,
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    model_kwargs={"temperature": 0.0},
)

chain = (
    RunnablePassthrough.assign(
        agent_scratchpad=lambda x: format_agent_scratchpad(x["intermediate_steps"])
    )
    | prompt
    | model.bind(stop_sequences=["</search_query>"])
    | StrOutputParser()
)

agent_chain = (
    RunnableParallel(
        {
            "partial_completion": chain,
            "intermediate_steps": lambda x: x["intermediate_steps"],
        }
    )
    | parse_output
)

agent_executor = AgentExecutor(agent=agent_chain, tools=[search], verbose=True)  
