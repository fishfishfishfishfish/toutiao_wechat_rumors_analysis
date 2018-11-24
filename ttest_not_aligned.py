from scipy.stats import ttest_ind
from scipy.stats import levene
import pandas as pd
import random


NameList = ["data_articles_health", "rumors_positive_health_cleaned",
            "weChat_fact_health", "weChat_rumours_health"]
# 两组数据liwc的独立样本t检验
liwcDir = "files/liwc_res/"
ttestDir = "files/ttest_res/"
liwc1Name = NameList[2]
liwc2Name = NameList[1]
liwc1 = pd.read_csv(liwcDir + "liwc_res_" + liwc1Name + ".csv")  # 第一个liwc结果
liwc2 = pd.read_csv(liwcDir + "liwc_res_" + liwc2Name + ".csv")  # 第二个liwc结果
col_names = ["pronoun", "ppron", "i", "we", "you", "shehe", "they", "ipron",
             "TenseM", "PastM", "PresentM", "FutureM", "ProgM",
             "affect", "posemo", "negemo", "anx", "anger", "sad", "death",
             "preps", "conj", "cogmech", "insight", "cause", "discrep", "tentat", "certain", "inhib", "incl", "excl",
             "bio", "body", "health", "sexual", "ingest",
             "social", "family", "friend", "humans",
             "percept", "see", "hear", "feel",
             "achieve", "adverb", "assent", "auxverb", "filler", "funct", "home", "Interjunction",
             "leisure", "money", "motion", "MultiFun", "negate", "nonfl", "number", "PrepEnd",
             "quant", "QuanUnit", "relativ", "relig", "space", "SpecArt", "swear", "time",
             "verb", "work", "youpl"]
ttest_res = {"name": list(), "t_value": list(), "p_value": list()}
for col_name in col_names:
    A = liwc1[col_name]
    B = liwc2[col_name]
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
ttest_df.to_csv(ttestDir + "ttest_res-" + liwc1Name + "&" + liwc2Name + ".csv", index=False)

