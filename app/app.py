import os
import gradio as gr
import requests
from dotenv import load_dotenv
from langchain.agents import AgentExecutor
from agentwiki.retriever_agent import agent_chain,search
from agentwiki.output_parser import extract_between_tags

# Load environment variables from .env file

load_dotenv()

UI_PORT: int = int(os.getenv("UI_PORT", "8510"))

# def respond(question, history):
#     url = "http://localhost:8000/chat"
#     data = {
#         "question": question
#     }
#     response = requests.post(url,data=data)
#     if response.status_code == 200:
#         return response.json()
#     return "No he podido responder a tu pregunte. Por favor, intenta de nuevo."

assistant = AgentExecutor(agent=agent_chain, tools=[search], verbose=False)

def respond(question, history):
    global assistant
    response  = assistant.invoke({"query": question})
    return extract_between_tags('information', response['output'])



icon_bot_path = "assets/bot.png"
icon_user_path = "assets/user.png"
chatbot = gr.ChatInterface(
    fn=respond,
    chatbot=gr.Chatbot(elem_id="chatbot", height="auto", avatar_images=[icon_user_path, icon_bot_path]),
    title="",
    textbox=gr.Textbox(placeholder="¡Hola!, ¿en que te puedo ayudar?", container=False, scale=7),
    clear_btn="Limpiar",
    retry_btn=None,
    undo_btn=None,
    submit_btn="Enviar",
    theme=gr.themes.Default(primary_hue="purple", secondary_hue="indigo"),
)

# Which city has more citizens: Alicante or Murcia?
if __name__ == "__main__":
    chatbot.launch(server_name="0.0.0.0",server_port=UI_PORT)
  
  
