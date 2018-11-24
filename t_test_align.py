from scipy.stats import ttest_ind
from scipy.stats import levene
import pandas as pd
import random

# 计算新闻和谣言liwc的独立样本t检验
# 随机抽取同样数量的谣言和新闻
fact = pd.read_csv("data_articles_as_far_as.csv")
rumors = pd.read_csv("liwc_res_rumors_positive_content_cleaned.csv")
col_names = ["pronoun", "ppron", "i", "we", "you", "shehe", "they", "ipron",
             "TenseM", "PastM", "PresentM", "FutureM", "ProgM",
             "affect", "posemo", "negemo", "anx", "anger", "sad", "death",
             "preps", "conj", "cogmech", "insight", "cause", "discrep", "tentat", "certain", "inhib", "incl", "excl",
             "bio", "body", "health", "sexual", "ingest",
             "social", "family", "friend", "humans",
             "percept", "see", "hear", "feel"]
fact_index = list(range(0, len(fact)))
rumors_index = list(range(0, len(rumors)))
random.shuffle(fact_index)
random.shuffle(rumors_index)
sample_num = 5955
print(rumors_index[0:sample_num])
ttest_res = {"name": list(), "t_value": list(), "p_value": list()}
for col_name in col_names:
    A = fact.iloc[fact_index[0:sample_num]][col_name]
    B = rumors.iloc[rumors_index[0:sample_num]][col_name]
    ttest_single_res = None
    if levene(A, B).pvalue > 0.05:
        ttest_single_res = ttest_ind(A, B, equal_var=True)
    else:
        ttest_single_res = ttest_ind(A, B, equal_var=False)
    ttest_res["name"].append(col_name)
    ttest_res["t_value"].append(ttest_single_res.statistic)
    ttest_res["p_value"].append(ttest_single_res.pvalue)
    print(col_name)
ttest_df = pd.DataFrame(ttest_res)
ttest_df.to_csv("ttest_res['content']_aligned_with" + str(sample_num) + "samples_chosen_fact.csv", index=False)
