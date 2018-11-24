from bs4 import BeautifulSoup
import pandas as pd
import re

# 去掉谣言数据的html标签
DF = pd.read_csv("files/rumour_positive_health.csv")
res = {"content": list()}
for _, row in DF.iterrows():
    print(row["id"])
    string = row['content']
    try:
        soup = BeautifulSoup(string, 'html.parser')
        single_res = soup.get_text()
        if single_res.find("{!-- PGC_VIDEO:{") == -1 and single_res != "":
            single_res = re.sub("\{[\s\S]*\}", "", single_res)
            res["content"].append(single_res)
    except Exception as e:
        print("----------------------")
res_df = pd.DataFrame(res)
res_df.to_csv("files/rumors_positive_health_cleaned.csv", index=True)
