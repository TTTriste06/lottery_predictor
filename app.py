import streamlit as st
import pandas as pd
from predictor import recommend_numbers, get_top_hot_numbers

st.set_page_config("双色球预测软件", layout="wide")
st.title("🎯 历史规律预测软件")

# ===== 数据加载 =====
st.subheader("📂 历史数据上传")
uploaded_file = st.file_uploader("上传双色球历史数据文件（.xlsx）", type="xlsx")

if uploaded_file:
    df_raw = pd.read_excel(uploaded_file, sheet_name="数据统计", skiprows=6)
    df_raw = df_raw.dropna(how="all").reset_index(drop=True)
    df = df_raw.iloc[2:, :11].copy()
    df.columns = ["期号", "红球1", "红球2", "红球3", "红球4", "红球5", "红球6", "篮球", "奇数个数", "偶数个数", "和值"]
    df.reset_index(drop=True, inplace=True)

    st.success("✅ 数据读取成功！")

    # ===== 数据展示 =====
    st.subheader("📊 最近10期开奖记录")
    st.dataframe(df.head(10))

    # ===== 高频号码统计 =====
    st.subheader("🔥 红球/篮球出现频率")
    hot_reds, hot_blues = get_top_hot_numbers(df)
    col1, col2 = st.columns(2)
    col1.bar_chart(hot_reds)
    col2.bar_chart(hot_blues)

    # ===== 预测推荐 =====
    st.subheader("🎯 历史规律推荐号码")
    recommend = recommend_numbers(df)
    st.markdown(f"**推荐红球（可从中选取2~4个）**：{recommend['红球']}\n\n")
    st.markdown(f"**推荐篮球（热度靠前）**：{recommend['篮球']}")

else:
    st.warning("请先上传历史数据 Excel 文件。")
