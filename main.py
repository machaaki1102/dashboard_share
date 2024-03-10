import pandas
from japanmap import picture
import matplotlib.pyplot as plt
import streamlit as st
 
#st.image(picture())
#st.write("1")

#  CSVをPanasで読み込む
df = pd.read_csv('SSDSE-E-2022v2.csv', encoding='shift_jis', header=2)

# カラーマップでmatplotlibのcmapのjetを設定
cmap = plt.get_cmap('jet')
# カラーマップの最小値と最大値を設定
norm = plt.Normalize(vmin=df['1人当たり県民所得（平成23年基準）'].min(), vmax=df['1人当たり県民所得（平成23年基準）'].max())
# カラーマップの凡例を表示
plt.colorbar(plt.cm.ScalarMappable(norm, cmap))
# データをSeries化する際に可視化対象のデータをカラーマップに従ってカラーコードに変換する関数を作成
fcol = lambda x: '#' + bytes(cmap(norm(x), bytes=True)[:3]).hex()
# japanmapライブラリとmatplotlibを使って可視化
plt.imshow(picture(df['1人当たり県民所得（平成23年基準）'].apply(fcol)))