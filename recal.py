import numpy as np


class Recal:
    relevants = np.load('results.npy')

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
                        # print(res[0]+"----"+res[1])
                        # print(title + "++++"+item[0])
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
        count = 0
        total = self._calculate_total(results[0])
        for item in results[1]:
            for rel in self.relevants:
                if rel[1] == item:
                    count += 1
        return (count / total) * 100

    def _calculate_total(self, cui):
        total = 0
        for item in self.relevants:
            if item[0] == cui:
                total += 1
        return total
