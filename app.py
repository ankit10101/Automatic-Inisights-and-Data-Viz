import streamlit as st
import pandas as pd
from lida import Manager, TextGenerationConfig , llm  
from PIL import Image
from io import BytesIO
import base64
from dotenv import load_dotenv
import os
import openai

# Configuring the OpenAI API Key
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# To convert charts into images, so that they can be displayed on Stremlit front-end
def base64_to_image(base64_string):
    # Decode the base64 string
    byte_data = base64.b64decode(base64_string)
    # Use BytesIO to convert the byte data to image
    return Image.open(BytesIO(byte_data))

# Streamlit App Code

st.set_page_config(
    page_title="Automatic Insights and Visualization App",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.header("Automatic Insights and Visualization 🤖")

menu = st.sidebar.selectbox("Choose an Option", ["Automatic Insights", "Query based Graph"])

if menu == "Automatic Insights":
    st.subheader("Generate Automatic Insights")
    uploaded_file = st.file_uploader("Choose a csv file")
    if uploaded_file is not None:
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)
        btn = st.button("Generate Suggestions", type = "primary")

        if btn: 
            lida = Manager(text_gen = llm("openai"))
            textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-3.5-turbo-0301", use_cache=True)
            summary = lida.summarize(dataframe, summary_method="default", textgen_config=textgen_config)  
            goals = lida.goals(summary, n=5, textgen_config=textgen_config)

            i = 0
            library = "seaborn"
            imgs = []
            textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
            for i in range(len(goals)):
                charts = lida.visualize(summary=summary, goal=goals[i], textgen_config=textgen_config, library=library)
                # print(charts)  
                # charts[0]
                img_base64_string = charts[0].raster
                img = base64_to_image(img_base64_string)
                imgs.append(img)

            tab1, tab2, tab3, tab4, tab5 = st.tabs(["Goal 1", "Goal 2", "Goal 3", "Goal 4", "Goal 5"])

            with tab1:
                st.header("Goal 1")
                goals[0].question
                st.image(imgs[0])

            with tab2:
                st.header("Goal 2")
                goals[1].question
                st.image(imgs[1])

            with tab3:
                st.header("Goal 3")
                goals[2].question
                st.image(imgs[2])
            
            with tab4:
                st.header("Goal 4")
                goals[3].question
                st.image(imgs[3])
            
            with tab5:
                st.header("Goal 5")
                goals[4].question
                st.image(imgs[4])


elif menu == "Query based Graph":
        st.subheader("Query based graphs")
        uploaded_file = st.file_uploader("Choose a csv file")
        if uploaded_file is not None:
            dataframe = pd.read_csv(uploaded_file)
            st.write(dataframe)
            user_query = st.text_input("Enter your data query")
            btn = st.button("Generate Graph", type = "primary")

            if btn: 
                lida = Manager(text_gen = llm("openai"))
                textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-3.5-turbo-0301", use_cache=True)
                summary = lida.summarize(dataframe, summary_method="default", textgen_config=textgen_config)  
                library = "seaborn"
                charts = lida.visualize(summary=summary, goal=user_query, textgen_config=textgen_config, library=library)
                img_base64_string = charts[0].raster
                img = base64_to_image(img_base64_string)
                
                st.text(user_query)
                st.image(img)
