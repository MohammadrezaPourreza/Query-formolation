
import pandas as pd
from pandas import DataFrame
from pymed import PubMed
from expander import Expander
from utils import tag_sentence_stanford



class Search:
    def __init__(self, expander: Expander):
        self._expander = expander

    def query(self, query: str, max_records: int = 1000, expand=True):
        if expand:
            return self._expand_and_search(query, max_records)
        else:
            return self._query_no_expansion(query, max_records)

    def _expand_and_search(self, query: str, max_records: int = 100):
        expanded_query = self._expander.expand(query, 5)
        return self.search_pubmed(expanded_query, max_records)

    def _query_no_expansion(self, query: str, max_records: int = 100):
        return self.search_pubmed(query, max_records)

    def search_pubmed(self, query: str, max_records=10000) -> DataFrame:
        pubmed = PubMed(tool="PubMedSearcher_hamid", email="s.hamid.sajjadi@gmail.com")

        search_term = query
        print("query : "+query)
        number_of_articles = pubmed.getTotalResultsCount(query)

        print("total result for query is : "+str(number_of_articles))
        if number_of_articles > 100000:
            number_of_articles = 100000
        article_ids = pubmed._getArticleIds(query=query, max_results=number_of_articles)
        # results = pubmed.query(search_term, max_results=number_of_articles)
        # articleList = []
        articleInfo = []

        # for article in results:
        #     articleDict = article.toDict()
        #     articleList.append(articleDict)

        # Generate list of dict records which will hold all article details that could be fetch from PUBMED API
        for article in article_ids:
            # pubmedId = article["pubmed_id"].partition("\n")[0]
            # Append article info to dictionary
            # articleInfo.append({u"pubmed_id": pubmedId, u"title": article["title"]})
            articleInfo.append(article)
        #
        # Generate Pandas DataFrame from list of dictionaries
        articlesPD = pd.DataFrame.from_dict(articleInfo)
        # print(articlesPD)
        # print(articleInfo)
        return articleInfo , number_of_articles
