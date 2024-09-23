import streamlit as st
import pandas as pd
from collections import Counter
import re
import streamlit_echarts

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

# 生成词云图
def generate_wordcloud(top_keywords, font_path):
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

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
        plot_bar_chart(top_keywords_bar)
        
        # 显示高频词统计表格
        top_keywords_table = pd.DataFrame(top_keywords_bar, columns=['Keyword', 'Frequency'])
        st.subheader('Top Keywords Table')
        st.table(top_keywords_table)
        
        # 指定中文字体路径
        font_path = "simhei.ttf"  # 请根据实际情况修改字体路径
        st.subheader('Word Cloud')
        wordcloud_fig = generate_wordcloud(top_keywords_cloud, font_path)
        st.pyplot(wordcloud_fig)

def plot_bar_chart(top_keywords):
    # 转换数据为 ECharts 格式
    data = [{"name": keyword, "value": count} for keyword, count in top_keywords]
    options = {
        "title": {
            "text": "Top Keywords Bar Chart"
        },
        "tooltip": {},
        "legend": {
            "data": ["Frequency"]
        },
        "xAxis": {
            "data": [item["name"] for item in data],
            "axisLabel": {
                "rotate": 45
            }
        },
        "yAxis": {},
        "series": [{
            "name": "Frequency",
            "type": "bar",
            "data": [item["value"] for item in data]
        }]
    }
    st_echarts(options)

def st_echarts(options):
    # 使用 streamlit-echarts 组件
    streamlit_echarts.st_echarts(options=options, height="600px")

if __name__ == '__main__':
    main()
