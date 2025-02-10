# Install necessary packages
#!pip install --upgrade langchain openai tiktoken chromadb sentence-transformers langchain-community cohere pypdfium2 wikipedia

# Import required libraries
import os
import time
import random
import zipfile
import json

from preprocessing import CHOOSE_P
import sys
sys.modules["sqlite3"] = __import__("pysqlite3")

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import Cohere
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import Document

# Set your OpenAI API key
os.environ["COHERE_API_KEY"] = "6YCEh9PnOi7fELMgBsghd35CF9RnONVqC3ouS647"



# Define Functions to Parse and Answer Questions

def create_answer(extracted_text,q):

    def parse_query(query):
        parts = query.split(":", 1)
        if len(parts) == 2:
            number_part = parts[0].strip()
            question_text = parts[1].strip()
            number = int(''.join(filter(str.isdigit, number_part)))
            return number, question_text
        else:
            return None, query

    def answer_question(query):
        question_number, question_text = parse_query(query)
        docs = retriever.get_relevant_documents(question_text)
        context = "\n\n".join([doc.page_content for doc in docs])
        input_data = {
            "question_number": question_number,
            "question": question_text,
            "context": context
        }
        answer = llm_chain.run(input_data)
        return answer
    # Documents
    all_docs = extracted_text

    # Split Documents into Chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    splitted_docs = text_splitter.split_documents(all_docs)

    # Create Embeddings and Vector Store
    embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

    vectorstore = Chroma.from_documents(
        splitted_docs,
        embedding_model,
        persist_directory='db'
    )
    vectorstore.persist()

    # Initialize the Retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})

    # Initialize the LLM
    llm = Cohere(
        model="command-r-plus-08-2024",
        temperature=0.0,
        max_tokens=256,
        cohere_api_key="6YCEh9PnOi7fELMgBsghd35CF9RnONVqC3ouS647"
    )


    # Define the Prompt Template
    prompt_template = PromptTemplate(
        input_variables=["question_number", "question", "context"],
        template="""
    شما باید به پرسش زیر پاسخ دهید. پاسخ باید به صورت یک دیکشنری شامل یک رشته باشد که به شکل زیر است:

        "answer": "پاسخ شما"

    **توجه:**
    - پاسخ ها حداقل 10 کلمه و حداکثر 20 کلمه باشد
    - فقط یک پاسخ ارائه دهید.
    - از استفاده از 'و' (واو عطف) در پاسخ خودداری کنید.
    - اگر پاسخ نام یک کشور است، آن را به **فارسی** بنویسید.
    - اگر پاسخ یک عبارت اختصاری است، آن را به حروف **انگلیسی** بنویسید.
    - پاسخ باید دقیق و مرتبط با پرسش باشد.

    **پرسش:** {question}

    **متن کمکی:**
    {context}

    **پاسخ:**""",
    )

    # Create the LLM Chain
    llm_chain = LLMChain(llm=llm, prompt=prompt_template)

    # Answer the Questions
    answer = answer_question(q)
    return answer



