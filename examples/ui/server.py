import os

import requests
import streamlit as st
from dotenv import load_dotenv
from streamlit_modal import Modal

import webbrowser as wb
page_params = st.experimental_get_query_params()

#-------->>>>>>>>
#Author: Raghu Kodanda - Imported sys to include knowledgeGraph
## knowledgeGraph.showKwGraph enables to Display the response from LLM App as a Knowedge Grap using graphviz 
import sys
import graphviz
from knowledgeGraph import showKwGraph
#<<<<<<<<<<--------

with st.sidebar:
    st.markdown(
        "[View the source code on GitHub](https://github.com/pathwaycom/llm-app)"
    )

# Load environment variables
load_dotenv()
api_host = os.environ.get("PATHWAY_REST_CONNECTOR_HOST", "127.0.0.1")
api_port = int(os.environ.get("PATHWAY_REST_CONNECTOR_PORT", 8080))


# Streamlit UI elements
st.title("LLM App")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

#-------->>>>>>>>
#Author: Raghu Kodanda - Imported sys to include knowledgeGraph
## 
##Maintaining Click status of button to hide graph upon click
if 'clicked' not in st.session_state:
    st.session_state.clicked = False

if st.session_state.clicked:
    st.session_state.clicked = False
#<<<<<<<<<<--------


#-------->>>>>>>>
#Author: Raghu Kodanda - Imported sys to include knowledgeGraph
## 
##showGraph Helper method to prepare & invoke knowledgeGraph.showKwGraph
def showGraph(gpText):
    print("Showing Grpah Here ...")
    #showKwGraph(gpText)

    if page_params:
        text = page_params.get("text")[0]
        st.write(text)
        print("Page Params")
    else:
        #text = st.text_input("Enter Text")
        text = "KnowledgeGraph"
        btn = st.button("Hide the Graph")
        #st.graphviz_chart(showGraph(response))
        #showGraph(response)
        showKwGraph(response)
        print("Page Parms else")
        if btn:
            print("Button if")
            st.markdown(f"http://localhost:8501/?text={text}")
            wb.open_new_tab(f"http://localhost:8501/?text={text}")
#if page_params:
#   text = page_params.get("text")[0]
#   st.write(text)

#else:
   #text = st.text_input("Enter Text")
#   text = "KnowledgeGraph"
#   btn = st.button("Click to open")

#   if btn:
#       st.markdown(f"http://localhost:8501/?text={text}") 
#       wb.open_new_tab(f"http://localhost:8501/?text={text}")
#<<<<<<<<<<--------


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# React to user input
if prompt := st.chat_input("How can I help you today?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    url = f"http://{api_host}:{api_port}/"
    data = {"query": prompt, "user": "user"}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        response = response.json()
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        showGraph(response)
        
        #if page_params:
        #     text = page_params.get("text")[0]
        #     st.write(text)
        #     print("Page Params")
        #else:
             #text = st.text_input("Enter Text")
        #     text = "KnowledgeGraph"
        #     btn = st.button("Hide the Graph")
             #st.graphviz_chart(showGraph(response))
             #showGraph(response)
        #     print("Page Parms else")
        #     if btn:
        #          print("Button if")
        #          st.markdown(f"http://localhost:8501/?text={text}")
        #          wb.open_new_tab(f"http://localhost:8501/?text={text}")

    else:
        st.error(
            f"Failed to send data to Discounts API. Status code: {response.status_code}"
        )
