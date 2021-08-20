import streamlit as st
from annotated_text import annotation
import collections
from skillNer.general_params import SKILL_DB


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_skill_extractor():
    # This function will only be run the first time it's called
    import spacy
    from skillNer.skill_extractor_class import SkillExtractor

    from nltk.corpus import stopwords
    from spacy.matcher import PhraseMatcher
    # init params of skill extractor
    print('load model')
    nlp = spacy.load("en_core_web_lg")
    stop_words = set(stopwords.words('english'))
    print('load matcher')
    # init skill extractor
    skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher, stop_words)
    return skill_extractor


def create_ann_list(text, results):
    type_to_color = {'Hard Skill': "#faa", 'Soft Skill': '#afa'}
    text_tokens = text.split(' ')
    annots = {}
    all_res = results['ngram_scored']+results['full_matches']
    ids_done = []
    # create annotations from matches
    for match in all_res:
        id_ = match['skill_id']
        type_ = SKILL_DB[id_]['skill_type']
        span_str = ' '.join([text_tokens[i] for i in match['doc_node_id']])
        annot = annotation(span_str, type_, background=type_to_color[type_],
                           color="#333", margin_left='10px', margin_right='10px', margin_bottom='5px')
        annots[match['doc_node_id'][0]] = annot
        for i in match['doc_node_id']:
            ids_done.append(i)
    # create strs for non annotated text
    for i, token in enumerate(text_tokens):
        if i not in ids_done:
            annots[i] = annotation(token,
                                   color="#fff", background="transparent",  margin_bottom='5px')
    annots_ = collections.OrderedDict(sorted(annots.items())).values()
    return annots_
