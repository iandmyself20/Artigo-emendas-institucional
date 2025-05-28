#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import unicodedata 
import matplotlib.pyplot as plt


# In[2]:


Base = pd.read_csv(r'C:\Users\lunav\Downloads\Base artigo emendas Dados 03112024.csv', engine='python', delimiter=";", index_col=False)


# In[3]:


Base


# In[4]:


Base['Pagototal'] = Base[['pago2015', 'pago2016', 'pago2017', 'pago2018', 'pago2019', 'pago2020', 'pago2021']].sum(axis=1)


# In[5]:


mediana_pagototal = Base['Pagototal'].median()
Base['Acimamediana'] = (Base['Pagototal'] > mediana_pagototal).astype(int)


# In[6]:


media_pagototal = Base['Pagototal'].mean()
Base['Acimamedia'] = (Base['Pagototal'] > media_pagototal).astype(int)


# In[7]:


Base


# In[8]:


Base.to_csv('C:/Users/lunav/Downloads/BaseEmendasDados.csv', index=False)


# In[19]:


# Selecionando as colunas relevantes para o gráfico
columns_to_plot = [
    'pago2015', 'pago2016', 'pago2017', 'pago2018', 'pago2019', 'pago2020', 'pago2021', 'pago2022', 'pago2023',
    'VLcusteio2015', 'VLcusteio2016', 'VLcusteio2017', 'VLcusteio2018', 'VLcusteio2019', 'VLcusteio2020', 
    'VLcusteio2021', 'VLcusteio2022', 'VLcusteio2023',
    'VLincremento2015', 'VLincremento2016', 'VLincremento2017', 'VLincremento2018', 'VLincremento2019', 
    'VLincremento2020', 'VLincremento2021', 'VLincremento2022', 'VLincremento2023',
    'VLtransfespec2015', 'VLtransfespec2016', 'VLtransfespec2017', 'VLtransfespec2018', 'VLtransfespec2019', 
    'VLtransfespec2020', 'VLtransfespec2021', 'VLtransfespec2022', 'VLtransfespec2023'
]

# Filtrar apenas as colunas de interesse
data_filtered = Base[columns_to_plot]

# Agrupar os dados por ano, somando os valores para cada ano
data_filtered_grouped = data_filtered.sum()

# Definir os anos de 2015 a 2023 para as séries que possuem dados consistentes
years = list(range(2015, 2024))

# Preparar os dados para cada linha, considerando a extensão de anos
pago_values = list(data_filtered_grouped.filter(like='pago').values)[:len(years)]
VLcusteio_values = list(data_filtered_grouped.filter(like='VLcusteio').values)[:len(years)]
VLincremento_values = list(data_filtered_grouped.filter(like='VLincremento').values)[:len(years)]
VLtransfespec_values = list(data_filtered_grouped.filter(like='VLtransfespec').values)[:len(years)]

# Converter para milhões
pago_values = [v / 1e9 for v in pago_values]
VLcusteio_values = [v / 1e9 for v in VLcusteio_values]
VLincremento_values = [v / 1e9 for v in VLincremento_values]
VLtransfespec_values = [v / 1e9 for v in VLtransfespec_values]

# Plotar cada série como uma linha no gráfico
plt.figure(figsize=(12, 8))
plt.plot(years, pago_values, marker='o', label='Pago')
plt.plot(years, VLcusteio_values, marker='s', label='VL Custeio')
plt.plot(years, VLincremento_values, marker='^', label='VL Incremento')
plt.plot(years, VLtransfespec_values, marker='x', label='VL Transf. Espec.')

# Adicionar títulos, rótulos e legenda
plt.title('Evolução dos Valores por Ano')
plt.xlabel('Ano')
plt.ylabel('Valor (em bilhões)')
plt.legend()
plt.grid(True)
plt.show()

