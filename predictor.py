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

def get_last_draw(df):
    """获取最近一期的红球与篮球号码"""
    latest = df.iloc[0]
    red_last = set(map(int, latest[["红球1", "红球2", "红球3", "红球4", "红球5", "红球6"]]))
    blue_last = int(latest["篮球"])
    return red_last, blue_last

def get_neighbor_candidates(red_last):
    """获取左右相邻红球的备选（左一/右一）"""
    neighbors = set()
    for num in red_last:
        if 1 <= num - 1 <= 33:
            neighbors.add(num - 1)
        if 1 <= num + 1 <= 33:
            neighbors.add(num + 1)
    return neighbors

def get_blue_candidates(blue_last):
    """获取与上期篮球差值为±1~5的候选篮球"""
    candidates = set()
    for d in range(1, 6):
        for b in [blue_last - d, blue_last + d]:
            if 1 <= b <= 16:
                candidates.add(b)
    return candidates

def get_all_historical_combinations(df):
    """提取历史所有红球组合（升序元组）用于去重"""
    history = set()
    for _, row in df.iterrows():
        balls = tuple(sorted(map(int, row[["红球1", "红球2", "红球3", "红球4", "红球5", "红球6"]])))
        history.add(balls)
    return history

def recommend_numbers(df, use_repeat=True, use_neighbor=True, use_blue_delta=True, exclude_history=True):
    """
    综合多种理论依据推荐红球与篮球：
    - 高频热号
    - 上期重复红球（1~2个）
    - 相邻红球
    - 上期篮球 ±1~5
    - 排除历史重复组合（完整6红球）
    """
    red_df, blue_df = get_top_hot_numbers(df)
    red_last, blue_last = get_last_draw(df)
    history_set = get_all_historical_combinations(df) if exclude_history else set()

    red_repeat = list(red_last & set(red_df.index))[:2] if use_repeat else []
    neighbor_reds = get_neighbor_candidates(red_last) if use_neighbor else set()

    top_reds = [r for r in red_df.index if r not in red_repeat][:10]
    candidate_reds = sorted(set(red_repeat + top_reds + list(neighbor_reds)))[:20]

    final_reds = []
    for a in candidate_reds:
        for b in candidate_reds:
            for c in candidate_reds:
                for d in candidate_reds:
                    for e in candidate_reds:
                        for f in candidate_reds:
                            group = tuple(sorted(set([a, b, c, d, e, f])))
                            if len(group) == 6:
                                if exclude_history and group in history_set:
                                    continue
                                final_reds = list(group)
                                break
                        if final_reds: break
                    if final_reds: break
                if final_reds: break
            if final_reds: break
        if final_reds: break

    if not final_reds:
        final_reds = candidate_reds[:6]

    candidate_blues = list(get_blue_candidates(blue_last)) if use_blue_delta else []
    top_blues = [b for b in blue_df.index if not use_blue_delta or b in candidate_blues][:3]
    if not top_blues:
        top_blues = list(blue_df.index[:3])

    return {
        "红球": final_reds,
        "篮球": top_blues
    }
