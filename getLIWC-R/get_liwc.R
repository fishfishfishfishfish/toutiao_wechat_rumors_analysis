library(RJSONIO)
library(stringr)
library(plyr)
library(jiebaR)
library(quanteda)

workspace <- getwd()
fileName <- "weChat_fact_health.csv"
dictPath <- paste(workspace, "LIWC_dict_index.txt", sep="/")
filePath <- paste(workspace, "../files/cleaned_data" ,fileName, sep="/")
resPath <- paste(workspace, "../files/liwc_res", paste0("liwc_res_", fileName), sep="/")
bigdict <- dictionary(file = dictPath, format = "LIWC", encoding = "GBK") #  这里注意词典文件的编码
mixseg <- worker()
# 读取文本数据
data <- read.csv(filePath, fileEncoding = "GBK", quote = "", stringsAsFactors = FALSE)
word_count <- 0
# 对文本数据进行分词
for(i in 1:nrow(data)){
  if(i %% 1 == 0){print(i)}
  after_segment <- segment(as.character(data[i, 'content']), jieba=mixseg)
  if(length(after_segment) > 0){
    word_count <- word_count + length(after_segment)
    after_segment <- str_c(after_segment, collapse = " ")
    data[i, 'content'] <- after_segment
  }
  else{
    data[i, 'content'] <- NA
  }
}
data <- data[complete.cases(data),]
word_count <- word_count / nrow(data)

# 计算liwc
w_corpus <- corpus(data[, 'content'])
liwc_res <- data.frame(dfm(w_corpus, dictionary=bigdict)) 
liwc_res <- cbind("id" = data$id, liwc_res)
write.csv(liwc_res, file = resPath, quote = F, row.names = F, fileEncoding = "GBK")
