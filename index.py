
import streamlit as st
from annotated_text import annotated_text, annotation
from utils import load_skill_extractor, create_ann_list


skill_extractor = load_skill_extractor()

st.title('SkillNer Demo')
user_input = st.text_area(
    "Text to annotate", 'We need an expert in esport management. Fluency in both english and french is mandatory!')

annotations = skill_extractor.annotate(user_input)
# print(annotations)
text = annotations['text']
annotations = annotations['results']
annotations_render = create_ann_list(text, annotations)
#job_description = "We need an expert in esport management. Fluency in both english and french is mandatory!"


annotated_text(*annotations_render)
