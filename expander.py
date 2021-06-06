from abc import ABC, abstractmethod
from typing import Tuple, List, Dict

from gensim.models import KeyedVectors

from db import get_cui_str
from utils import extract_cui, load_cui_to_biovec, tag_sentence_stanford


class IExpander(ABC):
    @abstractmethod
    def expand(self, query: str, topn=10) -> str:
        pass


class Expander(IExpander):
    def __init__(self, kv: KeyedVectors):
        self._kv = kv

    def _expand_cui(self, cui: str, topn):
        return self._kv.most_similar(positive=cui, topn=topn)

    def expand_term(self, phrase: str, topn=10) -> Dict[str, List[Tuple[str, str]]]:
        """
        This function, extracts CUI from the term using quickumls and 
        :param phrase : str
        :param topn : int, optional
        :return: dictionary of cui terms in the phrase with list of their corresponding similar words

            example:
            { "human papillomavirsu" : [('C1628028', 'Mupapillomavirus'), ....]
        """
        cui, terms = extract_cui(phrase)
        final_similars = {}
        for c, term in zip(cui, terms):
            similars: list[tuple[str, float]] = self._kv.most_similar(positive=c, topn=topn)
            final_similars[term] = [(similar[0], get_cui_str(similar[0])) for similar in similars]
        return final_similars

    def expand(self, query: str, topn=10) -> str:
        """
        This function finds Noun phrases in the query and expand terms in those noun phrases (discarding other parts of query)
        every term is joined by their similar terms using OR
        terms in a noun phrase (which are already ORed by their similar words) are then joined by AND
        and then finally this noun phrases are joined by OR


        :param query: query to be expanded
        :param topn: number of similar terms added to query for each cui term
        :return: expanded query
        """
        nouns: list[str] = tag_sentence_stanford(query)
        and_clauses = []
        for noun in nouns:
            expanded_noun = self.expand_term(noun, topn)
            or_clauses = []
            for key, value in expanded_noun.items():
                or_clause = ' OR '.join(['"{}"'.format(v[1]) for v in value])
                or_clause = key + ' OR ' + or_clause
                or_clauses.append(or_clause)
            and_clauses.append(' AND '.join(["({})".format(or_clause) for or_clause in or_clauses]))
        expanded_query = ' OR '.join(["({})".format(and_clause) for and_clause in and_clauses if and_clause])
        return expanded_query


if __name__ == '__main__':
    kv = load_cui_to_biovec()
    expander = Expander(kv)

    expanded: str = expander.expand('fever')
    print(expanded)
