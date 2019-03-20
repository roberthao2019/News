
import json
import jieba
import jieba.analyse
import importlib
import glob
import pymysql

# 載入使用者自建詞庫
jieba.load_userdict("dict.txt")

#SQL連線
db = pymysql.connect(host="localhost", user="root", password="mysql", db="news")
cursor = db.cursor()

try:
    for fn in glob.glob("E:/udn_json-20190301T093011Z-001/udn_json/news/*.json"):
        #print("現在處理檔案:", fn)
        f = open(fn, "r", encoding="utf-8")
        file_content = json.load(f)
        # print(file_content)
        news_temp = file_content["news"]
        # print(news_temp)
        for news in news_temp:
            # print(news)
            # 把這新聞的內文跟關鍵字拉出來
            news_url = news["news_link"]
            print(news_url)
            news_title = news["news_title"]
            news_content = news["news_content"]
            # 進行同義字分析
            news_key_word = jieba.analyse.textrank(news_content, topK=20, withWeight=True)
            keyword_list = []
            for item in news_key_word:
                print(item[0])
                keyword_list.append(item[0])
            # print(keyword_list)

            count = 0
            if len(keyword_list) < 20:
                for keyword in keyword_list:
                    count += 1
                # print(count)
                while count < 20:
                    keyword_list.append(None)
                    count += 1
                    # print(count)
            # print(keyword_list)

            insert_sql = "INSERT INTO news (URL, keyword1, keyword2, keyword3, keyword4, keyword5, keyword6, keyword7, " \
                         "keyword8, keyword9, keyword10, keyword11, keyword12, keyword13, keyword14, keyword15, " \
                         "keyword16, keyword17, keyword18, keyword19, keyword20) " \
                         "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                         "'%s', '%s', '%s', '%s', '%s', '%s', '%s')"\
                         % (news_url, keyword_list[0], keyword_list[1], keyword_list[2], keyword_list[3],
                            keyword_list[4], keyword_list[5], keyword_list[6], keyword_list[7], keyword_list[8],
                            keyword_list[9], keyword_list[10], keyword_list[11], keyword_list[12], keyword_list[13],
                            keyword_list[14], keyword_list[15], keyword_list[16], keyword_list[17], keyword_list[18],
                            keyword_list[19])
            print(insert_sql)
            cursor.execute(insert_sql)
            db.commit()

            # 對 news_title 進行中文分詞
            words = jieba.cut(news_content, cut_all=True)
            # print("  True Mode: " + "/ ".join(words))
            words = jieba.cut(news_content, cut_all=False)
            # print("  Default Mode: " + "/ ".join(words))
            words = jieba.cut_for_search(news_content)
            # print("  Search Engine Mode: " + ", ".join(words))
except:
    print("insert failed")
    db.rollback()
finally:
    cursor.close()
    db.close()
