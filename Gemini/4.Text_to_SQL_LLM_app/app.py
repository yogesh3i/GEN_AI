import streamlit as st 
import os 
from dotenv import load_dotenv 
import pymysql
import google.generativeai as genai 

# configure the GENAI API KEY 

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load the model and gove the parsona

def get_gemini_response(question,prompt):
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    response = model.generate_content([prompt[0],question])
    return response.text


# function to rertriev the query from the database 
def read_sql_query(sql,db):
    conn = pymysql.connect(host='localhost',user='root',password='Yogesh@123',database='student')
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    return data
    

## Define Your Prompt or creating an parsona 
prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name stu_info and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STU_INFO ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STU_INFO 
    where CLASS="10th"; 
    also the sql code should not have ``` in beginning or end and sql word in output

    """


]


# setting up the UI 

st.set_page_config(page_title="Text to SQL")
st.header("📊 Ask me anything i will annoy your DB🛢️")


question  = st.text_input("Input: ", key="input")
submit = st.button("Send it to DB")

# once the submit is clicked 
if submit:
    query = get_gemini_response(question,prompt)
    print(query)
    response = read_sql_query(query,"stu_info")
    st.subheader("Here is the output🔍 i found: ")
    print(response)
    for row in response:
        st.code(query)
        print(row)
        st.header(row)
        
        
