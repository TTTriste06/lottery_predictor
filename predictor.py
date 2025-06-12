import pandas as pd
from collections import Counter

def get_top_hot_numbers(df):
    """统计红球和篮球出现频率"""
    reds = df[["红球1", "红球2", "红球3", "红球4", "红球5", "红球6"]].values.flatten()
    blues = df["篮球"].values
    
    red_counts = Counter(reds)
    blue_counts = Counter(blues)
    
    red_df = pd.Series(red_counts).sort_values(ascending=False).head(20)
    blue_df = pd.Series(blue_counts).sort_values(ascending=False).head(10)
    return red_df, blue_df

def recommend_numbers(df):
    """基于历史推荐红球与篮球"""
    red_df, blue_df = get_top_hot_numbers(df)
    recommend_reds = list(red_df.index[:8])
    recommend_blues = list(blue_df.index[:3])

    return {
        "红球": recommend_reds,
        "篮球": recommend_blues
    }
