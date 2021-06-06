from pandas import DataFrame
from gensim.models import KeyedVectors
from dataset_creator import Dataset
from expander import Expander
from recal import Recal
from search import Search
import numpy as np
import pandas as pd
from utils import load_cui_to_biovec
from utils import load_cui_to_vec

sum_recall = 0
count = 0

# java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

kv = load_cui_to_biovec()
# kv = load_cui_to_vec()
expander = Expander(kv)
searcher = Search(expander)

# q = "Anti‐vascular endothelial growth factor for neovascular age‐related macular degeneration"
np_load_old = np.load
np.load = lambda *a, **k: np_load_old(*a, allow_pickle=True, **k)
topics = np.load('topics.npy')
# q = "fever"
# df: DataFrame = searcher.query(q, expand=True)
# df = df.astype({"pubmed_id": "int64"})
output = None
for i in range(1):
    temp = []
    q = topics[i, 1]
    dataset_creator = Dataset(kv)

    df = dataset_creator.return_dataset(topics[i, 0], q, 0, "OR")
    if df is not None:
        if i != 0:
            output = pd.concat([output, df])
        else:
            output = df
    # try:
    #     result = searcher.query(q, expand=True)
    #     temp.append(topics[i, 0])
    #     temp.append(result)
    #     output.append(temp)
    #     print("current successful topic : " + str(i))
    # except Exception as e:
    #     print("current failed topic : " + str(i))
# expanded = np.array(output, dtype=object)
# rec = Recal()
# ultimate_res = rec.recal(expanded)
# output.to_csv('dataset.csv')
