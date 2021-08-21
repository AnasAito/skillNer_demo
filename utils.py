import sys
import subprocess
import streamlit as st
from annotated_text import annotation
import collections

import pandas as pd
import os


def grouper(iterable):
    prev = None
    group = []
    for item in iterable:
        if not prev or item - prev <= 1:
            group.append(item)
        else:
            yield group
            group = [item]
        prev = item
    if group:
        yield group


token = st.secrets['skillner_token']


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def load_skill_extractor():
    # This function will only be run the first time it's called
    import spacy
    try:
        from skillNer.skill_extractor_class import SkillExtractor
        from skillNer.general_params import SKILL_DB
    except:
        os.system('cd')
        package = 'git+https://' + token+'@github.com/AnasAito/SkillNER.git'
        install(package)
        from skillNer.skill_extractor_class import SkillExtractor
        from skillNer.general_params import SKILL_DB

    from spacy.matcher import PhraseMatcher
    # init params of skill extractor
    print('load model')

    nlp = spacy.load('en_core_web_lg')

    print('load matcher')
    # init skill extractor
    skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher, ('test'))
    return skill_extractor


def create_ann_list(text, results):
    try:
        from skillNer.general_params import SKILL_DB
    except:
        token = st.secrets['skillner_token']
        pip_cmd = 'pip install ' + 'git+https://' + \
            token+'@github.com/AnasAito/SkillNER.git'
        os.system(pip_cmd)
        from skillNer.general_params import SKILL_DB

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
                           color="#333", margin='2px')
        annots[match['doc_node_id'][0]] = annot
        for i in match['doc_node_id']:
            ids_done.append(i)
    # create strs for non annotated text
    non_match_ids = [i for i, _ in enumerate(text_tokens) if i not in ids_done]
    dict_ = dict(enumerate(grouper(non_match_ids), 1))
    for v in dict_.values():
        span = ' '.join([text_tokens[i] for i in v])
        annots[v[0]] = span
        # annotation(token,color="#fff", background="transparent",)
    print(dict_)
    print('-----')
    # print(collections.OrderedDict(sorted(annots.items())))
    annots_ = collections.OrderedDict(sorted(annots.items())).values()
    return annots_


def create_dfs(results):
    try:
        from skillNer.general_params import SKILL_DB
    except:
        token = st.secrets['skillner_token']
        pip_cmd = 'pip install ' + 'git+https://' + \
            token+'@github.com/AnasAito/SkillNER.git'
        os.system(pip_cmd)
        from skillNer.general_params import SKILL_DB

    f_matches = results['full_matches']
    f_arr = []
    for match in f_matches:
        id_ = match['skill_id']
        full_name = SKILL_DB[id_]['skill_name']
        type_ = SKILL_DB[id_]['skill_type']
        f_arr.append([id_, full_name, type_])
    s_matches = results['ngram_scored']
    s_arr = []
    for match in s_matches:
        id_ = match['skill_id']
        full_name = SKILL_DB[id_]['skill_name']
        type_ = SKILL_DB[id_]['skill_type']
        score = match['score']
        s_arr.append([id_, full_name, type_, score])
    full_df = pd.DataFrame(
        f_arr, columns=['skill id', 'skill name', 'skill type'])
    sub_df = pd.DataFrame(
        s_arr, columns=['skill id', 'skill name', 'skill type', 'score'])
    return full_df, sub_df
