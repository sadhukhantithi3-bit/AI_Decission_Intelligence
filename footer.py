import streamlit as st


def add_footer():

    st.markdown("""
    <style>

    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color:#161B22;
        color:#94A3B8;
        text-align:center;
        padding:10px;
        font-size:14px;
        border-top:1px solid #334155;
        z-index:999;
    }

    </style>


    <div class="footer">

    🤖 AI Decision Intelligence Platform  
    Developed by <b>Teethi Sadhukhan</b>  
    Python • AI • Machine Learning • Data Analytics

    </div>

    """, unsafe_allow_html=True)