import pandas

file = pandas.read_csv("files/rumour_positive_flattened.csv")
selected = file[file["g_category0"] == "news_health "]["content"]
print(selected.head(10))
selected.to_csv("files/rumour_positive_health.csv")
