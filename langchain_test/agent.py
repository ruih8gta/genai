import os
import configparser
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

#ベクトルストア
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
#検索
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import RunnablePassthrough


# Import relevant functionality
from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

#Agent作成用
from langgraph.prebuilt import create_react_agent


conf = configparser.ConfigParser()
conf.read("setting.ini",encoding="utf-8")
os.environ["OPENAI_API_KEY"] = conf["DEFAULT"]["api_key"]
#os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["TAVILY_API_KEY"] = conf["DEFAULT"]["tavily_key"]


search = TavilySearchResults(max_results=2)
#0 tavily 呼び出し
#search_results = search.invoke("what is the weather in SF")
#print(search_results)
#0 end
# If we want, we can create other tools.
# Once we have all the tools we want, we can put them in a list that we will reference later.
tools = [search]

#OpenAIチャット設定
model = ChatOpenAI(model="gpt-4-turbo")
#1 通常メッセージ
"""
response = model.invoke([HumanMessage(content="hi!")])
print(response.content)
"""
#1 end

#2 ツールとモデルを連携
"""
model_with_tools = model.bind_tools(tools)

response = model_with_tools.invoke([HumanMessage(content="Hi!")])

print(f"ContentString: {response.content}")
print(f"ToolCalls: {response.tool_calls}")

#toolに関係する質問
response = model_with_tools.invoke([HumanMessage(content="What's the weather in SF?")])
print(f"ContentString: {response.content}")
print(f"ToolCalls: {response.tool_calls}")
"""
#2 end


#agent_executor = create_react_agent(model, tools)
"""
response = agent_executor.invoke({"messages": [HumanMessage(content="hi!")]})

print(response["messages"])

response = agent_executor.invoke(
    {"messages": [HumanMessage(content="栃木県の市長選挙はいつ?")]}
)
print(response["messages"])
"""
"""
#3 stream
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="2024年の栃木県宇都宮市の市長選挙は何月何日ですか?日本語で回答して。")]}
):
    print(chunk)
    print("----")
#3 end
"""
memory = MemorySaver()
agent_executor = create_react_agent(model, tools, checkpointer=memory)

config = {"configurable": {"thread_id": "abc123"}}
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="私は築地山喜代三郎です。")]}, config
):
    print(chunk)
    print("----")

for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="私は誰でしょうか。")]}, config
):
    print(chunk)
    print("----")    