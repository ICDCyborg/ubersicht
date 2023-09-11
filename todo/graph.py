import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import base64
from io import BytesIO

def Output_Graph():
    '''プロットしたグラフを画像データとして出力するための関数'''
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def Plot_Graph(x, y, threshold=None):
    '''グラフをプロットするための関数'''
    # 日本語フォントを適用することで文字化けを回避
    plt.rcParams['font.family'] = 'MS Gothic'
    plt.switch_backend('AGG')
    # グラフのサイズ調整
    plt.figure(figsize=(5, 3))
    # plt.title('グラフ')
    fig, ax = plt.subplots()
    bar_width = 0.4
    bars = ax.bar(x, y, bar_width)
    for bar in bars:
        cx = bar.get_x() + bar.get_width() / 2
        cy = bar.get_height()
        radius = bar_width / 2
        circle = Circle((cx, cy), radius, color='blue', fill=True)
        ax.add_patch(circle)
    if threshold is not None:
        plt.axhline(y=threshold, color='r')
    plt.xlabel('日付')
    plt.ylabel('値')
    plt.xticks(rotation=45)
    plt.tight_layout()
    graph = Output_Graph()
    return graph