import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="StockPlex",
                   page_icon=":bar_chart:",
                   layout="wide")


df = pd.read_excel(
    io='btc.xlsx',
    engine='openpyxl',
    sheet_name='btc',
)

# Main Page
st.markdown("<h1 style='text-align: center; color: white;'> StockPlex: Dynamic Market Insights</h1>", unsafe_allow_html=True)
st.markdown("##")

#KPI
df_2023_onw = df[df['Date'].dt.year >= 2023] # Filter the DataFrame for data starting from 2024 onwards


st.header('Stock Price Movement Over Time', divider='rainbow')
col1,col2,col3,col4=st.columns(4)

with col1:
    open_var = df_2023_onw.groupby(['Date'])['Open'].mean().reset_index()
    #Plotting the line chart
    fig_line = px.line(open_var, x='Date', y='Open', title='Open Price', height=400, width=400)
    st.plotly_chart(fig_line)

with col2:
    open_var = df_2023_onw.groupby(['Date'])['High'].mean().reset_index()
    #Plotting the line chart
    fig_line = px.line(open_var, x='Date', y='High', title='High Price', height=400, width=400)
    st.plotly_chart(fig_line)

with col3:
    open_var = df_2023_onw.groupby(['Date'])['Low'].mean().reset_index()
    #Plotting the line chart
    fig_line = px.line(open_var, x='Date', y='Low', title='Low Price', height=400, width=400)
    st.plotly_chart(fig_line)

with col4:
    open_var = df_2023_onw.groupby(['Date'])['Close'].mean().reset_index()
    #Plotting the line chart
    fig_line = px.line(open_var, x='Date', y='Close', title='Close Price', height=400, width=400)
    st.plotly_chart(fig_line)
    
    open_var = df_2023_onw.groupby(['Date'])['Close'].mean().reset_index()
    #Plotting the line chart
    fig_line = px.line(open_var, x='Date', y='Close', title='Close Price', height=400, width=400)
    st.plotly_chart(fig_line)

st.markdown("---")

# Group by date
vol_month = (
    df_2023_onw.groupby(by=["Date"])["Volume"]
    .mean()
    .reset_index()
    .sort_values(by="Date")
)


fig_amount = px.bar(
    vol_month,
    x="Date",
    y="Volume",
    orientation="v",
    title="Volume of Trades Over Time",
    color_discrete_sequence=["#0083B8"] * len(vol_month),
    template="plotly_white",
    height=400, width=400,
)
fig_amount.update_layout(
    yaxis=(dict(showgrid=False))
)
st.plotly_chart(fig_amount)

hide_st_style = """
            <style>
            #MainMenu {visibility : hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)