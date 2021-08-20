import streamlit as st
from annotated_text import annotated_text, annotation

st.title('SkillNer Demo')
user_input = st.text_area("Text to annotate", 'enter a job description ... ')

annotated_text(
    "Hello ",
    annotation("world!", "HARD SKILL", background="#8ef",
               color="#000",  margin_left='10px', margin_right='10px', margin_bottom='5px'),
    "Hello ",
    annotation("world!", "noun", background="#ddd",
               color="#333", margin_left='10px', margin_right='10px', margin_bottom='5px'),
    "Hello ",

)
