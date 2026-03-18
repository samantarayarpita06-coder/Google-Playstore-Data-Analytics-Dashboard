
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# custom style
st.markdown("""
<style>
body {background-color:#0e1117;color:white;}
</style>
""", unsafe_allow_html=True)

df = pd.read_csv("googleplaystore.csv")

df['Installs']=df['Installs'].str.replace('[+,]','',regex=True).astype(int)
df['Last Updated']=pd.to_datetime(df['Last Updated'],errors='coerce')

# sidebar
st.sidebar.title("Filters")
cat=st.sidebar.multiselect("Category",df['Category'].unique(),default=df['Category'].unique())
df=df[df['Category'].isin(cat)]

# KPIs
c1,c2,c3,c4=st.columns(4)
c1.metric("⭐ Avg Rating",round(df['Rating'].mean(),2))
c2.metric("📥 Installs",f"{df['Installs'].sum():,}")
c3.metric("💬 Reviews",f"{df['Reviews'].sum():,}")
c4.metric("📦 Apps",len(df))

# charts row1
r1c1,r1c2,r1c3=st.columns(3)

r1c1.plotly_chart(px.pie(df,names="Type",hole=0.5,title="Free vs Paid"),use_container_width=True)

top=df.groupby("Category")["Installs"].sum().sort_values(ascending=False).head(10)
r1c2.plotly_chart(px.bar(top,title="Top Categories"),use_container_width=True)

r1c3.plotly_chart(px.scatter(df,x="Rating",y="Reviews",color="Category",title="Rating vs Reviews"),use_container_width=True)

# row2
r2c1,r2c2=st.columns(2)

trend=df.groupby(df['Last Updated'].dt.month)['Installs'].sum()
r2c1.plotly_chart(px.line(trend,title="Installs Trend"),use_container_width=True)

rev=df.groupby(df['Last Updated'].dt.month)['Reviews'].sum()
r2c2.plotly_chart(px.line(rev,title="Reviews Trend"),use_container_width=True)

st.markdown("### Insights")
st.write("• Top categories dominate installs")
st.write("• Free apps have higher distribution")
