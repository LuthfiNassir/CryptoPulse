import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="StockPulse",
                   page_icon=":bar_chart:",
                   layout="wide")

theme = """
            <style>
                [data-testid="stAppViewBlockContainer"]{
                background-color: #021619;
                } 
                .st-emotion-cache-z5fcl4 {
                    padding: 1rem 3rem 2rem;
                    color: #FFFFFF;
                }  
                .st-cd {
                    background-color: #118d95;
                }
                p {
                    color: #699eb8;
                }
                .st-cu {
                    # background: linear-gradient(to right, #699eb8 100%, #699eb8 100%, #699eb8 100%, #699eb8 100%);
                }
                
            </style>
            """
st.markdown(theme, unsafe_allow_html=True)

df = pd.read_excel(
    io='btc.xlsx',
    engine='openpyxl',
    sheet_name='btc',
)

# Main Page
st.markdown("<h1 style='text-align: center; color:#ffffff;'> StockPlex: Dynamic Market Insights</h1>", unsafe_allow_html=True)
st.markdown("##")


year = st.select_slider(
    "Select a from which year onwards ",
    options=['2024', '2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010'],
    )

#KPI
df_2023_onw = df[df['Date'].dt.year == int(year)] # Filter data starting from 2024 onwards
average_price = round(df_2023_onw['Open'].mean(), 2)
average_high = round(df_2023_onw['High'].mean(), 2)
average_low = round(df_2023_onw['Low'].mean(), 2)
average_volume = int(df_2023_onw['Volume'].mean())




c1,c2,c3,c4=st.columns(4)
with c1:
    st.markdown("<h3 style=' color: #118d95;'>Average Daily price</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style=' color: #699eb8;'>US $ {average_price:,}</h3>", unsafe_allow_html=True)

with c2:
    st.markdown("<h3 style=' color: #118d95;'>Average High price</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style=' color: #699eb8;'>US $ {average_high:,}</h3>", unsafe_allow_html=True)

with c3:
    st.markdown("<h3 style=' color: #118d95;'>Average Low price</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style=' color: #699eb8;'>US $ {average_low:,}</h3>", unsafe_allow_html=True)

with c4:
    st.markdown("<h3 style=' color: #118d95;'>Average Volume</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style=' color: #699eb8;'>US $ {average_volume:,}</h3>", unsafe_allow_html=True)

st.markdown('##')


st.header('Bitcoin Price Movement Over Time', divider='green')

tab1,tab2=st.tabs(["Line Chart","Candlestick Chart"])

with tab1:
    col1,col2,col3,col4=st.columns(4) # to get columns

    with col1:
        open_gr = df_2023_onw.groupby(['Date'])['Open'].mean().reset_index()
        fig_line = px.line(open_gr, x='Date', y='Open', title='Open Price') # Plotting the line chart
        st.plotly_chart(fig_line, use_container_width=True)

    with col2:
        high_gr = df_2023_onw.groupby(['Date'])['High'].mean().reset_index()
        fig_line = px.line(high_gr, x='Date', y='High', title='High Price') # Plotting the line chart
        st.plotly_chart(fig_line, use_container_width=True)

    with col3:
        low_gr = df_2023_onw.groupby(['Date'])['Low'].mean().reset_index()
        fig_line = px.line(low_gr, x='Date', y='Low', title='Low Price') # Plotting the line chart
        st.plotly_chart(fig_line, use_container_width=True)

    with col4:
        close_gr = df_2023_onw.groupby(['Date'])['Close'].mean().reset_index()
        fig_line = px.line(close_gr, x='Date', y='Close', title='Close Price') # Plotting the line chart
        st.plotly_chart(fig_line, use_container_width=True)
        

with tab2:
    candle = go.Figure(data=[go.Candlestick(x=df_2023_onw['Date'],
                                            open=df_2023_onw['Open'],
                                            high=df_2023_onw['High'],
                                            low=df_2023_onw['Low'],
                                            close=df_2023_onw['Close'])])
    candle.update_layout(title="Candlestick Chart for Daily Stock Prices")
    st.plotly_chart(candle, use_container_width=True)  


st.markdown("---")


# Group by date
vol_month = (
    df_2023_onw.groupby(by=["Date"])["Volume"]
    .mean()
    .reset_index()
    .sort_values(by="Date")
)
 
# Volume trade bar chart
vol_bar = px.bar(
    vol_month,
    x="Date",
    y="Volume",
    orientation="v",
    title="Volume of Trades Over Time",
    color_discrete_sequence=["#0083B8"] * len(vol_month),
    template="plotly_white",
    height=400, width=400,
)
vol_bar.update_layout(
    yaxis=(dict(showgrid=False))
)
st.plotly_chart(vol_bar, use_container_width=True)


hide_st_style = """
            <style>
            #MainMenu {visibility : hidden;}
            footer {visibility: hidden;}
            body {background-color: #31EC56;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)