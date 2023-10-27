import streamlit as st
import os
import openai
openai.api_key = os.getenv("OPENAI_KEY")

#Configure the page title, favicon, layout, etc
st.set_page_config(page_title="SQL Buddy")

def getSQL(queryDescription):
    #queryDescription = "how many rows are in the customer table?"
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        # model="gpt-3.5-turbo",
        temperature=0.2,
        messages=[
            {"role": "system",
             "content": """
                        You are a SQL expert.
                        The user will ask for your assistance retrieving data. 
                        Your responses shall be the SQL code to query the data needed by the user. 
                        Your code should be clean, concise and readable. 
                        Include comments to explain your code.
                        Only respond with SQL.
                        The system is Snowflake.      
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


def mainPage():
    container1 = st.container()
    col1, col2, col3 = container1.columns([1,3,1])
    container2 = st.container()
    container3 = st.container()

    with col2:
        st.header("SQL Buddy")

    with container2:
        plainEnghlishQuery = st.text_input(label="Describe the query you want to make.")
        submitQueryButton = st.button("Generate SQL")
        if submitQueryButton:
            sqlQuery = getSQL(plainEnghlishQuery)

    with container3:
        sqlQueryUserText = st.text_area(label="Here is your SQL Query", value=sqlQuery)





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

