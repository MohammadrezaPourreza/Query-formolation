from expander import Expander
from gensim.models import KeyedVectors
from search import Search
from recal import Recal

class Dataset:
    def __init__(self, kv: KeyedVectors):
        self._kv = kv
    def returndataset(self,topic,query,topn,conjunction: str = " "):
        self.expander = Expander(self._kv)
        cuis = self.expander._expand_term(query,topn)
        output = []
        result = self.search_sentence(query)
        output.append([query,result])
        for key in cuis.keys():
            for tupple in cuis[key]:
                newQ = query+conjunction+tupple[1]
                result = self.search_sentence(newQ)
                if result>0:
                    output.append([newQ,result])
        recal = Recal()
        for expansion in output:
            recal.recal([topic,expansion[1]])
    def search_sentence(self , query):
        searcher = Search(self.expander)
        return searcher._search_pubmed(query=query)