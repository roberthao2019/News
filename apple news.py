
import json
import jieba
import jieba.analyse
import importlib
import glob

for fn in glob.glob("E:/apple_json-20190227T122726Z-001/apple_json/apple_news/*.json"):
    print("現在處理檔案:", fn)
    f = open(fn, "r", encoding="utf-8")
    file_content = json.load(f)

# 因為裡面有日期跟新聞資訊 把新聞資訊拉出來
    news_temp = file_content["news"]
    print(news_temp)
# 裡面可能有多則新聞 先把第一則拉出來
    for news_temp2 in news_temp:
# 把這新聞的內文跟關鍵字拉出來
        news_content = news_temp2["news_content"]
        news_key_word = jieba.analyse.extract_tags(news_content, topK=20, withWeight=True)
        for item in news_key_word:
            print(item[0], item[1])
        news_title = news_temp2["news_title"]
        print(news_content)
        print(news_key_word)

# 對 news_title 進行中文分詞

        words = jieba.cut(news_content, cut_all=True)
        print("  True Mode: " + "/ ".join(words))
        words = jieba.cut(news_content, cut_all=False)
        print("  Default Mode: " + "/ ".join(words))
        words = jieba.cut_for_search(news_content)
        print("  Search Engine Mode: " + ", ".join(words))

