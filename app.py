from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os
import re


app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')
OPENAI_API_KEY=OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
print('API KEY----------------------------------')

print(OPENAI_API_KEY)
print('--------------------------------------------')


embeddings = download_hugging_face_embeddings()


index_name = "copticbot"

# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":4})


llm = OpenAI(temperature=0.1, max_tokens=500)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

def format_with_br_tags(answer: str) -> str:
    formatted_lines = []

    # Split into numbered list items (e.g., "1. ...", "2. ...")
    list_items = re.findall(r'\d+\.\s.*?(?=\d+\.|$)', answer, re.DOTALL)

    for item in list_items:
        # Add <br> at the end of the item
        item = item.strip()

        # Break long sentences (>25 words)
        sentences = re.split(r'(?<=[.!?])\s+', item)
        new_sentences = []
        for sentence in sentences:
            words = sentence.split()
            if len(words) > 1025:
                # Try to break at a natural pause (e.g., comma or semicolon)
                chunks = re.split(r'([,;])', sentence)
                rebuilt = ""
                word_count = 0
                for chunk in chunks:
                    chunk_words = chunk.split()
                    word_count += len(chunk_words)
                    rebuilt += chunk
                    """ if word_count >= 25:
                        rebuilt += "<br>"
                        word_count = 0 """
                new_sentences.append(rebuilt)
            else:
                new_sentences.append(sentence)
        
        # Recombine and append <br> after the whole item
        formatted_item = ' '.join(new_sentences).strip() + "<br>"
        formatted_lines.append(formatted_item)

    return '\n'.join(formatted_lines)

@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    user_input = msg
    print("User Input:", user_input)

    response = rag_chain.invoke({"input": user_input})
    raw_answer = response["answer"]
    print("Raw Answer:", raw_answer)

    formatted_answer = format_with_br_tags(raw_answer)
    print("Formatted Answer:", formatted_answer)

    return formatted_answer 
""" 
@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    response = rag_chain.invoke({"input": msg})
    print("Response : ", response["answer"])
    return response["answer"]
    
    """




if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 4000, debug= True)