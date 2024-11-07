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



documents = [
    Document(
        page_content="Dogs are great companions, known for their loyalty and friendliness.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Cats are independent pets that often enjoy their own space.",
        metadata={"source": "mammal-pets-doc"},
    ),
    Document(
        page_content="Goldfish are popular pets for beginners, requiring relatively simple care.",
        metadata={"source": "fish-pets-doc"},
    ),
    Document(
        page_content="Parrots are intelligent birds capable of mimicking human speech.",
        metadata={"source": "bird-pets-doc"},
    ),
    Document(
        page_content="Rabbits are social animals that need plenty of space to hop around.",
        metadata={"source": "mammal-pets-doc"},
    ),
]

if __name__ =="__main__":
    conf = configparser.ConfigParser()
    conf.read("setting.ini",encoding="utf-8")
    os.environ["OPENAI_API_KEY"] = conf["DEFAULT"]["api_key"]

    #ベクトルストア
    vectorstore = FAISS.from_documents(
        documents,
        embedding=OpenAIEmbeddings(model="text-embedding-ada-002"),
    )
    """
    #1
    #類似度に対応した返答を返す
    print(vectorstore.similarity_search("cat"))
    #スコア付きで返答を返す
    print(vectorstore.similarity_search_with_score("cat"))
    
    #???
    embedding = OpenAIEmbeddings().embed_query("cat")
    print(vectorstore.similarity_search_by_vector(embedding))
    #1 end
    """
    #検索
    """
    #2
    retriever = RunnableLambda(vectorstore.similarity_search).bind(k=1)  # select top result
    print(retriever.batch(["cat", "shark"]))
    
    retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 1},
    )
    print(retriever.batch(["cat", "shark"]))
    #2 end
    """
    llm = ChatOpenAI(model="gpt-4-turbo")

    message = """
    Answer this question using the provided context only.
    {question}
    Context:
    {context}
    """
    retriever = RunnableLambda(vectorstore.similarity_search).bind(k=1)  # select top result
    prompt = ChatPromptTemplate.from_messages([("human", message)])
    rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm
    response = rag_chain.invoke("tell me about cats")
    print(response.content)
