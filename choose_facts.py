import time
import pandas as pd
import numpy as np

# 在liwc基础上，选出与谣言最不相似的新闻
fact = pd.read_csv("liwc_res_data_articles.json['content'].csv")
rumors = pd.read_csv("liwc_res_rumors_positive_content_cleaned.csv")
basket = list(range(fact.iloc[:, 0].size))
picked = list()
print(basket)
start_time = time.time()
for i in range(rumors.iloc[:, 0].size):
    if i % 100 == 0:
        print(i)
    choice = 0
    ri = np.array(rumors.iloc[i].tolist()[1:])
    f0 = np.array(fact.iloc[0].tolist()[1:])
    max_dist = np.sum((ri-f0)**2)
    for j in range(len(basket)-1):
        fi = np.array(fact.iloc[j].tolist()[1:])
        dist = np.sum((ri-fi)**2)
        # print(dist, j)
        if dist > max_dist:
            max_dist = dist
            choice = j
    picked.append(basket.pop(choice))
    # print("choose", choice)
    # time.sleep(30)
end_time = time.time()

print("time cost: ", end_time - start_time)
print(len(basket), basket)
print(len(picked), picked)
print(len(basket)+len(picked))

new_fact = fact.iloc[picked]
new_fact.to_csv("data_articles_as_far_as.csv", index=False)