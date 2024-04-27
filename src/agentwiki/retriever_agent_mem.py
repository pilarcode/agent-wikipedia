from langchain.agents import AgentExecutor
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import MessagesPlaceholder
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
MEMORY_KEY = "chat_history"

prompt = ChatPromptTemplate.from_messages(
    [
        ("user", retrieval_prompt),
        ("ai", "{agent_scratchpad}"),
        MessagesPlaceholder(variable_name=MEMORY_KEY)
    ]
)

prompt = prompt.partial(retriever_description=retriever_description)


bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

model = BedrockChat(
    client=bedrock_runtime,
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    model_kwargs={"temperature": 0.0},
)

#RunnablePassthrough object is used as a “passthrough” take takes any input to the current component 
#and allows us to provide it in the component output.
chain = (
    RunnablePassthrough.assign(
        agent_scratchpad=lambda x: format_agent_scratchpad(x["intermediate_steps"])
    )
    | prompt
    | model.bind(stop_sequences=["</search_query>"])
    | StrOutputParser()
)

#The RunnableParallel object allows us to define multiple values and operations, and run them all in parallel
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

