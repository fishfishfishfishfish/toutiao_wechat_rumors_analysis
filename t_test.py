from scipy.stats import ttest_ind
from scipy.stats import levene
import pandas as pd
import random

fact_and_rumours = pd.read_csv("liwc_res_fact_and_rumor.csv")
ttest_res = {"name": list(), "t_value": list(), "p_value": list()}
col_names = fact_and_rumours.columns.values.tolist()
col_names.pop(len(col_names)-1)
print(col_names)
for col_name in col_names:
    A = fact_and_rumours[fact_and_rumours['label'] == 0][col_name]
    B = fact_and_rumours[fact_and_rumours['label'] == 1][col_name]
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
ttest_df.to_csv("ttest_res['content'].csv", index=False)

