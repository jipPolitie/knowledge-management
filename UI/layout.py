import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
from AIDA.Extract_Sentence_abstract import extract_sentences


st.title('How many hours should you train an officer for?')

st.sidebar.write('How many articles would you like to see?')
# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    1, 4,step=1,value = 4
)

st.sidebar.write('Sorted By')


sort_column = st.sidebar.radio(
    "",
    ('# Citations', 'Keywords', 'Date Published'))


st.sidebar.write('Options')

add_checkbox1 = st.sidebar.checkbox('Main Arguments', value=True, key='Argument')
add_checkbox2 = st.sidebar.checkbox('# Citations', value=True, key='Citations')
add_checkbox3 = st.sidebar.checkbox('Author', value=True, key='Author')
add_checkbox4 = st.sidebar.checkbox('URL', value=True, key='URL')
add_checkbox5 = st.sidebar.checkbox('Keywords', value=True, key='Keywords')
add_checkbox6 = st.sidebar.checkbox('Date Published', value=True, key='Date Published')

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = link
    return f'<a target="_blank" href="{link}">{text}</a>'

# link is the column with hyperlinks

# very old:
# df = pd.DataFrame(np.array([['30', 'Main Arguments1', 350, 'Pamela Richards, Debbie Roberts, Mark Britton', 'URL1', 'Enhance Learning, Police training', '06-1-2019'],
#                             ['24', 'Main Arguments2', 600, 'Erik Borglund, Urban Nulden', 'URL2', 'Personas, Scenarios', '28-11-2020'],
#                             ['43', 'Main Arguments3', 50, 'R Yalcinkaya', 'URL3', 'Theory of Planned Behaviour, Technology Acceptance', '15-6-2023'],
#                             ['20', 'Main Arguments4', 200, 'MM Brown, JL Budney', 'URL4', 'Proactive approach,', '26-7-2021']]),
#                   columns=['Answer', 'Main Arguments', '# Citations', 'Author', 'URL', 'Keywords', 'Date Published'])

#build dataframe
# extract_sentences(directory='articles/10articels_about_wether_online_vocational_education', output_path='extracted_conclusions/10_vocational_conclusion.csv')
path='../extracted_conclusions/10_vocational_conclusion.csv'
df=pd.read_csv(path, sep='|')

old_df = pd.DataFrame(np.array([['30', 'Main Arguments1', 350, 'Pamela Richards, Debbie Roberts, Mark Britton', 'https://www.taylorfrancis.com/chapters/edit/10.4324/9780429265365-14/decision-making-pamela-richards-debbie-roberts-mark-britton', 'Enhance Learning, Police training', '06-1-2019'],
                            ['24', 'Main Arguments2', 600, 'Erik Borglund, Urban Nulden', 'https://core.ac.uk/download/pdf/301355808.pdf', 'Personas, Scenarios', '28-11-2020'],
                            ['43', 'Main Arguments3', 50, 'R Yalcinkaya', 'https://search.proquest.com/openview/e8c5731b0b0b1dabc8f1eaaa447ef874/1?pq-origsite=gscholar&cbl=18750', 'Theory of Planned Behaviour, Technology Acceptance', '15-6-2023'],
                            ['20', 'Main Arguments4', 200, 'MM Brown, JL Budney', 'https://onlinelibrary.wiley.com/doi/abs/10.1111/1540-6210.00262', 'Proactive approach,', '26-7-2021']]),
                  columns=['Answer', 'Main Arguments', '# Citations', 'Author', 'URL', 'Keywords', 'Date Published'])

df.assign('Date Published')
df['Date Published'] = pd.to_datetime(df['Date Published']).dt.date

df['# Citations'] = pd.to_numeric(df['# Citations'])

df = df.sort_values(sort_column, axis=0,ascending=False)

df['URL'] = df['URL'].apply(make_clickable)


checkbox_list = [True, add_checkbox1, add_checkbox2, add_checkbox3, add_checkbox4, add_checkbox5, add_checkbox6]

df=df.iloc[:add_slider]
df=df.loc[:,checkbox_list].copy()


#st.dataframe(df)
df = df.to_html(escape=False)
st.write(df, unsafe_allow_html=True)
# st.dataframe(df.loc[:add_slider-1,checkbox_list].copy()             )
