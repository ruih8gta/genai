import os
import configparser
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

#Config Definition
def model():
    config = configparser.ConfigParser()
    config.read("setting.ini",encoding="utf-8")
    os.environ["OPENAI_API_KEY"] = config["DEFAULT"]["api_key"]

    model = ChatOpenAI(model="gpt-3.5-turbo")
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
    #print(chain.invoke({"local":"関西","message":"こんにちは、元気ですか？"}))
    return chain