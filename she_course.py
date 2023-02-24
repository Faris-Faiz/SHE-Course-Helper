import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import plotly.graph_objects as go
from datetime import datetime

excel_file = ('mayascrapingproject/shecourselist.xlsx')

st.set_page_config(page_title="SHE Helper!",
                   page_icon=":book:",
                   layout="wide")

she_courses_cluster1 = pd.read_excel(excel_file)
df = she_courses_cluster1

# SIDEBAR
link = '[Source Code](https://github.com/Faris-Faiz/SHE-Course-Helper)'
st.sidebar.markdown("##### " + link, unsafe_allow_html=True)
st.sidebar.header("Filtering the SHE course:")
agree = st.sidebar.checkbox('No negatives (DANGEROUS!)', value=True)

learning_mode = st.sidebar.multiselect(
    "Select the Learing Mode:",
    options=she_courses_cluster1["MEDIUM"].unique(),
    default=["ONLINE", "LECTURE"]
)

cluster = st.sidebar.selectbox(
    "Select the Cluster:",
    [1, 2, 3, 4]
)

faculty = st.sidebar.multiselect(
    "Select the Faculty:",
    options=she_courses_cluster1["FACULTY"].unique(),
    default=she_courses_cluster1["FACULTY"].unique()
)

full = "F"

if agree:
    df_selection = she_courses_cluster1.query(
    "FACULTY == @faculty & MEDIUM == @learning_mode & FULL == @full & CLUSTER == @cluster & REGISTERED != -1"
)

else:
    df_selection = she_courses_cluster1.query(
        "FACULTY == @faculty & MEDIUM == @learning_mode & FULL == @full & CLUSTER == @cluster"
    )

## Doughnut Graph stuff
df = she_courses_cluster1.groupby('CLUSTER')['FULL'].apply(lambda x: (x == 'F').sum()).reset_index(name='count')

fig = go.Figure(data=[go.Pie(values=df['count'], hole=.6, labels=['Cluster 1', 'Cluster 2', 'Cluster 3', 'Cluster 4'])])
fig.update_traces(textinfo='percent+label')

fig.update_layout(
    title={
        'text': "Percentage of vacant classes based on the cluster they're in",
        'y': 0.88,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    })


# Retrieving last updated data
# Open the file in read mode
with open('mayascrapingproject/lastran.txt', 'r') as file:
    # Read the contents of the file
    content = file.read()

date_format = "%Y-%m-%d %H:%M:%S.%f"
datetime_object = datetime.strptime(content, date_format)
formatted_dt = datetime_object.strftime('%I:%M%p on %d of %B %Y')

## MAINPAGE

st.markdown("## :book: SHE Course Helper!     _by Faris Faiz_")
st.markdown("##### Last Data Updated at " + formatted_dt)

vacant_courses = she_courses_cluster1['FULL'].value_counts()['F']

left_column, middle_column, right_column = st.columns(3)

total_courses = len(she_courses_cluster1)

percent_available = (vacant_courses / total_courses) * 100

# Chart section

chart_left, chart_middle, chart_right = st.columns(3)

with chart_left:
    st.plotly_chart(fig)

with chart_right:
    df_courses_available = she_courses_cluster1.groupby('CLUSTER')['FULL'].apply(lambda x: (x == 'F').sum()).reset_index(name='AVAILABLE COURSES')
    st.dataframe(df_courses_available)

with left_column:
    st.metric("Available Courses:", total_courses)

with middle_column:
    st.metric("Vacant Courses:", vacant_courses)

she_courses_cluster1.groupby(by=["FULL"]).sum()

st.title("List of Available Courses:")
st.markdown("**-1 Values :arrow_right: it's unknown**, **Registered** :arrow_right: **registered for the subject**, **Capacity** :arrow_right: **capacity of the subject.** \nIt's better to focus on the subjects that don't have any negative numbers!")
df_selection.drop(columns=['FULL', 'CLUSTER'], axis=1, inplace=True)
st.write("Showing courses from cluster " + str(cluster))
st.dataframe(df_selection.style.hide_index())