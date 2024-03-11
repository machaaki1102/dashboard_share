import pandas as pd
from japanmap import picture
import matplotlib.pyplot as plt
import streamlit as st
 
#st.image(picture())
#st.write("1")

# =====
#  CSVをPanasで読み込む
#df = pd.read_csv('SSDSE-E-2022v2.csv', encoding='shift_jis', header=2)

# カラーマップでmatplotlibのcmapのjetを設定
#cmap = plt.get_cmap('jet')
# カラーマップの最小値と最大値を設定
#norm = plt.Normalize(vmin=df['1人当たり県民所得（平成23年基準）'].min(), vmax=df['1人当たり県民所得（平成23年基準）'].max())
# カラーマップの凡例を表示
#plt.colorbar(plt.cm.ScalarMappable(norm, cmap))
# データをSeries化する際に可視化対象のデータをカラーマップに従ってカラーコードに変換する関数を作成
#fcol = lambda x: '#' + bytes(cmap(norm(x), bytes=True)[:3]).hex()
# japanmapライブラリとmatplotlibを使って可視化
#plt.imshow(picture(df['1人当たり県民所得（平成23年基準）'].apply(fcol)))

#====

df = pd.read_csv("SSDSE-C-2023.csv",encoding='shift-jis',header=1)
df = df[["都道府県","牛肉"]]

# 最小値を0 、最大値を 1にする
data = df["牛肉"]
df["牛肉"] = np.interp(data, (data.min(), data.max()), (0, 1)) 

# 辞書作成
dic = {}
cmap = plt.get_cmap('Reds') # 赤のカラーマップ
for ken, val in df.values:
    dic[ken] = cmap(val, bytes=True)
#これを地図に表示します。


# 地図表示
st.image(picture(dic))