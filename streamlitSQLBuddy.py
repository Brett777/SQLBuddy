import streamlit as st


#Configure the page title, favicon, layout, etc
st.set_page_config(page_title="SQL Buddy")

def mainPage():
    container1 = st.container()
    col1, col2, col3 = container1.columns([1,3,1])
    container2 = st.container()
    container3 = st.container()

    with col2:
        st.header("SQL Buddy")

    with container2:
        plainEnghlishQuery = st.text_input(label="Describe the query you want to make.")

    with container3:
        sqlQuery = st.text_area(label="Here is your SQL Query", value="select * from yourDatabase.table")





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

