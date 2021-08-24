
import streamlit as st
from annotated_text import annotated_text, annotation
from utils import load_skill_extractor, create_ann_list, create_dfs
import pandas as pd

skill_extractor = load_skill_extractor()

st.title('SkillNer - Demo')
st.markdown('## Enter a job posting text :')
default_text = '''
You are a Python Developer with a solid experience in Web development and  esx
and have a thoughtful expatriation and manage project . You're passionate and powerful.
You are recognized for your ability to evolve within a team and around common projects
and you easily adapt in a new environment. javascript and node and french and english
'''
user_input = st.text_area(
    "Text to annotate", default_text, height=200)

annotations = skill_extractor.annotate(user_input)
# print(annotations)
text = annotations['text']
annotations = annotations['results']

annotations_render = create_ann_list(text, annotations)


st.markdown('## Entity linking : ')
st.markdown('-----------')
annotated_text(*annotations_render)
st.markdown('-----------')
f_df, s_df = create_dfs(annotations)
st.markdown('## Entity recognition : ')
st.markdown('> Full matches ')


f_df
st.markdown('> Sub matches ')
s_df
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
