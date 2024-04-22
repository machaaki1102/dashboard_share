import pandas as pd
from japanmap import picture
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np 
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

#df
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
#st.image(picture(dic))

#=====kepler.gl

from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon


st.write("This is a kepler.gl map in streamlit")

#初期地を設置する。
config = {
  "version": "v1",
  "config": {
    "mapState": {
      "bearing": 0,
      "latitude": 37.68944,
      "longitude": 137.99167,
      "pitch": 0,
      "zoom": 4,
    },
    "visState": {
      "layers": [
        {
          "type": "geojson",
          "config": {
            "dataId": "japan",
            "label": "Share Layer",
            "color": [221, 178, 124],
            "columns": {
              "geojson": "_geometry"
            },
            "isVisible": True,
            "visConfig": {
              "opacity": 0.8,
              "strokeOpacity": 0.8,
              "thickness": 0.5,
              "strokeColor": [221, 178, 124],
              "colorRange": {
                "name": "Global Warming",
                "type": "sequential",
                "category": "Uber",
                "colors": ["#5A1846", "#900C3F", "#C70039", "#E3611C", "#F1920E", "#FFC300"]
              },
              "colorField": {
                 "name": "sale_r5",
                 "type": "real"
              },
              "sizeRange": [0, 10],
              "radiusRange": [0, 50],
              "heightRange": [0, 500],
              "elevationScale": 5,
              "stroked": True,
              "filled": True,
              "enable3d": False,
              "wireframe": False
            },
            "hidden": False,
            "textLabel": [{"field": None, "color": [255, 255, 255], "size": 18, "offset": [0, 0], "anchor": "start", "alignment": "center"}]
          },
        }
      ],
      "interactionConfig": {
        "tooltip": {
        "enabled": True,
        "fieldsToShow": {
          "japan": ["nam_ja", "share", "sale_r5"]
          }
        }
       }
      }
    }
}

config4 = {
  "version": "v1",
  "config": {
    "mapState": {
      "bearing": 0,
      "latitude": 37.68944,
      "longitude": 137.99167,
      "pitch": 0,
      "zoom": 4
    },
    "visState": {
      "layers": [
        {
          "type": "geojson",
          "config": {
            "dataId": "japan",
            "label": "Japan",  
            "isVisible": True,  # True を大文字で始める
            "visConfig": {
              "fillColor": {
                #"name": "Global Warming",
                #"type": "sequential",
                #"category": "Uber",
                #"colors": [
                #  "#0198BD",
                #  "#49E3CE",
                #  "#E8FEB5",
                #  "#FEEDB1",
                #  "#FEAD54",
                #  "#D50255"
                #]
                "name": "Your Custom Palette",
                "type": "ordinal",
                "category": "Custom",
                "colors": ["#0198BD", "#FEAD54", "#D50255"]
              },
            },
          },
          "colorField": {
  
            "name": "sale_r5",
            "type": "real"
          },
          "colorScale": "quantile",
        }
      ],
      "interactionConfig": {  # layers 配列の外、visState オブジェクトの直下に移動
        "tooltip": {
          "enabled": True,  # True を大文字で始める
          "fieldsToShow": {
            "japan": ["nam_ja", "share", "sale_r5"]
          },
        },
      },
    },  
  },
}

# KeplerGlの設定を定義
config5 = {
  "version": "v1",
  "config": {
    "visState": {
      "layers": [
        {
          "type": "geojson",
          "config": {
            "dataId": "japan",  # ここでのデータIDは、後でデータを追加する際に使用するIDと一致させる
            "label": "japan",
            "isVisible": True,
            "visConfig": {
              "fillColor": {
                "name": "Your Custom Palette",
                "type": "ordinal",  # "ordinal"はカテゴリカルデータ、"sequential"は連続データに適している
                "category": "Custom",
                "colors": ["#0198BD", "#FEAD54", "#D50255"]  # この色の配列を変更して、異なる色を設定
              },
            },
            "colorField": {
              "name": "share",  # 色を変更するために使用するフィールド
              "type": "real"
            },
            "colorScale": "quantile"  # 色のスケール（"quantize", "quantile", "ordinal", "linear"など）
          }
        }
      ]
    }
  }
}


# GeoJSONデータをGeoDataFrameに変換
japan_geojson = gpd.read_file('japan.geojson')

# CSV ファイルを読み込む
ken_share_df = pd.read_csv('ken_share.csv',encoding='utf-8-sig')
# シェアのパーセンテージを数値に変換
ken_share_df['share'] = ken_share_df['share'].str.rstrip('%').astype('float') / 100
# GeoDataFrameとDataFrameを結合（ここでは'nam_ja'と'Prefecture'を結合キーとして使用）
japan_geojson = japan_geojson.merge(ken_share_df, left_on='nam_ja', right_on='Prefecture')

#桁数の調整、shareは小数点3桁、sale_r5は整数
japan_geojson['share'] =japan_geojson['share'].round(3)
japan_geojson['sale_r5'] =japan_geojson['sale_r5'].round(0)

#map1にconfigのデータで初期設定を行う。
map_1 = KeplerGl(height=600, config = config)
map_1.add_data(data=japan_geojson, name="japan")
keplergl_static(map_1)

#japan_geojson.to_file('japan_updated.geojson', driver='GeoJSON')


