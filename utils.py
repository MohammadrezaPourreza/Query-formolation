import os
import re
import string
from os import getenv, path
from typing import Tuple, List

import nltk
from dotenv import load_dotenv
from gensim.models import KeyedVectors
from nltk.corpus import stopwords
from nltk.parse.corenlp import CoreNLPServer, CoreNLPParser
from quickumls import QuickUMLS

from constant import ACCEPTED_SEMTYPES

stop_words = stopwords.words('english')

load_dotenv()

quickumls_fp = "../SLR/QuickUMLS"
matcher = QuickUMLS(
    quickumls_fp,
    overlapping_criteria="score",
    threshold=0.85,
    similarity_name="cosine",
    accepted_semtypes=ACCEPTED_SEMTYPES,
)

CORE_NLP_DIR = "D:\stanford-corenlp-4.2.2\stanford-corenlp-4.2.2"
CORE_NLP_VER = "4.2.2"
try:
    server = CoreNLPServer(path.join(CORE_NLP_DIR, "stanford-corenlp-{}.jar".format(CORE_NLP_VER)),
                           path.join(CORE_NLP_DIR, "stanford-corenlp-{}-models.jar".format(CORE_NLP_VER)))
    server.start()
except:
    print('server is already running')


def remove_parenthesis(s: str) -> str:
    """Given an string, removes all the text inside `()` and `[]`

    Args:
        s (str): [description]

    Returns:
        str: `s` without `()` or `[]`
    """
    return re.sub("[\(\[].*?[\)\]]", "", s)


def extract_cui(text: str) -> Tuple[List[str], List[str]]:
    """This function uses `quickumls` package to find and extract CUIs (UMLS Concepts) from a text

    Args:
        text (str): [description]

    Returns:
        Tuple[List[str], List[str]]: returns two list, first one is CUIs, second list is the cuis corresponding terms
    """

    matches = matcher.match(text, best_match=True, ignore_syntax=False)
    cuis = []
    terms = []
    for match in matches:
        for concept in match:
            if concept["preferred"]:
                cuis.append(concept["cui"])
                terms.append(concept["term"])
    return cuis, terms


def tag_sentence(sentence: str, acceptable_tags=None):
    if acceptable_tags is None:
        acceptable_tags = ['NN']
    text = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(text)
    return [token[0] for token in tagged if token[1] in acceptable_tags]


def tag_sentence_stanford(text: str):
    text = ' '.join([t for t in text.split() if t not in stop_words])
    ACCEPTED_LABELS = ['ROOT', 'FRAG', 'S', 'NP']

    def traverse_tree(tree):
        leaves = []
        for subtree in tree:
            if type(subtree) == nltk.tree.Tree:
                if subtree.label() in ACCEPTED_LABELS:
                    leaves.append(traverse_tree(subtree))
                elif subtree.label() and subtree.label() not in string.punctuation:
                    # leaves.append(' '.join(subtree.leaves()))
                    leaves.extend(subtree.leaves())
            else:
                leaves.append(subtree)
        return leaves

    # with CoreNLPServer(path.join(STANFORD, "stanford-corenlp-4.2.2.jar"),
    #                    path.join(STANFORD, "stanford-corenlp-4.2.2-models.jar")
    #                    ):

    parser = CoreNLPParser(url="http://localhost:9000")
    root = next(parser.raw_parse(text))
    parsed = traverse_tree(root)

    return concat_strings(parsed)


def concat_strings(l):
    this_str = ''
    all_strs = []
    for node in l:
        if type(node) == str:
            this_str += ' ' + node
        else:
            all_strs.extend(concat_strings(node))
    if this_str:
        all_strs.append(this_str.strip())
    return all_strs


def load_cui_to_biovec():
    f = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'cui_to_wordvec', 'cui_biowordvec')
    return KeyedVectors.load(f)

def load_cui_to_vec():
    f = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'cui2vec', 'cui2vec_emmbeding')
    return KeyedVectors.load(f)
if __name__ == "__main__":
    import timeit

    start = timeit.default_timer()
    print(tag_sentence_stanford(
        "Human papillomavirus testing versus repeat cytology for triage of minor cytological cervical lesions"))
    stop = timeit.default_timer()
    print('Time: ', stop - start)

    # print(json.dumps(,indent=4))
