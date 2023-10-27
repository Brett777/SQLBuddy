import streamlit as st
import snowflake.connector
import pandas as pd
import os
import openai
openai.api_key = os.getenv("OPENAI_KEY")

# snowflakeSQL = """-- This query will count the number of unique customers from California (CA)
# SELECT COUNT(DISTINCT "CustomerID")
# FROM "DEMO"."SAFER_LC"."LENDING_CLUB_PROFILE"
# WHERE "addr_state" = 'CA';"""

#Configure the page title, favicon, layout, etc
st.set_page_config(page_title="Data Bot")

def getSQL(queryDescription):
    #queryDescription = "how many rows are in the customer table?"
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        # model="gpt-3.5-turbo",
        temperature=0.2,
        messages=[
            {"role": "system",
             "content": """
                        You are an expert in Snowflake SQL.
                        The user will ask for your assistance in retrieving data from Snowflake. 
                        Your response shall be the Snowflake SQL code to query the needed data. 
                        Your code shall be clean, concise and executable. 
                        Include comments to explain your code.
                        Only respond with executable Snowflake SQL and nothing else. Anything other that Snowflake SQL must be commented. 
                        When referencing column names, wrap them in double-quotes.                       
                             
                        Database name: DEMO
                        Schema: SAFER_LC
                        Table1: LENDING_CLUB_PROFILE
                        Table1 columns:
                        'CustomerID' VARCHAR(16777216),
                        'loan_amnt' NUMBER(38,0),
                        'funded_amnt' NUMBER(38,0),
                        'term' VARCHAR(16777216),
                        'int_rate' VARCHAR(16777216),
                        'installment' FLOAT,
                        'grade' VARCHAR(16777216),
                        'sub_grade' VARCHAR(16777216),
                        'emp_title' VARCHAR(16777216),
                        'emp_length' VARCHAR(16777216),
                        'home_ownership' VARCHAR(16777216),
                        'annual_inc' VARCHAR(16777216),
                        'verification_status' VARCHAR(16777216),
                        'purpose' VARCHAR(16777216),
                        'zip_code' VARCHAR(16777216),
                        'addr_state' VARCHAR(16777216)
                        Table2: LENDING_CLUB_TARGET
                        Table2 columns:
                        'CustomerID' VARCHAR(16777216),
                        'BadLoan' VARCHAR(16777216),
                        'date' DATE
                        Table3: LENDING_CLUB_TRANSACTIONS     
                        Table3 columns:
                        'CustomerID' VARCHAR(16777216),
                        'AccountID' VARCHAR(16777216),
                        'Date' DATE,
                        'Amount' VARCHAR(16777216),
                        'Description' VARCHAR(16777216)             
                        """
             },
            {"role": "user", "content":queryDescription}
        ]
    )
    return completion.choices[0].message.content

def sayAnswer(query, answer):
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        # model="gpt-3.5-turbo",
        temperature=0.2,
        messages=[
            {"role": "system",
             "content": """
                        Your job is to form a complete English sentence as an answer to the user's question.
                        You will be provided with the user's question, as well as some data that supports the answer.
                        Analyze the data, and provide a short answer in a sentence or two. 
                            """
             },
            {"role": "user", "content": "question: " + query + " Supporting Data: " + answer}
        ]
    )
    return completion.choices[0].message.content


def executeSnowflakeQuery(snowflakeSQL):
    con = snowflake.connector.connect(
        user='DATAROBOT',
        password='D@t@robot',
        account='datarobot_partner',
        warehouse='DEMO_WH',
        database='DEMO',
        schema='SAFER_LC'
    )
    cursor = con.cursor()
    cursor.execute(snowflakeSQL)
    results = cursor.fetchall()
    con.close()
    return results

def mainPage():
    container1 = st.container()
    container2 = st.container()
    container3 = st.container()
    if "generateQueryButtonState" not in st.session_state:
        st.session_state["generateQueryButtonState"] = False
        st.session_state["executeQueryButtonState"] = False
        st.session_state["sqlQuery"] = ""
        st.session_state["sqlQueryUserText"] = ""
        st.session_state["queryResult"] = ""

    with container1:
        st.header("Data Bot")

    with container2:
        plainEnghlishQuery = st.text_input(label="Ask a question about the data")
        generateQueryButton = st.button("Get Answer")
        if generateQueryButton:
            st.session_state["generateQueryButtonState"] = True
            with st.spinner("Generating Query..."):
                st.session_state["sqlQuery"] = getSQL(plainEnghlishQuery)

            with container3:
                st.code(st.session_state["sqlQuery"], language="sql")
                with st.spinner("Executing Query..."):
                    st.session_state["queryResult"] = executeSnowflakeQuery(str(st.session_state["sqlQuery"]))
                    st.write(st.session_state["queryResult"])
                    st.write(sayAnswer(str(plainEnghlishQuery), str(st.session_state["queryResult"])))






#Main app
def _main():
    hide_streamlit_style = """
    <style>
    # MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) # This let's you hide the Streamlit branding
    mainPage()

if __name__ == "__main__":
    _main()

