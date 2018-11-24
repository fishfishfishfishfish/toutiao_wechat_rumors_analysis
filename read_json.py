import json
import pandas as pd
import re


def get_json_stream(file: str, targets: list):
    """
    :param file: json文件名
    :param targets: 需要提取的内容的路径的列表
    :return: 提取为数据框的格式
    """
    raw_data = dict()  # 使用字典临时保存需要提取的数据
    for target in targets:
        raw_data[target] = list()  # 初始化字典为空列表组成的字典

    with open(file, 'r') as f:
        # print("文件共有", len(f.readlines()), "行")
        for line in f.readlines():  # 读取json文件的每一行，每一行才是一个json格式文本
            # print(line)  # debug
            data_line = json.loads(line)  # 载入json数据
            for target in targets:
                data_unit = data_line
                target_path = target.split('/')  # 根据给定的路径去提取
                for path in target_path:
                    try:
                        data_unit = data_unit[path]
                    except Exception as e:
                        data_unit = " "
                        break
                if isinstance(data_unit, dict):
                    tmp = ""
                    for k, v in data_unit.items():
                        tmp += str(k) + " "
                    data_unit = tmp
                if isinstance(data_unit, list) and len(data_unit) != 0 and not isinstance(data_unit[0], str):
                    if target in raw_data.keys():
                        del raw_data[target]
                    for item in data_unit:
                        k = target + "/" + item["name"]
                        if k not in raw_data.keys():
                            raw_data[k] = list()
                        raw_data[k].append(item["count"])
                    continue
                if isinstance(data_unit, list) and (len(data_unit) == 0 or isinstance(data_unit[0], str)):
                    tmp = ""
                    for item in data_unit:
                        tmp += item
                    data_unit = tmp
                if isinstance(data_unit, str):
                    data_unit = data_unit.replace(",", "，")  # 逗号作为分隔符, 内容里的逗号去掉
                    data_unit = data_unit.replace(".", "。")  # 英文句号作为分隔符, 在R里面处理, 分词时gsub函数会出问题, 去掉
                    data_unit = re.sub("\s", " ", data_unit)  # 把空白字符去掉
                raw_data[target].append(data_unit)
            # 保证每一列一样长
            raw_data_len = [len(v) for _, v in raw_data.items()]
            max_len = max(raw_data_len)
            for _, v in raw_data.items():
                if len(v) < max_len:
                    v.append("")
    df = pd.DataFrame(raw_data)  # 把数据存储为数据框
    return df


def get_json_listed_data(file: str, target: str):
    with open(file, 'r') as f:
        line = f.readlines()[1]
        data_line = json.loads(line)
        data_line = data_line[target]
        for item in data_line:
            print(item["name"])


"""
data_articles.json
rumour_positive.json
article_group_stats
channel_group_stats
media_id
title
video_group_stats
g_category4
feed_group_stats
g_category1
g_category0
g_category3
g_category2
content
source
related_group_stats
gid
comments
keywords
"""
if __name__ == '__main__':
    Count = 1
    Targets = list()
    File = input('请输入文件名：')
    name = input('路径名1：')
    while name != '':
        Count += 1
        Targets.append(name)
        name = input('路径名' + str(Count) + ':')
    DF = get_json_stream(File, Targets)
    DF.to_csv(File + str(Targets[1:6]) + '.csv')
    # -----------------------输出一行json--------------------
    # f = open("files/data_articles.json")
    # lines = f.readlines()
    # line = lines[1000]
    # print(line)
    # --------------------list形式的数据------------------
    # File = input('请输入文件名：')
    # Name = input('路径名：')
    # get_json_listed_data(File, Name)
