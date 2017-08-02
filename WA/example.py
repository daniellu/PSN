
import jieba.analyse
from os import path
import matplotlib as mpl
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np

if __name__ == "__main__":
    content = open("data.txt", "rb").read()

    # tags extraction based on TF-IDF algorithm
    # extract the top 10 most frequent words
    tagsWeights = jieba.analyse.extract_tags(content, topK=50, withWeight=True)

    frequency_array = {}
    for tag in tagsWeights:
        print(tag[0])
        frequency_array[tag[0]] = (tag[1])

    #we need specify the font here as word cloud does not have chinese character by default
    wc = WordCloud(font_path='simsun.ttc',
                   background_color="white", max_words=300,
                   max_font_size=40, random_state=42)

    # generate word cloud with frenquecies
    wc.generate_from_frequencies(frequency_array)

    plt.imshow(wc)
    plt.axis("off")
    plt.show()

