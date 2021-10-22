import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import os, sys
import logging as log

log.basicConfig(stream=sys.stderr, level=log.DEBUG)
log.warning(os.getcwd())
# change pwd to current project to make relative paths work
os.chdir(os.path.dirname(sys.argv[0]))
log.warning(os.getcwd())

from AIDA.Extract_Sentence_abstract import extract_sentences


# format text links as html links
def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = link
    return f'<a target="_blank" href="{link}">{text}</a>'


#transform conclusions
conclusions_path = './articles/10articels_about_wether_online_vocational_education'
extracted_key_statements = './extracted_conclusions/10_vocational_conclusion.csv'
extract_sentences(conclusions_path, extracted_key_statements)
df = pd.read_csv(extracted_key_statements, sep='|')

df_length = df.shape[0]

# add placeholder columns
df = df.assign(Date_published=['N/A'] * df_length).assign(No_of_citations=['N/A'] * df_length)


# df['Date Published'] = pd.to_datetime(df['Date Published']).dt.date
# df['# Citations'] = pd.to_numeric(df['# Citations'])
# df['URL'] = df['URL'].apply(make_clickable)

# build dashboard
st.title('How many hours should you train an officer for?')

st.sidebar.write('How many articles would you like to see?')
# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    1, df_length, step=1, value=df_length
)

st.sidebar.write('Sorted By')

sort_column = st.sidebar.radio("", ('No_of_citations', 'Date_published'))

st.sidebar.write('Options')

add_checkbox1 = st.sidebar.checkbox('Main Arguments', value=True, key='Sentence')
add_checkbox2 = st.sidebar.checkbox('# Citations', value=True, key='No_of_citations')
add_checkbox3 = st.sidebar.checkbox('Author', value=True, key='Author')
add_checkbox4 = st.sidebar.checkbox('URL', value=True, key='URL')
add_checkbox5 = st.sidebar.checkbox('Keywords', value=True, key='Keywords')
add_checkbox6 = st.sidebar.checkbox('Date Published', value=True, key='Date_published')



# checkbox_list = [True, add_checkbox1, add_checkbox2, add_checkbox3, add_checkbox4, add_checkbox5, add_checkbox6]
checkbox_list = [True, add_checkbox1, add_checkbox2, add_checkbox6]

df = df.iloc[:add_slider]
df = df.loc[:, checkbox_list].copy()
df = df.sort_values(sort_column, axis=0, ascending=False)

# st.dataframe(df)
df = df.to_html(escape=False)
st.write(df, unsafe_allow_html=True)
# st.dataframe(df.loc[:add_slider-1,checkbox_list].copy()             )
