import streamlit as st
# -*- coding: utf-8 -*-

"""# 📊 Projeto Final – Análise Contábil com Ajuste Econômico"""


"""Este projeto tem como objetivo integrar análise de dados contábeis de empresas com indicadores econômicos, utilizando Python, Pandas, Ipeadata e Streamlit.
"""

if st.checkbox("Mostrar enunciado 1)"):
    st.write("📝 1) Configure o título na barra do navegador, da página do projeto no Streamlit e descrição inicial do projeto (peso: 1,0)")
    st.write("- Título na barra (`page_title`): Lista de Exercícios 4")
    st.write("- Título da página (`header`): Projeto Final - Análise Contábil com Ajuste Econômico")
    st.write("- Descrição projeto (`write`): Este projeto tem como objetivo integrar análise de dados contábeis de empresas com indicadores econômicos, utilizando Python, Pandas, Ipeadata e Streamlit.")
else:
    st.write("📌 Enunciado ocultado.")

if st.checkbox("Mostrar enunciado 2)"):
    st.write("📝 2) Importe os dados do arquivo empresas_dados.csv utilizando pandas e apresente todas as linhas da df (peso: 1,0)")
    st.write("Dica: Utilize `head(len(df))")
else:
    st.write("📌 Enunciado ocultado.")

st.header("🗃️ Dados das Empresas:")

import pandas as pd
arquivo = "https://raw.githubusercontent.com/kamillapires/Projetofinal/refs/heads/main/empresas_dados.csv"
df = pd.read_csv(arquivo, sep=";")
st.dataframe(df.head(len(df)))

if st.checkbox("Mostrar enunciado 3)"):
    st.write("📝 3) Calcule os indicadores Margem Líquida e ROA e salve como novas coluna da df. Depois apresente os dois indicadores no mesmo gráfico de linhas, agrupado por Ano  (peso: 1,0)")
    st.write("- Margem Líquida = Lucro Líquido / Receita Líquida * 100")
    st.write("- ROA = Lucro Líquido / Ativo Total *  100")
else:
    st.write(" 📌 Enunciado ocultado.")
    
import matplotlib.pyplot as plt
df["Margem Líquida"] = df["Lucro Líquido"] / df["Receita Líquida"] * 100
df["ROA"] = df["Lucro Líquido"] / df["Ativo Total"] * 100


mostrar_df = st.checkbox('Mostrar dados atualizados')

if mostrar_df:
    st.subheader("📂 Dados atualizados com as colunas Margem Líquida e ROA:")
    st.dataframe(df)
else:
    st.write(" 📌 Clique acima para exibir os dados atualizados.")

st.subheader("📈 Gráfico de Indicadores: Margem Líquida e ROA ao Longo do Tempo:")
df_agrupado = df.groupby('Ano')[['Margem Líquida', 'ROA']].mean().reset_index()

anos = df_agrupado['Ano'].unique()  # Garante que todos os anos estejam listados
anos = sorted(anos)

fig, ax = plt.subplots()
plt.figure(figsize=(10, 6))
plt.grid(True)
plt.xticks(df_agrupado['Ano'])

ax.plot(df_agrupado['Ano'], df_agrupado['Margem Líquida'], marker='o', label='Margem Líquida')
ax.plot(df_agrupado['Ano'], df_agrupado['ROA'], marker='o', label='ROA')

ax.set_title("Margem Líquida e ROA ao longo dos anos")
ax.set_xlabel("Anos")
ax.set_ylabel("Valores")
ax.legend(title="Indicadores")
ax.set_xticks(anos)
fig.tight_layout()
st.pyplot(fig)

if st.checkbox("Mostrar enunciado 4)"):
    st.write("📝 4) Utilize o pacote ipeadatapy e faça busca para encontrar o indicador que traga o IPCA, taxa de variação, em % e anual: (peso: 2,0)")
    st.write("- Baixe os dados no período de 2010 a 2024")
    st.write("- Altere o nome da coluna 'YEAR' para 'Ano'")
    st.write("- Altere o nome da coluna 'VALUE ((% a.a.))' para 'IPCA'")
    st.write("- Apresente a df para checar se tudo deu certo")
