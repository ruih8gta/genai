import os
import configparser
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
#会話履歴
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph

from typing import Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict



#Config Definition
#単純なチャットボット
def model_simple():
    prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "あなたは{local}人です。ユーザーの会話に対して{local}弁で返答をしてください",
                ),
                ("human", "{message}"),
            ]
        )
    #result = model.invoke(messages)
    parser = StrOutputParser()
    chain = prompt_template | model | parser
    return chain


class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    language: str

def model_histoy():
    prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "あなたはAIアシスタントです。質問には必ず{language}語で答えてください。",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

    # Define a new graph
    workflow = StateGraph(state_schema=State)
    # Define the function that calls the model
    def call_model(state: State):
        chain = prompt_template | model
        response = chain.invoke(state)
        return {"messages": response}


    # Define the (single) node in the graph
    workflow.add_edge(START, "model")
    workflow.add_node("model", call_model)

    # Add memory
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    return app

if __name__ =="__main__":
    conf = configparser.ConfigParser()
    conf.read("setting.ini",encoding="utf-8")
    os.environ["OPENAI_API_KEY"] = conf["DEFAULT"]["api_key"]

    model = ChatOpenAI(model="gpt-4-turbo")

    #1 基本的な会話の実行
    """
    chain = model_simple()
    print(chain.invoke({"local":"沖縄","message":"こんにちは、元気ですか？"}))
    """
    #1 end

    #2 履歴を保持する会話の実行
    
    app = model_histoy() 
    config = {"configurable": {"thread_id": "abc123"}}
    #query1:自己紹介
    query = "私は太郎です."
    language = "英語"
    input_messages = [HumanMessage(query)]
    output = app.invoke(
        {"messages": input_messages,"language":language},
        config)
    output["messages"][-1].pretty_print()  # output contains all messages in state
    #query2:同じthread_idだと、会話を覚えている
    query2 = "私の名前は何ですか?"
    input_messages2 = [HumanMessage(query2)]
    output2 = app.invoke({"messages": input_messages2}, config)
    output2["messages"][-1].pretty_print()
    config2 = {"configurable": {"thread_id": "abc234"}}
    #query3:thread_idが変わると、会話を忘れる。
    input_messages3 = [HumanMessage(query2)]
    output3 = app.invoke({"messages": input_messages3,"language":language}, config2)
    output3["messages"][-1].pretty_print()
    #2 end