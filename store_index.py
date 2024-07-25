from src.helper import read_file,text_split,embed
from langchain_community.vectorstores import Pinecone
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone as LangchainPinecone
from pinecone import Pinecone, ServerlessSpec
import pinecone
import os
from dotenv import load_dotenv
load_dotenv()

openaikey=os.getenv('openaikey')
os.environ['openai_api_key']=openaikey
embedding=OpenAIEmbeddings()

data = read_file('C:\\Users\\DELL\\OneDrive\\Desktop (1)\\kfc chatbot\\data\\data.txt')

datachunks = text_split(data)

texts = datachunks

doc_embeds = embed(texts)

vectors = []
for idx, (text, embedding) in enumerate(zip(datachunks, doc_embeds)):
    vectors.append({
        "id": str(idx+1),
        "values": embedding,
        "metadata": {'text': text}
    })
    
load_dotenv()
pinecone_key=os.getenv('pineconekey')
pc = Pinecone(pinecone_key)
print(pc)
index_name = "chatbot-kfc" 
index=pc.Index('chatbot-kfc')

try:
    index.upsert(
        vectors=vectors,
        namespace="ns1"
    )
    print("Vectors upserted successfully.")
except Exception as e:
    print(f"An error occurred during upsert: {e}")
    raise





