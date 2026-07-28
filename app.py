import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.ensemble import IsolationForest
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
LOGIN_USERNAME = "admin"
LOGIN_PASSWORD = "1234"
st.set_page_config(
    page_title="AI Decision Intelligence Platform",
    page_icon="🤖",
    layout="wide"
)
st.markdown("""
<style>

.stApp{
    background-color:#0E1117;
    color:white;
}

section[data-testid="stSidebar"]{
    background-color:#161B22;
}

h1,h2,h3,h4,h5,h6{
    color:#00E5FF;
}

.stButton>button{
    background:#00BFFF;
    color:white;
    border-radius:10px;
    height:45px;
    width:100%;
    border:none;
}

.stDownloadButton>button{
    background:#00C853;
    color:white;
    border-radius:10px;
}

div[data-testid="metric-container"]{
    background:#1E293B;
    padding:15px;
    border-radius:12px;
    border:1px solid #334155;
}

</style>
""", unsafe_allow_html=True)
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-3.5-flash")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.markdown("""
<div style="
background: linear-gradient(135deg,#0F172A,#1E3A8A);
padding:35px;
border-radius:20px;
color:white;
text-align:center;
margin-bottom:25px;">

<h1 style="color:white;">🤖 AI Decision Intelligence Platform</h1>

<p style="font-size:18px;">
Welcome back! Login to access your AI-powered data analytics workspace.
</p>

<hr>

<h3 style="color:#38BDF8;">🚀 Analyze • Visualize • Predict</h3>



</div>
""", unsafe_allow_html=True)

    st.subheader("🔐 User Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username == LOGIN_USERNAME and password == LOGIN_PASSWORD:

            st.session_state.logged_in = True
            st.rerun()

        else:
            st.error("Invalid Username or Password")

    st.stop()
st.markdown("""
<div style="
background: linear-gradient(135deg,#0F172A,#1E3A8A);
padding:35px;
border-radius:20px;
color:white;
margin-bottom:25px;
box-shadow:0px 8px 20px rgba(0,0,0,0.3);">

<h1 style="text-align:center;color:white;">
🤖 AI Decision Intelligence Platform
</h1>

<p style="text-align:center;font-size:18px;">
Transform your CSV & Excel data into powerful business insights with AI, Machine Learning and Interactive Analytics.
</p>

<hr>

<h2 style="text-align:center;color:#38BDF8;">
🚀 Everything You Need In One Platform
</h2>

<div style="display:grid;
grid-template-columns:repeat(2,1fr);
gap:12px;
margin-top:20px;">

<div style="background:#1E293B;padding:15px;border-radius:12px;">
📂 CSV & Excel Upload
</div>

<div style="background:#1E293B;padding:15px;border-radius:12px;">
🧹 Automatic Data Cleaning
</div>

<div style="background:#1E293B;padding:15px;border-radius:12px;">
📊 KPI Dashboard
</div>

<div style="background:#1E293B;padding:15px;border-radius:12px;">
📈 Interactive Charts
</div>

<div style="background:#1E293B;padding:15px;border-radius:12px;">
📉 Advanced Visualizations
</div>

<div style="background:#1E293B;padding:15px;border-radius:12px;">
💡 AI Business Insights
</div>

<div style="background:#1E293B;padding:15px;border-radius:12px;">
🤖 Gemini AI Assistant
</div>

<div style="background:#1E293B;padding:15px;border-radius:12px;">
🔮 Sales Forecasting
</div>

<div style="background:#1E293B;padding:15px;border-radius:12px;">
🚨 AI Anomaly Detection
</div>

<div style="background:#1E293B;padding:15px;border-radius:12px;">
📥 Download Cleaned Dataset
</div>

<div style="background:#1E293B;padding:15px;border-radius:12px;">
📄 AI PDF Report
</div>

<div style="background:#1E293B;padding:15px;border-radius:12px;">
⚡ Fast & Interactive Dashboard
</div>

</div>

<hr>

<h3 style="color:#22C55E;text-align:center;">
👇 Upload your CSV or Excel dataset below to get started
</h3>

</div>
""", unsafe_allow_html=True)

st.success("📂 Supported Formats: CSV (.csv) | Excel (.xlsx) | Excel (.xls)")
st.sidebar.title("Navigation")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file, encoding="latin1")
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ File Uploaded Successfully!")

    st.subheader("📊 Dataset Preview")
    st.dataframe(df)

    st.subheader("📋 Dataset Information")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    st.subheader("Missing Values")
    st.write(df.isnull().sum())

    st.subheader("🧹 Auto Data Cleaning")

    duplicate_rows = df.duplicated().sum()
    missing_values = df.isnull().sum().sum()

    st.write(f"Duplicate Rows: {duplicate_rows}")
    st.write(f"Missing Values: {missing_values}")

    df = df.drop_duplicates()

    numeric_columns = df.select_dtypes(include="number").columns
    df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())

    categorical_columns = df.select_dtypes(include="object").columns
    df[categorical_columns] = df[categorical_columns].fillna("Unknown")

    st.success("✅ Data Cleaned Successfully!")

    st.subheader("📋 Cleaned Dataset")
    st.subheader("⬇️ Download Cleaned Dataset")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
    label="📥 Download Cleaned CSV",
    data=csv,
    file_name="cleaned_dataset.csv",
    mime="text/csv"
)
    st.dataframe(df)
    st.subheader("📊 KPI Dashboard")

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:
        selected_col = st.selectbox(
        "Select Numeric Column",
        numeric_cols
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total", round(df[selected_col].sum(), 2))
    col2.metric("Average", round(df[selected_col].mean(), 2))
    col3.metric("Maximum", round(df[selected_col].max(), 2))
    col4.metric("Minimum", round(df[selected_col].min(), 2))
    st.subheader("📊 Interactive Charts")

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:
        selected_col = st.selectbox(
        "Select Numeric Column for Chart",
        numeric_cols
    )

    chart_type = st.selectbox(
        "Select Chart Type",
        ["Bar Chart", "Histogram", "Box Plot"]
    )

    if chart_type == "Bar Chart":
        fig = px.bar(df, y=selected_col)
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Histogram":
        fig = px.histogram(df, x=selected_col)
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Box Plot":
        fig = px.box(df, y=selected_col)
        st.plotly_chart(fig, use_container_width=True)
        st.subheader("📈 Advanced Visualizations")

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:
        x_axis = st.selectbox("Select X-Axis", df.columns)
        y_axis = st.selectbox("Select Y-Axis", numeric_cols)

    chart = st.selectbox(
        "Choose Chart",
        ["Line Chart", "Scatter Plot", "Pie Chart"]
    )

    if chart == "Line Chart":
        fig = px.line(df, x=x_axis, y=y_axis, title="Line Chart")
        st.plotly_chart(fig, use_container_width=True)

    elif chart == "Scatter Plot":
        fig = px.scatter(df, x=x_axis, y=y_axis, title="Scatter Plot")
        st.plotly_chart(fig, use_container_width=True)

    elif chart == "Pie Chart":
        category_cols = df.select_dtypes(include="object").columns

        if len(category_cols) > 0:
            category = st.selectbox("Category", category_cols)
            pie = df.groupby(category)[y_axis].sum().reset_index()

            fig = px.pie(
                pie,
                names=category,
                values=y_axis,
                title="Pie Chart"
            )
            st.plotly_chart(fig, use_container_width=True)


        st.subheader("🤖 AI Insights")

    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:
     st.write(f"### 📌 {col}")

    st.write(f"Highest Value : {df[col].max()}")

    st.write(f"Lowest Value : {df[col].min()}")

    st.write(f"Average : {round(df[col].mean(),2)}")

    if df[col].mean() > df[col].median():
        st.success(f"{col} is positively skewed.")

    else:
        st.warning(f"{col} is negatively skewed.")

    st.subheader("🤖 AI Business Assistant")

    question = st.text_input("Ask about your dataset")

    if st.button("Ask AI"):
        if question.strip() == "":
         st.warning("Please enter a question.")
        else:
         prompt = f"""
   Dataset Columns:
   {list(df.columns)}

   Dataset Sample:
   {df.head().to_string()}

   Question:
   {question}
   """

        try:
            response = model.generate_content(prompt)
            st.success(response.text)

        except Exception:
            st.error("AI Service is temporarily unavailable. please try again later.")
    st.subheader("📈 Sales Forecasting")

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:
     forecast_col = st.selectbox(
        "Select Column for Forecasting",
        numeric_cols,
        key="forecast"
    )

    values = df[forecast_col].dropna().values

    if len(values) > 5:
        X = np.arange(len(values)).reshape(-1, 1)
        y = values

        model = LinearRegression()
        model.fit(X, y)

        future_days = st.slider(
            "Forecast Next Values",
            1,
            20,
            5
        )

        future_X = np.arange(
            len(values),
            len(values) + future_days
        ).reshape(-1, 1)

        predictions = model.predict(future_X)

        forecast_df = pd.DataFrame({
            "Future Index": future_X.flatten(),
            "Predicted Value": predictions
        })

        st.write("### Forecast Results")
        st.dataframe(forecast_df)

        fig = px.line(
            forecast_df,
            x="Future Index",
            y="Predicted Value",
            title="Forecast"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("🚨 AI Anomaly Detection")

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:

     anomaly_col = st.selectbox(
        "Select Column",
        numeric_cols,
        key="anomaly"
    )

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    temp = df[[anomaly_col]].dropna().copy()

    temp["Anomaly"] = model.fit_predict(temp[[anomaly_col]])

    st.write("Detected Anomalies")

    st.dataframe(temp[temp["Anomaly"] == -1])

    fig = px.scatter(
        temp,
        y=anomaly_col,
        color=temp["Anomaly"].astype(str),
        title="Anomaly Detection"
    )

    st.subheader("📄 Download AI Report")

    numeric_cols = df.select_dtypes(include="number").columns

    pdf_col = st.selectbox(
    "Select Column for PDF Report",
    numeric_cols,
    key="pdf_col"
)

    if st.button("Generate PDF Report"):

       styles = getSampleStyleSheet()
       pdf = SimpleDocTemplate("AI_Report.pdf")

       story = []

       story.append(Paragraph("<b>AI Decision Intelligence Report</b>", styles["Heading1"]))
       story.append(Paragraph(f"Rows: {df.shape[0]}", styles["BodyText"]))
       story.append(Paragraph(f"Columns: {df.shape[1]}", styles["BodyText"]))
       story.append(Paragraph(f"Missing Values: {df.isnull().sum().sum()}", styles["BodyText"]))
       story.append(Paragraph(f"Average {pdf_col}: {round(df[pdf_col].mean(), 2)}", styles["BodyText"]))
       story.append(Paragraph("Dataset cleaned successfully.", styles["BodyText"]))

       pdf.build(story)

       with open("AI_Report.pdf", "rb") as file:
          st.download_button(
            label="📥 Download PDF",
            data=file,
            file_name="AI_Report.pdf",
            mime="application/pdf",
            key="pdf_download"
        )
