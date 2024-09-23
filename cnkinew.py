import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from wordcloud import WordCloud
from collections import Counter
import re
import pandas as pd

# 设置matplotlib支持中文
def set_chinese_font():
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题

# 读取TXT文件
def read_keywords(file_content):
    keywords = []
    for line in file_content:
        if line.startswith("K1 "):
            keywords.extend(re.split(';', line[3:].strip()))
    return keywords

# 统计高频词
def get_top_keywords(keywords, top_n):
    counter = Counter(keywords)
    return counter.most_common(top_n)

# 生成条形图
def plot_bar_chart(top_keywords):
    set_chinese_font()  # 调用设置中文字体的函数
    words, counts = zip(*top_keywords)
    plt.figure(figsize=(10, 6))
    bars = plt.bar(words, counts)
    plt.xlabel('Keywords')
    plt.ylabel('Frequency')
    plt.title('Top Keywords Bar Chart')
    plt.xticks(rotation=45)
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')
    plt.tight_layout()
    return plt

# 生成词云图
def generate_wordcloud(top_keywords, font_path):
    wordcloud = WordCloud(width=1600, height=1200, background_color='white', font_path=font_path).generate_from_frequencies(dict(top_keywords))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud')
    plt.tight_layout()
    return plt

# Streamlit应用
def main():
    st.title('Keyword Analysis Tool')
    uploaded_file = st.file_uploader("Upload your TXT file", type=['txt'])
    if uploaded_file is not None:
        # 读取文件内容
        file_content = uploaded_file.read().decode('utf-8').splitlines()
        keywords = read_keywords(file_content)
        top_n_bar = st.slider('Number of top keywords for bar chart', 1, 50, 20)
        top_n_cloud = st.slider('Number of top keywords for word cloud', 1, 200, 50)
        
        top_keywords_bar = get_top_keywords(keywords, top_n_bar)
        top_keywords_cloud = get_top_keywords(keywords, top_n_cloud)
        
        st.subheader('Top Keywords Bar Chart')
        chart = plot_bar_chart(top_keywords_bar)
        st.pyplot(chart)
        
        # 显示高频词统计表格
        top_keywords_table = pd.DataFrame(top_keywords_bar, columns=['Keyword', 'Frequency'])
        st.subheader('Top Keywords Table')
        st.table(top_keywords_table)
        
        # 指定中文字体路径
        font_path = "simhei.ttf"  # 请根据实际情况修改字体路径
        st.subheader('Word Cloud')
        wordcloud_fig = generate_wordcloud(top_keywords_cloud, font_path)
        st.pyplot(wordcloud_fig)

if __name__ == '__main__':
    main()
