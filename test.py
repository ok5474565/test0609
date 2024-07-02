import streamlit as st
import jieba
import requests
from collections import Counter
from bs4 import BeautifulSoup
import re  # 导入正则表达式库
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud

# 设置中文字体
font_path = 'simhei.ttf'

# 定义数据清洗函数
def clean_text(text):
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text()
    text = re.sub(r'\s+', '', text)  # 合并多个空格
    return text

# 定义去除标点符号和数字的函数
def remove_punctuation_and_numbers(text):
    text = re.sub(r'[^\w\s]', '', text)  # 去除标点符号
    text = re.sub(r'\d+', '', text)  # 去除数字
    return text

# 定义分词函数
def segment(text):
    stopwords = ['的', '了', '在', '是', '我', '你', '他', '她', '它', '们', '这', '那', '之', '与', '和', '或']
    text = remove_punctuation_and_numbers(text)
    words = jieba.lcut(text)
    words = [word for word in words if word and word not in stopwords]
    return words

def main():
    st.title("文本分析与词云可视化")

    url = st.text_input("请输入网页 URL:")

    if url:
        response = requests.get(url)
        response.encoding = 'utf-8'
        text = response.text

        text = clean_text(text)
        words = segment(text)
        word_counts = Counter(words)
        top_words = dict(word_counts.most_common(20))  # 只取词频最高的20个词

        # 生成词云
        wordcloud = WordCloud(font_path=font_path, max_words=20).generate_from_frequencies(top_words)

        # 绘制词云图
        plt.figure(figsize=(10, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)

        # 创建DataFrame来展示前20个词频统计
        top_words_df = pd.DataFrame(list(top_words.items()), columns=['词语', '词频'])
        top_words_df['序号'] = range(1, 21)  # 添加序号

        # 绘制横向柱状图
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.barh(top_words_df['序号'], top_words_df['词频'], color='skyblue')  # 使用barh绘制横向柱状图
        ax.set_yticks(top_words_df['序号'])  # 设置y轴刻度
        ax.set_yticklabels(top_words_df['词语'])  # 设置y轴标签
        ax.set_xlabel('词频')  # x轴标签
        ax.set_ylabel('词语')  # y轴标签
        ax.set_title('前20个词频统计条形图')  # 图表标题

        # 显示图表
        st.pyplot(fig)

        # 显示词频统计表格
        st.write("以下是前20个词频统计表格：")
        st.table(top_words_df)

if __name__ == "__main__":
    main()