else:
    st.write(" 📌 Enunciado ocultado.")

st.subheader("🔁 IPCA: taxa de variação anual (em %):")
    
#Procurando todos os conjuntos de dados com o codigo ou nome igual a "IPCA"

import ipeadatapy as ip

ip.list_series('IPCA')

#Apresentando detalhes da série
ip.describe("PRECOS_IPCAG")

#Apresentação dos dados no período de 2010 a 2024

ip.timeseries("PRECOS_IPCAG", yearGreaterThan=2009, yearSmallerThan=2025)

ipca_dados = ip.timeseries("PRECOS_IPCAG", yearGreaterThan=2009, yearSmallerThan=2025)
ipca_dados = ipca_dados.rename(columns={"YEAR": "Ano", "VALUE ((% a.a.))": "IPCA"})
st.dataframe(ipca_dados)

if st.checkbox("Mostrar enunciado 5)"):
    st.write("📝 5) Combine as duas df (Excel e IPEA) em uma nova df e calcule nova coluna chamada Receita Real (peso: 2,0)")
    st.write("- Utilize a função `pd.merge()` para unificar as duas df utiilizando a coluna Ano como conexão (chave primária) entre elas")
    st.write("- Crie nova coluna chamada Receita Real que será o resultado da Receita Líquida de cada ano deduzido o IPCA do ano: `Receita Real = Receitta Líquida - ( Receita Líquida * (IPCA/100) )")
    st.write("- Apresente a nova df combinada")
    
else:
    st.write(" 📌 Enunciado ocultado.")

#Combinado as duas df

df2 = pd.merge(df, ipca_dados, on='Ano')
if st.checkbox('Mostrar dados unificados:'):
    st.subheader("📂 Dados Unificados:")
    st.dataframe(df2)
else:
    st.write(" 📌 Clique acima para exibir os dados unificados.")


#Nova df com a nova coluna de Receita Real 
df2["Receita Real"] = df2["Receita Líquida"] - (df2["Receita Líquida"] * (df2["IPCA"]/100))
st.subheader(" 💾 Atualização dos Dados: Inclusão da Coluna 'Receita Real'")
st.dataframe(df2)

if st.checkbox("Mostrar enunciado 6)"):
    st.write("📝 6) Crie gráfico de linha que apresente as variáveis Receita Líquida e Receita Real ao longo dos anos (no mesmo gráfico) (peso: 1,0)")
else:
    st.write(" 📌 Enunciado ocultado.")

st.subheader("📈 Receita Líquida e Receita Real ao longo dos anos:")

fig, ax = plt.subplots(figsize=(10, 6))
ax.grid(True)
ax.plot(df2["Ano"], df2["Receita Líquida"], marker='o', label='Receita Líquida')
ax.plot(df2["Ano"], df2["Receita Real"], marker='o', label='Receita Real')
ax.set_title("Receita Líquida e Receita Real ao longo dos anos")
ax.set_xlabel("Anos")
ax.set_ylabel("Valores")
ax.legend(title="Indicadores")
ax.set_xticks(anos)
fig.tight_layout()
st.pyplot(fig)

if st.checkbox("Mostrar enunciado 7)"):
    st.write("📝 7) Faça os ajustes necessários e leve este projeto para a web usando GitHub e Streamlit (peso: 2,0)")
    st.write("- Faça os ajustes necessários no projeto para ser publicado no Streamlit")
    st.write("- Crie novo repositório público no GitHub e leve os arquivos .py e .csv pra lá. Aproveite e crie o arquivo requirements.txt com os pacotes utilizados no projeto")
    st.write("- Crie novo projeto no Streamlit e associe ao repositório da lista")
else:
    st.write(" 📌 Enunciado ocultado.")
