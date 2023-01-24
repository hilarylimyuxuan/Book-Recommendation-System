# -*- coding: utf-8 -*-
import streamlit as st

#header
st.title('Book Recommendation System')
st.subheader("Weekly Top Selling Books")
st.image('book_image.png',use_column_width=True)
#table of content
st.subheader('Table of Content')
st.write('1. Project background - Description of the Data Science Project')
st.write('2. Project Objectives')
st.write('3. Data Modelling')
st.write('4. Data Interpretation')
st.write('5. Deployment of Data Product')
st.write('6. Insights and Conclusion')
st.write('7. References')
#project background
st.subheader('Project Background')
st.write('Write intro here!')

st.subheader('Project Objectives')
st.write('Write objectives here!')

#import library
import pandas as pd
import numpy as np
import ast
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
#load data
book_df = pd.read_csv('books.csv')
cleaned_df = pd.read_csv("./books_clean.csv")

#build dashboard
add_sidebar=st.sidebar.selectbox('Navigation', ('Project Infomation','Book Data Facts','Search Engine'))

#condition
if add_sidebar == 'Project Infomation':
     st.write('Write project info here')

if add_sidebar == 'Book Data Facts':
     st.write('Write book data facts here')

if add_sidebar == 'Search Engine':
     st.write('Write search engine here')
#Genre Selection
select_content = st.selectbox ('Choose a Genre!',('A','B', 'C','D','E'))
#Author Selection
select_content = st.selectbox ('Choose an Author!',('A','B', 'C','D','E'))
#Recommendation Books



# chart_data = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=["a", "b", "c"])

# st.bar_chart(chart_data)