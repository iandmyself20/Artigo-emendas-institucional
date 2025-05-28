#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import unicodedata 


# # Empenho e pagamento das emendas
# Fonte: InvestSUS 
# https://infoms.saude.gov.br/extensions/CGIN_Painel_Emendas/CGIN_Painel_Emendas.html#GUIA02

# In[10]:


Proposta = pd.read_csv(r'G:\Meu Drive\Doutorado\Disciplinas\Dados\SUS\Consulta portal FNSout2024.csv', delimiter=';', index_col=False)


# In[11]:


Proposta


# In[12]:


Proposta['Data Portaria'] = pd.to_datetime(Proposta['Data Portaria'], errors='coerce')
Proposta['Data Último Pgto'] = pd.to_datetime(Proposta['Data Último Pgto'], errors='coerce')

# Criar a coluna de diferença em dias
# Calcular a diferença e substituir NaN por 0 antes de converter para inteiro
Proposta['DIFERENCA_DIAS'] = (Proposta['Data Último Pgto'] - Proposta['Data Portaria']).dt.days.fillna(0).astype(int)


# In[13]:


Proposta['Pago (R$)'] = Proposta['Pago (R$)'].astype('int64') 


# In[14]:


Proposta


# In[15]:


# Remover linhas onde a coluna 'ANO' é igual a 2024
Proposta = Proposta[Proposta['Ano'] != 2024]


# In[16]:


import pandas as pd
import matplotlib.pyplot as plt

media_diferencas = Proposta.groupby('Ano')['DIFERENCA_DIAS'].mean().reset_index()


# Plotar o gráfico
plt.figure(figsize=(10, 6))
plt.plot( media_diferencas['Ano'],media_diferencas['DIFERENCA_DIAS'], marker='o')

# Adicionar títulos e legendas
plt.xlabel('Ano')
plt.ylabel('Média da diferença em dias entre o pagamento e o empenho')
plt.title('')
plt.legend()
plt.grid(True)
plt.show()


# In[17]:


# Calcular a média de DIFERENCA_DIAS quando ANO é 2016
media_2016 = Proposta[Proposta['Ano'] == 2016]['DIFERENCA_DIAS'].mean()

# Exibir a média
print(f'A média da coluna DIFERENCA_DIAS para o ano de 2016 é: {media_2016}')


# In[18]:


# Calcular a média de DIFERENCA_DIAS quando ANO é 2016
media_2023 = Proposta[Proposta['Ano'] == 2023]['DIFERENCA_DIAS'].mean()

# Exibir a média
print(f'A média da coluna DIFERENCA_DIAS para o ano de 2023 é: {media_2023}')


# In[19]:


condicoes = [
    Proposta['Tipo de Instrumento'].isin([
        'ACADEMIA', 'AMBIENCIA', 'APS', 'CAPS', 'CER', 'COVID-19', 
        'EQUIPAMENTO', 'NEONATAL', 'OFICINA ORTOPEDICA', 
        'PAA - UBS CONSTRUÇÃO', 'UA', 'UBS', 'UBSAMPLIACAO', 
        'UBSFLUVIAL', 'UBSREFORMA', 'UPA'
    ]),
    Proposta['Tipo de Instrumento'].isin([
        'Convênio', 'Convênio Equipamento', 'Convênio Obra', 
        'Convênio Produto', 'PRODUTO', 'TED', 'TED Equipamento', 
        'TED Obra'
    ]),
    Proposta['Tipo de Instrumento'].isin([
        'INCREMENTO MAC', 'INCREMENTO PAP'
    ])
]

# Definindo os valores correspondentes
valores = ['Fundo a fundo investimento', 'Convênio', 'Incremento custeio']

# Criando a nova coluna 'Tipo'
Proposta['Tipo'] = np.select(condicoes, valores, default='Outros')


# In[20]:


total_pago_por_tipo = Proposta.groupby(['Ano', 'Tipo'])['Pago (R$)'].sum().reset_index()
total_pago_por_tipo['Pago (R$)'] = total_pago_por_tipo['Pago (R$)'].astype('int64')  # ou float


# In[21]:


total_pago_por_tipo


# In[22]:


# Verificar os dados
print(total_pago_por_tipo)

# Criar um gráfico de linhas
plt.figure(figsize=(12, 6))

# Criar linhas separadas para cada Tipo
for tipo in total_pago_por_tipo['Tipo'].unique():
    subset = total_pago_por_tipo[total_pago_por_tipo['Tipo'] == tipo]
    plt.plot(subset['Ano'], subset['Pago (R$)'], marker='o', label=tipo)

# Configurar o gráfico
plt.title('')
plt.xlabel('Ano')
plt.ylabel('Total Pago (R$ bilhões)')
plt.xticks(rotation=45)  # Rotacionar os rótulos do eixo x para melhor visualização
plt.legend(title='Tipo')
plt.tight_layout()
plt.grid(True)

# Mostrar o gráfico
plt.show()


# In[23]:


total_pago_por_tipo


# In[90]:


Propostas.to_csv("Propostas.csv",  encoding='utf-8', index=False) 


# In[ ]:




