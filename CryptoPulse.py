import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import datetime

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
                .st-d3 {
                    background-color: #118d95;
                }
                p {
                    color: #699eb8;
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
st.markdown("<h1 style='text-align: center; color:#ffffff;'> CryptoPulse: Bitcoin Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("##")



#setting the date
startDate = datetime.date(2010, 7, 18)
endDate = datetime.date(2024, 3, 19)
d = st.date_input(
    "Select Date Range",
    (datetime.date(2024, 1, 1), endDate),
    startDate,
    endDate,
    format="MM.DD.YYYY",
)

start_date = datetime.datetime(d[0].year, d[0].month, d[0].day)  # Convert to datetime
end_date = datetime.datetime(d[1].year, d[1].month, d[1].day)  # Convert to datetime
df_filtered = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

# KPI
average_price = round(df_filtered['Open'].mean(), 2)
average_high = round(df_filtered['High'].mean(), 2)
average_low = round(df_filtered['Low'].mean(), 2)
average_volume = int(df_filtered['Volume'].mean())

vwSeries=(df_filtered['Close'] * df_filtered['Volume']).cumsum() / df_filtered['Volume'].cumsum()
vwDf=pd.DataFrame({'Date':df_filtered['Date'],'VWAP':vwSeries})


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
        open_gr = df_filtered.groupby(['Date'])['Open'].mean().reset_index()
        fig_line = px.line(open_gr, x='Date', y='Open', title='Open Price') # Plotting the line chart
        st.plotly_chart(fig_line, use_container_width=True)

    with col2:
        high_gr = df_filtered.groupby(['Date'])['High'].mean().reset_index()
        fig_line = px.line(high_gr, x='Date', y='High', title='High Price') # Plotting the line chart
        st.plotly_chart(fig_line, use_container_width=True)

    with col3:
        low_gr = df_filtered.groupby(['Date'])['Low'].mean().reset_index()
        fig_line = px.line(low_gr, x='Date', y='Low', title='Low Price') # Plotting the line chart
        st.plotly_chart(fig_line, use_container_width=True)

    with col4:
        close_gr = df_filtered.groupby(['Date'])['Close'].mean().reset_index()
        fig_line = px.line(close_gr, x='Date', y='Close', title='Close Price') # Plotting the line chart
        st.plotly_chart(fig_line, use_container_width=True)
        

with tab2:
    candle = go.Figure(data=[go.Candlestick(x=df_filtered['Date'],
                                            open=df_filtered['Open'],
                                            high=df_filtered['High'],
                                            low=df_filtered['Low'],
                                            close=df_filtered['Close'])])
    candle.update_layout(title="Candlestick Chart for Daily Stock Prices")
    st.plotly_chart(candle, use_container_width=True)  


st.markdown("---")


# Group by date
vol_month = (
    df_filtered.groupby(by=["Date"])["Volume"]
    .mean()
    .reset_index()
    .sort_values(by="Date")
)
 
coll1,coll2=st.columns(2)
with coll1:
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
    vol_bar.update_xaxes(title=' ')
    vol_bar.update_yaxes(title=' ')
    st.plotly_chart(vol_bar, use_container_width=True)

with coll2:
    Vwap=px.line(vwDf,x='Date',y='VWAP',title="Volume-Weighted Average Price (VWAP)")
    st.plotly_chart(Vwap)
st.markdown('---')

df_mov=df[df['Date'].dt.year>=2020]
df_mov['50-day'] = df_mov['Close'].rolling(window=50).mean()
df_mov['200-day'] = df_mov['Close'].rolling(window=200).mean()

# Create the line chart
fig = px.line(df_mov, x='Date', y=['50-day', '200-day'], title='Moving Averages')
fig.update_xaxes(title='Date')
fig.update_yaxes(title='Price')
# Display the line chart using Streamlit
st.plotly_chart(fig, use_container_width=True)


hide_st_style = """
            <style>
            #MainMenu {visibility : hidden;}
            footer {visibility: hidden;}
            body {background-color: #31EC56;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)