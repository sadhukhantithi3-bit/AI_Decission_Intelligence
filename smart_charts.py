import streamlit as st
import pandas as pd
import plotly.express as px
from modules.smart_detector import detect_best_columns


def smart_charts(df):

    st.markdown("---")
    st.header("📊 Smart Auto Dashboard")

    # -----------------------------
    # Copy Data
    # -----------------------------
    data = df.copy()

    # Detect best columns
    metric, category, date = detect_best_columns(data)

    numeric_cols = data.select_dtypes(include="number").columns.tolist()

    # -----------------------------
    # Sidebar Filters
    # -----------------------------

    st.sidebar.subheader("🎛 Dashboard Filters")

    if category:

        options = sorted(data[category].dropna().unique())

        selected = st.sidebar.multiselect(
            f"Select {category}",
            options
        )

        if selected:
            data = data[data[category].isin(selected)]

    # -----------------------------
    # KPI Cards
    # -----------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", data.shape[0])
    c2.metric("Columns", data.shape[1])
    c3.metric("Numeric", len(numeric_cols))
    c4.metric("Missing", int(data.isnull().sum().sum()))

    # -----------------------------
    # Line Chart
    # -----------------------------

    if date and metric:

        try:

            data[date] = pd.to_datetime(data[date])

            trend = (
                data.groupby(date)[metric]
                .sum()
                .reset_index()
            )

            fig = px.line(
                trend,
                x=date,
                y=metric,
                markers=True,
                title=f"{metric} Trend"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        except Exception:
            pass

    # -----------------------------
    # Bar Chart
    # -----------------------------

    if category and metric:

        bar = (
            data.groupby(category)[metric]
            .sum()
            .reset_index()
            .sort_values(metric, ascending=False)
            .head(10)
        )

        fig = px.bar(
            bar,
            x=category,
            y=metric,
            text_auto=True,
            title=f"{metric} by {category}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -----------------------------
    # Pie Chart
    # -----------------------------

    if category and metric:

        pie = (
            data.groupby(category)[metric]
            .sum()
            .reset_index()
            .head(8)
        )

        fig = px.pie(
            pie,
            names=category,
            values=metric
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
        
    # ==========================

    # -----------------------------
    # Histogram
    # -----------------------------

    if metric:

        fig = px.histogram(
            data,
            x=metric,
            title=f"{metric} Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # -----------------------------
    # Scatter
    # -----------------------------

    if len(numeric_cols) >= 2:

        fig = px.scatter(
            data,
            x=numeric_cols[0],
            y=numeric_cols[1],
            title="Correlation"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
        
         

    # -----------------------------
    # Heatmap
    # -----------------------------

    if len(numeric_cols) >= 2:

        corr = data[numeric_cols].corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale="Blues",
            aspect="auto"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )