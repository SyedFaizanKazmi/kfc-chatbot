from flask import Flask,render_template,request,jsonify,send_from_directory
from src.helper import embed
from src.prompt import *
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import ctransformers
from langchain_community.vectorstores import Pinecone as LangPinecone
from langchain.prompts import PromptTemplate
from langchain_pinecone import Pinecone
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import ChatOpenAI
import pinecone
import os
from dotenv import load_dotenv
load_dotenv()
openaikey=os.getenv('openaikey')
os.environ['openai_api_key']=openaikey

app = Flask(__name__)

load_dotenv()
pinecone_key=os.getenv('pineconekey')
pc = Pinecone(pinecone_key)
index_name = "chatbot-kfc" 
index=pc.Index('chatbot-kfc')
PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
llm=ChatOpenAI()
embedding=emb=OpenAIEmbeddings()
vectorstore = LangPinecone(index=index, embedding=embedding, text_key="text", namespace="ns1")
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={'k': 2}),
    return_source_documents=True,
    chain_type_kwargs={"prompt": PROMPT},
    output_key="result"
)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    result=qa({"query": input})
    print("Response : ", result["result"])
    return str(result["result"])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)
