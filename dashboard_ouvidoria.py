from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

ouvidoria_2023 =pd.read_excel('base da dados/2023.xlsx')
ouvidoria_2023.rename(columns={'Unidade Gestora': 'Unidade'}, inplace=True)
ouvidoria_2022 =pd.read_excel('base da dados/2022.xlsx')
ouvidoria_2021 =pd.read_excel('base da dados/2021.xlsx')
ouvidoria_2020 =pd.read_excel('base da dados/2020.xlsx')

#df_eouve = pd.read_json("eouve.json")

df_eouve = pd.concat([ouvidoria_2023, ouvidoria_2022, ouvidoria_2021, ouvidoria_2020 ])
df_eouve['Recebido em'] = pd.to_datetime(df_eouve['Recebido em'],format="%d/%m/%Y %H:%M:%S")
df_eouve['Ano'] = df_eouve['Recebido em'].dt.strftime('%Y')
df_eouve['Mes'] = df_eouve['Recebido em'].dt.strftime('%m')


st.set_page_config(page_title="Dashboard",layout="wide")
st.subheader("Analise Eouve")

with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


st.sidebar.image("data/logo1.png",caption="SEGD")

st.sidebar.header("Filtros")

ug = st.sidebar.checkbox("Filtrar por Unidade Gestora")
gestora = st.sidebar.selectbox(label='Unidade Gestora', options = list(df_eouve['Unidade'].unique()), index=0, help = 'Escolha uma Unidade Gestora para filtrar o dashboard', disabled = not ug)
ano_check = st.sidebar.checkbox("Filtrar por Ano")
ano = st.sidebar.selectbox(label='Ano', options = list(df_eouve['Ano'].unique()), index=0, help = 'Escolha uma Ano para filtrar o dashboard', disabled = not ano_check)

def filtra_dados(df_eouve):
    if ug:
        df_eouve = df_eouve[df_eouve['Unidade'] == gestora]
    if ano_check:
        df_eouve = df_eouve[df_eouve['Ano'] == ano]
    return(df_eouve)

df_eouve = filtra_dados(df_eouve)

col1, col2, col3 = st.columns(3, gap="small")

with col1:
    qtd_manifestacoes = df_eouve["Unidade"].count()
    st.metric(label="Manifestações", value=qtd_manifestacoes)

with col2:
    qtd_assuntos = df_eouve['Assunto'].nunique()
    st.metric(label="Assuntos", value=qtd_assuntos)

with col3:
    valor_mais_frequente = df_eouve['Origem de cadastro'].value_counts().idxmax()
    valor_mais_frequente2 = df_eouve['Origem de cadastro'].value_counts().max()
    st.metric(label="Maior origem de cadastro", value=valor_mais_frequente)

assuntos_com_muitos_pontos = df_eouve["Assunto"].value_counts()
unidades_com_muitos_pontos = df_eouve["Unidade"].value_counts()
   
col4, col5 = st.columns(2, gap="small")

with col4:
    graf_barra = px.bar(df_eouve, x=assuntos_com_muitos_pontos.head(8).index, y=assuntos_com_muitos_pontos.head(8).values, color_discrete_sequence=px.colors.sequential.Blues_r)
    graf_barra.update_layout(title='Ranking de Assuntos')
    st.plotly_chart(graf_barra, theme="streamlit", use_container_width=True)

with col5:
    
    graf_pizza = px.pie(df_eouve, values=unidades_com_muitos_pontos.head(8).values, names=unidades_com_muitos_pontos.head(8).index, color_discrete_sequence=px.colors.sequential.Blues_r, title='Manifestações por Secretaria')
    st.plotly_chart(graf_pizza, theme="streamlit", use_container_width=True)

df_count = df_eouve.groupby(['Ano', 'Mes']).size().reset_index(name='Contagem')
graf_linha = px.line(df_count, x='Mes', y='Contagem', color='Ano', markers=False, labels={'Mes': 'Mês'}, color_discrete_sequence=px.colors.sequential.Blues_r   )
graf_linha.update_traces(textposition="top center")
graf_linha.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), title='Manifestações por Mes em cada Ano')
st.plotly_chart(graf_linha, use_container_width=True, theme="streamlit")

    


# importa o texto
texto = df_eouve['Manifestação']

# concatenar as palavras
all_texto = " ".join(w for w in texto)

# importa as stopwords em português
stopwords = open('stopwords.txt').read()

# transforma as stopwords em um lista
lista_stopwords = stopwords.split(' \n')

# inicializa uma word cloud
wordcloud = WordCloud(stopwords = lista_stopwords,
                        background_color = 'white', # cor de fundo
                        width = 3000, # largura
                        height = 1500, # altura
                        colormap = 'winter') # cores das palavras

# gera uma wordcloud através do texto
wordcloud.generate(all_texto)

fig_3, cx = plt.subplots()
cx.imshow(wordcloud, interpolation = 'bilinear') # plotagem da nuvem de palavras
plt.axis('off') # remove as bordas
st.pyplot(fig_3, use_container_width=True)
    
# df_selection=df_eouve[['Manifestação', 'Assunto', 'Categoria', 'Origem de cadastro']]

#st.dataframe(df_eouve, use_container_width=True)