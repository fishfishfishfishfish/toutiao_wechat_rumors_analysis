import pandas
import re

# 处理微信数据集
# 提取需要的content字段
raw_data_file = open("files/raw_data/新闻账号原始数据(1083条, 区分健康).csv", encoding="GBK")
raw_data = pandas.read_csv(raw_data_file, dtype=str)
raw_data = raw_data.dropna(subset=["ti", "tx"], how="all")  # 丢弃标题和内容都缺失的
raw_data = raw_data.dropna(subset=["健康"], how="all")  # 丢弃非健康类的
raw_data = raw_data.fillna("")  # 补充缺失值
cleaned_data = raw_data["ti"] + " " + raw_data["tx"]  # 提取字段
for i, c in enumerate(cleaned_data):  # 遍历处理编码问题
    # errors = "ignore" 直接去掉非法字符
    # errors = "replace" 非法字符替换为?
    cleaned_data.iloc[i] = c.encode("GBK", errors="ignore").decode("GBK")  # 按实际位置索引
    cleaned_data.iloc[i] = re.sub(",", "，", cleaned_data.iloc[i])  # 逗号去掉避免影响csv
    cleaned_data.iloc[i] = re.sub("\s+", "", cleaned_data.iloc[i])
cleaned_data = pandas.DataFrame(cleaned_data, columns=["content"])  # 写入新的数据框
cleaned_data.to_csv("files/cleaned_data/weChat_fact_health.csv", encoding="GBK")
