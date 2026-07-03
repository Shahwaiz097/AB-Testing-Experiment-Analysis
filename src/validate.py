import pandas as pd

def check_missing_values(df: pd.DataFrame) -> pd.Series:
    return df.isna().sum()

def check_group_sizes(df: pd.DataFrame, group_col: str = "group") -> pd.Series:
    return df.groupby(group_col).size()

def check_date_range(df: pd.DataFrame, date_col: str = "date"):
    return df[date_col].min(), df[date_col].max()