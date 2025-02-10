import time
import random

from langchain.document_loaders import PyPDFium2Loader, WebBaseLoader, WikipediaLoader

# Load the PDF File and Preprocess

# Apply preprocessing to fix character issues
def preprocess_pdf_docs(docs):
    for doc in docs:
        text = doc.page_content
        # Replace incorrect characters with the correct ones
        text = text.replace('ͷ', 'ک')
        text = text.replace(chr(8206), '')
        text = text.replace(chr(8207), '')
        text = text.replace(chr(876) + ' ', 'ی ')
        text = text.replace(chr(876) + chr(13), 'ی ')
        # Add more replacements if needed
        doc.page_content = text
    return docs

def PDF_P(url):
    # Load the PDF file
    pdf_loader = PyPDFium2Loader(url)
    pdf_docs = pdf_loader.load()

    # Ensure pdf_docs is a list
    if not isinstance(pdf_docs, list):
        pdf_docs = [pdf_docs]
    pdf_docs = preprocess_pdf_docs(pdf_docs)
    return pdf_docs

# Load the Web Page Content
def WEB_P(url):
    web_loader = WebBaseLoader(url)
    web_docs = web_loader.load()

    # Ensure web_docs is a list
    if not isinstance(web_docs, list):
        web_docs = [web_docs]
    return web_docs

# Load Wikipedia Pages
def WIKI_P(url):
    wiki_titles = url.split(",")
    wiki_docs = []

    for title in wiki_titles:
        try:
            loader = WikipediaLoader(query=title, load_max_docs=1, lang='fa')
            docs = loader.load()
            wiki_docs.extend(docs)
        except Exception as e:
            print(f"Error loading {title}: {e}")
        # Sleep to respect API rate limits
        time.sleep(random.uniform(1, 3))
    return wiki_docs

def CHOOSE_P(p,url):
    if p == "pdf":
        result = PDF_P(url)
    elif p == "web":
        result = WEB_P(url)
    elif p == "wiki":
        result = WIKI_P(url)
    return result
      
