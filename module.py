import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import time
import itertools

rank = ["0.01-60","60-160","160-270","270-458","458-700","700-1200","1200-2399","2399-1560035"]
# bins=[0, 60, 160,270,458,700,1200,2399,float('Inf')]

classes = ["0.01-989","990-4723","4724-9729","9730-16753","16754-29419","29420-57398","57399-150358","150359-15035495"]
# bins=[0.00, 989, 4723,9729,16753,29419,57398,150358,float('Inf')]

class query_preprocess:
################################################################################

    def upload_query():
        query = pd.read_csv(r"query_users.csv")
        original_shape = query.shape

        query.CustomerDOB = pd.to_datetime(query.CustomerDOB)
        #query.TransactionDate = pd.to_datetime(query.TransactionDate)
        #query.TransactionTime = (query.TransactionTime.apply(lambda x: datetime.strptime(str(x).zfill(6), '%H%M%S'))).dt.time

        #query.CustomerDOB.dt.year.hist(bins=50)
        query.loc[query.CustomerDOB.dt.year > 2000, 'CustomerDOB'] = query.loc[query.CustomerDOB.dt.year > 2000, 'CustomerDOB'] - pd.DateOffset(years = 100)
        query.drop(query[query.CustomerDOB.dt.year == 1800].index, axis=0, inplace=True)
        #query.CustomerDOB.dt.year.hist(bins=50)

        query['Transaction_class'] = pd.cut(query['TransactionAmount (INR)'],
                                    bins=[0, 60, 160,270,458,700,1200,2399,float('Inf')], include_lowest=True,
                                    labels=rank,  right = True)

        query['AccountBalance_size'] = pd.cut(query['CustAccountBalance'],
                            bins=[0.00, 989, 4723,9729,16753,29419,57398,150358,float('Inf')], include_lowest=True,
                            labels=classes, right = True )

        query['CustomerAge'] = (( pd.to_datetime('today') - query.CustomerDOB ) / np.timedelta64(1, 'Y')).round(0)
        query['CustomerAge'] = query['CustomerAge'].astype(int)
        query["n_of_transactions"] = query.groupby(['CustomerDOB', "CustGender"])['TransactionAmount (INR)'].transform('count')
        #print(query.shape)
        qr = query.drop(['CustomerDOB','TransactionTime',"CustAccountBalance","TransactionAmount (INR)"], axis=1)
        qr.reset_index(drop= True, inplace = True)
        print("\n   original_shape : {}  →  query.shape : {}\n".format(original_shape, qr.shape))
        return qr

    def shingling_query(clean_query, vocabulary):
        q = {}
        id_ = 0
        for i in range(clean_query.shape[0]):
            q[id_] = set(clean_query.iloc[i])
            id_ += 1

        shingle_id_dict = {}
        count = len(vocabulary)
        for costumer_id, values in q.items():
            warehouse = set()
            for data in values:
                if data not in vocabulary.keys():
                    vocabulary[data] = count
                    count += 1
                warehouse.add(vocabulary[data])
            shingle_id_dict[costumer_id] = warehouse

        out = list(itertools.islice(q.items(), 3))
        aut = list(itertools.islice(shingle_id_dict.items(), 3))
        for nor,idx in zip(out, aut):
            print("query_user: {} = {}  →{:<2} {}".format(nor[0],nor[1],"", idx[1]))
        print("    ...")

        return q, shingle_id_dict


    def my_f(b,r):
        arr = np.linspace(0.0, 1, 500)
        empty = []
        my_trash = (1/b)**(1/r)
        for x in arr:
            result =  1 - (1 -(x)**r)**b
            empty.append(result)
        plt.plot(arr, empty)
        plt.grid()
        plt.xticks(np.linspace(0.0, 1, 11))
        plt.xlabel("Jac similarity")
        plt.ylabel("Prob to end in same bucket")
        plt.show()
        value = 0.85
        prob_of_values =  1 - ((1 -(value)**r)**b)
        print("\nItems with Jaccard similarity = {} have {} % chance of ending up in the same bucket".format(value, round(prob_of_values,2)))
        my_tresh = (1/b)**(1/r)
        print(" Threshold should be : ", round(my_tresh,2) )


class get_silimilar:
################################################################################

    def J_sim(self, set1,set2):
        result = len(set1.intersection(set2))/len(set1.union(set2))
        return result

    def retrive_similar(self, diz_risultati : dict, q : dict, d : dict, q_index : int, ind_dic):
        try:
            p = {}
            people = diz_risultati[q_index]
            print("Query user : {} → {}\n".format(q_index,q[q_index]))
            if people == None:
                print("  → No similar costumer found")
                return None
            print("Found similarity with :\n")
            for person in list(people):
                p[ind_dic[person]] = d[ind_dic[person]]
                j_sim = get_silimilar.J_sim(self,d[ind_dic[person]], q[q_index])
                print ("  ",ind_dic[person], p[ind_dic[person]], " with Jaccard similarity = {}".format(j_sim))
            return p
        except KeyError:
            print("Non è un utente della query")

##(self, diz_risultati : dict, q : dict, d : dict, q_index : int, ind_dic)
