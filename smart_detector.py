import pandas as pd


def detect_best_columns(df):
    

    numeric = df.select_dtypes(include="number").columns.tolist()

    category = df.select_dtypes(include=["object", "category"]).columns.tolist()

    date = []

    for col in df.columns:
        try:
            pd.to_datetime(df[col])
            date.append(col)
        except:
            pass

    metric_priority = [
        "sales",
        "revenue",
        "profit",
        "amount",
        "income",
        "price",
        "cost",
        "quantity"
    ]

    category_priority = [
        "region",
        "state",
        "city",
        "country",
        "category",
        "product",
        "segment",
        "department"
    ]

    date_priority = [
        "date",
        "order date",
        "invoice date",
        "purchase date"
    ]

    metric = numeric[0] if numeric else None
    cat = category[0] if category else None
    dt = date[0] if date else None

    for c in numeric:
        if any(x in c.lower() for x in metric_priority):
            metric = c
            break

    for c in category:
        if any(x in c.lower() for x in category_priority):
            cat = c
            break

    for c in date:
        if any(x in c.lower() for x in date_priority):
            dt = c
            break

    return metric, cat, dt