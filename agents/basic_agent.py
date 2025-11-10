from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from tools.basic_tool import echo_tool

llm = ChatOpenAI(model="gpt-4.1-mini") 

tools = [echo_tool]

prompt = "너는 사용자 요청을 이해하고 필요하면 툴을 사용해서 답변하는 어시스턴트야."

agent = create_agent(model=llm, tools=tools, system_prompt=prompt)
