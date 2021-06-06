from expander import Expander
from gensim.models import KeyedVectors
from search import Search
from recal import Recal
import pandas as pd


class Dataset:

    def __init__(self, kv: KeyedVectors):
        self._kv = kv
        self.expander = Expander(self._kv)

    def return_dataset(self, topic, query, topn, conjunction: str = "OR"):
        searcher = Search(self.expander)
        try:
            cuis = self.expander.expand_term(query, topn)
        except Exception as e:
            return None
        output = []
        result = self.search_sentence(query, searcher)
        output.append([query, result, ''])
        for key in cuis.keys():
            for item in cuis[key]:
                if item[1] is None:
                    continue
                newQ = query + " " + conjunction + " " + item[1]
                result = self.search_sentence(newQ, searcher)
                if len(result) > 0:
                    output.append([newQ, result, item[1]])

        recal = Recal()
        for expansion in output:
            rec = recal.recall_for_dataset((topic, expansion[1]))
            perc = recal.percision((topic, expansion[1]))
            expansion.append(rec)
            expansion.append(perc)
            expansion.append(topic)

        output = pd.DataFrame(output)
        output.columns = ['query', 'results', 'expanded_term', 'recall', 'precision', 'topic_id']
        output = output.drop(['results'], axis=1)
        return output

    def search_sentence(self, query, searcher):

        return searcher.search_pubmed(query=query)
