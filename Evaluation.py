import numpy as np
import pandas as pd


class Evaluation:
    relevants = np.load('results.npy')
    relevants_df = pd.DataFrame(relevants)
    relevants_df.columns =  ['topic_id','results']
    group = relevants_df.groupby(by='topic_id')

    def recal(self, expandeds):
        self._expandeds = expandeds
        results = np.load('results.npy')
        output = []
        for i in range(len(self._expandeds)):
            title = self._expandeds[i, 0]
            total = 0.0
            for res in results:
                if res[0] == title:
                    total += 1
            print("total relevant for title " + title + " is : " + str(total))
            count = 0.0
            for item in self._expandeds[i, 1]:
                for res in results:
                    if res[0] == title:
                        if res[1] == item:
                            count += 1
            print("recall at 1000 for title " + title + " is : " + str(100 * (count / total)))
            tempt = []
            tempt.append(title)
            tempt.append((count / total))
            output.append(tempt)
        sum = 0
        for item in output:
            sum += item[1]
        print("avg recall is : " + str((sum / len(output))))
        arr = np.array(output, dtype=object)
        np.save('output_Recalls', arr)
        return arr

    def recall_for_dataset(self, results):
        topic = results[0]
        res = results[1]
        total = self.calculate_total(topic)
        temp = self.relevants_df.loc[self.group.groups[topic]]
        count = temp.isin(res)
        count = count.results
        count = count.value_counts()[True]
        return (count/total)*100

    def percision(self, results):
        topic = results[0]
        res = results[1]
        total = len(res)
        temp = self.relevants_df.loc[self.group.groups[topic]]
        count = temp.isin(res)
        count = count.results
        count = count.value_counts()[True]
        return (count / total) * 100

    def calculate_total(self, cui):
        return  len(self.group.groups[cui])




