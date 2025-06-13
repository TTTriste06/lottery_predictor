import pandas as pd
from collections import Counter
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer

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
    latest = df.iloc[0]
    red_last = set(map(int, latest[["红球1", "红球2", "红球3", "红球4", "红球5", "红球6"]]))
    blue_last = int(latest["篮球"])
    return red_last, blue_last

def get_neighbor_candidates(red_last):
    neighbors = set()
    for num in red_last:
        if 1 <= num - 1 <= 33:
            neighbors.add(num - 1)
        if 1 <= num + 1 <= 33:
            neighbors.add(num + 1)
    return neighbors

def get_blue_candidates(blue_last):
    candidates = set()
    for d in range(1, 6):
        for b in [blue_last - d, blue_last + d]:
            if 1 <= b <= 16:
                candidates.add(b)
    return candidates

def get_all_historical_combinations(df):
    history = set()
    for _, row in df.iterrows():
        balls = tuple(sorted(map(int, row[["红球1", "红球2", "红球3", "红球4", "红球5", "红球6"]])))
        history.add(balls)
    return history

def recommend_numbers(df, use_repeat=True, use_neighbor=True, use_blue_delta=True, exclude_history=True):
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

def recommend_by_model(df):
    """输出一组基于随机森林模型的红球和篮球预测（仅做参考）"""
    df_red = df[["红球1", "红球2", "红球3", "红球4", "红球5", "红球6"]].astype(int)
    df_red_set = df_red.apply(lambda x: set(x), axis=1)

    mlb = MultiLabelBinarizer(classes=list(range(1, 34)))
    y = mlb.fit_transform(df_red_set)

    # 简单构造特征（用前一期数据的红球one-hot）预测下一期是否包含该号
    X = y[:-1]
    y_target = y[1:]

    X_train, X_test, y_train, y_test = train_test_split(X, y_target, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=0)
    model.fit(X_train, y_train)

    pred = model.predict([y[-1]])[0]
    pred_nums = [i+1 for i, val in enumerate(pred) if val == 1]
    red_ml = sorted(random.sample(pred_nums, 6)) if len(pred_nums) >= 6 else sorted(pred_nums + random.sample(list(set(range(1, 34)) - set(pred_nums)), 6 - len(pred_nums)))

    blue_mode = df["篮球"].astype(int).mode()[0]
    blue_ml = random.choice([blue_mode] + list(set(range(1, 17)) - {blue_mode}))

    return {
        "红球": red_ml,
        "篮球": [blue_ml]
    }
