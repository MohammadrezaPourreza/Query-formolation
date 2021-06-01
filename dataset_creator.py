from expander import Expander
from gensim.models import KeyedVectors
from search import Search
from recal import Recal
import pandas as pd


class Dataset:
    def __init__(self, kv: KeyedVectors):
        self._kv = kv

    def return_dataset(self, topic, query, topn, conjunction: str = " "):
        self.expander = Expander(self._kv)
        searcher = Search(self.expander)
        try:
            cuis = self.expander._expand_term(query, topn)
        except Exception as e:
            return None
        output = []
        result = self.search_sentence(query, searcher)
        output.append([query, result])
        for key in cuis.keys():
            for tupple in cuis[key]:
                if tupple[1] is None:
                    continue
                newQ = query + conjunction + tupple[1]
                result = self.search_sentence(newQ, searcher)
                if len(result) > 0:
                    output.append([newQ, result])

        recal = Recal()
        for expansion in output:
            rec = recal.recall_for_dataset((topic, expansion[1]))
            expansion.append(rec)

        output = pd.DataFrame(output)
        output.columns = ['query', 'results', 'recall']
        return output

    def search_sentence(self, query, searcher):

        return searcher._search_pubmed(query=query)
