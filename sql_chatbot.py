#------------------------------------------
# source:
# Build Your Own Sql Chatbot with Langchain and Streamlit
# https://ofeng.org/posts/langchain-streamlit-build-your-own-sql-chat/

from langchain.sql_database import SQLDatabase
from langchain.llms import OpenAI
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
import streamlit as st

#------------------------------------------

url = "https://drive.google.com/file/d/1oyiIcBY8vw4qAvaZKxIHtaGpz5V0Oj8k/view?usp=drive_link"
url2 = "https://www.pinecone.io/"

multiline_str1 = """
- created by Glen Brauer, Business Analyst in AAE (glenb@sfu.ca) \n

- PROBLEM: reports can take days or weeks to be developed manually\n

- SOLUTION: provide a self-serve report generator\n"""

multiline_str2 = """- leverages AI to query this [sample database](%s)""" % url

multiline_str3 ="""\n - sample prompt:\n Which customers located in San Francisco have purchased products? 

- scroll down to see its thoughts, actions and results

\n"""



with st.expander("Show/hide details"):
    st.write(multiline_str1 + multiline_str2 + multiline_str3)


    # st.markdown("- created by Glen Brauer, Business Analyst in AAE")
    # st.markdown("- demonstrates the ability to leverage ChatGPT and vector storage to access documents")
    # st.markdown("- sample question: 'How can I create a marketing effort?'")
    #
    # url = "https://drive.google.com/drive/u/0/folders/1gTD-OiqH5Bg3-ZqVuur9q8h-AGIzOlB7"
    #
    # st.write("- documents which have been ingested are located [here](%s)" % url)

#------------------------------------------
st.header("SFU Report Chatbot 1.0 (beta)")

st.chat_input(placeholder="Enter your prompt here...")


api_key = st.secrets["OPENAI_API_KEY"]  # st.text_input("api_key")
db_string = st.secrets["DB_STRING"] # st.text_input("db_string")

if api_key:
    db = SQLDatabase.from_uri(st.secrets["DB_STRING"])
    toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0, openai_api_key=st.secrets["OPENAI_API_KEY"]))
    agent_executor = create_sql_agent(
        llm=OpenAI(temperature=0, streaming=True, openai_api_key=st.secrets["OPENAI_API_KEY"]),
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )
else:
    st.write("Please input openai_api_key")

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent_executor.run(prompt, callbacks=[st_callback])

        st.write(response)

#------------------------------------------
