import streamlit as st
import tempfile

from preprocessing import CHOOSE_P
from model import create_answer

st.title("P&Q")

option = st.radio("یک گزینه را انتخاب کنید:", ["pdf", "web", "wiki"])

result = None

if option == "pdf":
    uploaded_file = st.file_uploader("یک فایل PDF انتخاب کنید", type=["pdf"])
    if uploaded_file is not None:
      # Create a temporary file to store the uploaded PDF
      with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(uploaded_file.read())
        temp_pdf_path = temp_pdf.name
      result = CHOOSE_P("pdf",temp_pdf_path)

elif option == "web":
    url = st.text_input("لینک یک سایت را وارد کنید:")
    if url:
        result = CHOOSE_P("web",url)

elif option == "wiki":
    wiki_url = st.text_input("لینک یک صفحه ویکیپدیا را وارد کنید:")
    if wiki_url:
        result = CHOOSE_P("wiki",wiki_url)

question = st.text_input("سوال خود را وارد کنید")

if question and result:
    final_output = create_answer(result,question)
    st.write(final_output)
