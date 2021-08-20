
import streamlit as st
from annotated_text import annotated_text, annotation
from utils import load_skill_extractor, create_ann_list, create_dfs
import pandas as pd

skill_extractor = load_skill_extractor()

st.title('SkillNer - Demo')
st.markdown('## Enter a job posting text :')
user_input = st.text_area(
    "Text to annotate", 'We need an expert in esport management. Fluency in both english and french is mandatory!')

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
