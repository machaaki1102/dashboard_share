import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import json

#ページ設定を行う
st.set_page_config(
    page_title="Sale Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

#データの読み込みを行う。

#①nitto_sale2.csvを読み込み、期ごとの県ごとに集計する
nitto_sale2 = pd.read_csv('nitto_sale2.csv')

# 「県」ごとに販売量を合計
nitto_sale2 = nitto_sale2[~nitto_sale2['県'].str.contains('原料供給')]

ken_list = list(nitto_sale2['県'].unique())
ki_list = list(nitto_sale2['期'].unique())

#st.write(ken_list)
#nitto_sale2 = nitto_sale2[nitto_sale2['期'] == ki ]
#nitto_sale2= nitto_sale2.groupby('県')['我社販売量'].sum().reset_index()
#nitto_sale2

#②ken_sale.csvを読み込み、県ごと田、畑を合わせて集計する
ken_sale = pd.read_csv('ken_sale.csv')


#他社のメーカー名と銘柄名を取得する
rival_sale = pd.read_csv('rival_sale.csv')
tokuisaki = rival_sale['取扱メーカー'].unique()  #得意先を取得
total = rival_sale['取扱数量'].sum()
tokuisaki_number = len(tokuisaki)


mei = rival_sale['取扱銘柄'].unique()
mei_number = len(mei)

#meigara = list(rival_sale['取扱銘柄'].unique())
#tokuisaki = 'ﾌｧｲﾄｸﾛｰﾑ㈱'

#取扱いメーカーから銘柄選択する
#filtered_data =  rival_sale[rival_sale['取扱メーカー'] == tokuisaki]
# 特定の列（例: '商品名'）から一意の値を取得
#select_meigara = filtered_data['取扱銘柄'].unique()


with st.sidebar:
    st.title('🏂 Sales Dashboard')
    
    #year_list = list(df_reshaped.year.unique())[::-1]
    selected_year = st.selectbox('Select a year', ki_list, index=len(ki_list)-1)
    #df_selected_year = nitto_sale2[nitto_sale2['期'] == selected_year]
    #df_selected_year_sorted = df_selected_year.sort_values(by='我社販売量', ascending=False)
    

    #selected_ken = st.selectbox('Select a prefecture', ken_list, index=len(ken_list)-1)
    selected_ken = st.selectbox('Select a prefecture', ken_list, index=3)
    
    #df_selected_ken = nitto_sale2[nitto_sale2['県'] == selected_ken]
    #df_selected_year_sorted = nitto_sale2.sort_values(by='我社販売量', ascending=False)

    #color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    #selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
    
    #他社のメーカー名と銘柄名を取得する

    selected_tokuisaki = st.selectbox('Select a manufactuer', tokuisaki)
    filtered_data =  rival_sale[rival_sale['取扱メーカー'] == selected_tokuisaki]
    # 特定の列（例: '商品名'）から一意の値を取得
    selected_meigara = filtered_data['取扱銘柄'].unique()
    selected_meigara = st.selectbox('Select a item', selected_meigara)
    #銘柄選定した時のデータフレーム取得
    #rival_sale = pd.read_csv('rival_sale.csv')
    #imput_mei = 'ｷｰｾﾞﾗｲﾄ'
    select_df = rival_sale[rival_sale['取扱銘柄'] == selected_meigara].sort_values('取扱数量', ascending=False)

#数字から文字列に

    mei_number = str(mei_number)
    st.write('他社銘柄確認数:' + mei_number)
    
    total =total.astype(str)
    st.write('他社取扱確認数量:' + total)


#col = st.columns((2, 4, 2), gap='medium')
col = st.columns((1.5, 4, 1.5), gap='medium')


with col[0]:
    st.markdown('県別_我社販売量')
    df_selected = nitto_sale2[nitto_sale2['期'] == selected_year]
    nitto_sale2 = df_selected.groupby('県')['我社販売量'].sum().reset_index()
    nitto_sale2 = nitto_sale2.sort_values(by='我社販売量', ascending=False)
    # インデックスをリセット
    nitto_sale2 = nitto_sale2.reset_index(drop=True)
    nitto_sale2.index = nitto_sale2.index + 1    
    # '販売数量' カラムの数値を小数点以下切り上げて整数に変換
    nitto_sale2['我社販売量'] = nitto_sale2['我社販売量'].astype(int)
    #nitto_sale2

    # 「県名」ごとに販売量を合計
    nen = 2023 #年数の選択
    ken_sale = ken_sale[ken_sale['年数'] == nen ]

    # 数値データが文字列として読み込まれている可能性があるため、カンマを削除し数値型に変換
    ken_sale['想定見込量'] = ken_sale['想定見込量'].str.replace(',', '').astype(int)
    ken_sale= ken_sale.groupby('県')['想定見込量'].sum().reset_index()
    
    # ③データフレームを「県」列で結合する。県、我社販売量、想定見込量がインデックスになっている。
    result_df = pd.merge(nitto_sale2, ken_sale, on='県', how='outer')
    # NaN 値を0で埋める
    result_df['我社販売量'] = result_df['我社販売量'].fillna(0)
    # 「我社販売量」を整数で四捨五入
    result_df['我社販売量'] = result_df['我社販売量'].round().astype(int)

    #シェアー率を計算して、カラムに足す。
    result_df['シェア'] =result_df['我社販売量'] /result_df['想定見込量']
    
    #我社販売量で降順でソートしなおす。
    result_df = result_df.sort_values(by='我社販売量', ascending=False)
    # インデックスをリセット
    result_df = result_df.reset_index(drop=True)
    result_df.index = result_df.index + 1 
    st.dataframe(result_df, height=400)

with col[1]:
    st.markdown('県別販売ヒートマップ')
    #図を表示する。

    # GeoJSON ファイルの読み込み
    with open('japan.geojson', 'r',encoding='utf-8') as file:
        japan_geojson = json.load(file)

    #コロプレス図のパラメーター調整を行う。
    fig = px.choropleth(result_df,
                        geojson=japan_geojson,
                        locations='県',  # DataFrameの都道府県名カラム
                        featureidkey="properties.nam_ja",  # GeoJSONの都道府県名キー
                        color='シェア',  # 色を付けるためのデータカラム
                        color_continuous_scale='Viridis',
                        #center={"lat": 37.5, "lon": 138},
                        center={"lat": 37, "lon": 135},
                        range_color=(0, 0.3),
                        labels={'我社販売量':'販売量','想定見込量':'市場'}
                        )
    fig.update_geos(visible=False, projection_scale=10)  # 地図の範囲をデータに合わせて調整
    #fig.update_geos(fitbounds="locations", visible=False, projection_scale=20)
    fig.update_layout(
        width=800,  # 幅を指定
        height=600  # 高さを指定
    )

# Streamlit でプロットを大きく表示
    #st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(fig)
    #fig.show()

with col[2]:
    st.markdown(selected_ken + 'の販売数量')
    nitto_sale = pd.read_csv('nitto_sale2.csv')
    df_selected2 = nitto_sale[nitto_sale['期'] == selected_year]
    df_selected2 = df_selected2[nitto_sale['県'] == selected_ken]
      # 「我社販売量」を整数で四捨五入
    df_selected2['我社販売量'] = df_selected2['我社販売量'].round().astype(int)
    df_selected2 = df_selected2.sort_values(by='我社販売量', ascending=False)
    df_selected2 = df_selected2[['得意先','我社販売量']] 
    df_selected2 = df_selected2.reset_index(drop=True)
    df_selected2.index = df_selected2.index + 1  
    #nitto_sale2 = df_selected2.groupby('県')['我社販売量'].sum().reset_index()
    #nitto_sale2 = nitto_sale2.sort_values(by='我社販売量', ascending=False)
    # インデックスをリセット
    #nitto_sale2 = nitto_sale2.reset_index(drop=True)
    #nitto_sale2.index = nitto_sale2.index + 1  
    #df_selected2 = df_selected2.set_properties(subset=['得意先'], **{'width': '300px'})

    st.dataframe(df_selected2, height=400)




#col = st.columns((3, 8), gap='medium')
col = st.columns((1.5, 4, 1.5), gap='medium')

with col[0]:
    st.markdown(selected_meigara  + '  ' + '店別販売数量')
    total2 = select_df['取扱数量'].sum().astype(str)
    st.write('確認数量合計:' + total2)
    select_df = select_df[['県','得意先','取扱数量']].reset_index(drop=True)
#   result_df = result_df.reset_index(drop=True)
    select_df.index = select_df.index + 1
    

    st.dataframe(select_df, height=400) 

with col[1]:
    st.markdown(selected_meigara  + '  ' + '県別販売ヒートマップ')

    #銘柄ごとの図を表示
    # GeoJSON ファイルの読み込み
    with open('japan.geojson', 'r',encoding='utf-8') as file:
        japan_geojson = json.load(file)

#コロプレス図のパラメーター調整を行う。
    select_df2 = select_df.groupby('県')['取扱数量'].sum().reset_index().sort_values('取扱数量', ascending=False)
    fig2 = px.choropleth(select_df2,
                        geojson=japan_geojson,
                        locations='県',  # DataFrameの都道府県名カラム
                        featureidkey="properties.nam_ja",  # GeoJSONの都道府県名キー
                        color='取扱数量',  # 色を付けるためのデータカラム
                        color_continuous_scale='Viridis',
                        center={"lat": 37.5, "lon": 138},
                        range_color=(0, 100),
                        #labels={'得意先':'得意先','取扱数量':'取扱数量'}
                        )
    #fig.update_geos(fitbounds="locations", visible=False, zoom=7) 
    #fig.update_geos(fitbounds="locations", visible=False, projection_scale=30) # 地図の範囲をデータに合わせて調整
    fig2.update_geos(visible=False, projection_scale=10)  # 地図の範囲をデータに合わせて調整
    #fig.update_geos(fitbounds="locations", visible=False, projection_scale=20)
    fig2.update_layout(
        width=800,  # 幅を指定
        height=600  # 高さを指定
    )#fig.update_geos(
    #    fitbounds="locations",
    #    visible=False,
    #    projection_scale=7,  # これを設定してもズームしない場合は次の手法を使う
    #    lataxis_range=[30, 55],  # 緯度の範囲を設定
    #    lonaxis_range=[110, 150]  # 経度の範囲を設定
    #    )
    
    #fig.update_layout(
    #    width=1000,  # 幅を指定
    #    height=600  # 高さを指定
    #)
# Streamlit でプロットを大きく表示
    st.plotly_chart(fig2) 
    #st.plotly_chart(fig, use_container_width=True)                    
    #fig.update_geos(fitbounds="locations")  # 地図の範囲をデータに合わせて調整
    #fig.show()
    #select_df = select_df[['県','得意先','取扱数量']].reset_index(drop=True)
#   result_df = result_df.reset_index(drop=True)
    #select_df.index = select_df.index + 1
    #st.dataframe(select_df, height=400) 

with col[2]:
    # データの作成
    data = {
        'カテゴリ': ['A', 'B', 'C', 'D'],
        '値': [40, 30, 20, 10]
    }
    df = pd.DataFrame(data)

# ドーナツチャートの作成
    fig = px.pie(df, values='値', names='カテゴリ', hole=0.8)
    fig.update_layout(width=400, height=400)
# Streamlitで表示
    st.markdown('donuts_chart')
    #st.title("ドーナツチャートの表示")
    st.plotly_chart(fig)