# -*- coding: utf-8 -*-
"""Análise do Airbnb Rio de Janeiro.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Vq26bvju1KslAd1qUsbSUHPCm9BGsZ-O
"""



"""# **Análise de Dados do Airbnb da cidade do Rio de Janeiro**

Airbnb maior empresa hoteleira da atualidade não possui hotel, conectando pessoas que querem viajar, alugando imóveis ou quartos de maneira pratica, o Airbnb oferece uma forma inovadora para uma hospedagem alternativa.

# **Apresentando os Dados**

> Os dados analisados foram obtidos a apartir do site "[insideAirbnb](https://http://insideairbnb.com/)".
Com base nas informações deste Dataset realizei alguns insights para responder algumas perguntas acerca de localização, preço, tipo de imóvel, reviewse etc...

# **Perguntas a serem respondidas**

> Qual o tipo de imóvel?


> Onde o imóvel esta localizado, qual tipo de bairro?


> Qauntas indicações o imóvel recebeu?

# **Data Cleaning e Data Wrangling**

>Limpeza e organização dos Dados
"""

# Commented out IPython magic to ensure Python compatibility.
# Importar pacotesnecessarios
import pandas as pd
! pip install -q matplotlib-venn
import seaborn as sns
sns.set_style()
import matplotlib.pyplot as plt
# %matplotlib inline

# Importar o arquivo listings.csv para um Data frame
# Url = http://data.insideairbnb.com/brazil/rj/rio-de-janeiro/2019-09-23/visualisations/listings.csv
df = pd.read_csv('http://data.insideairbnb.com/brazil/rj/rio-de-janeiro/2019-09-23/visualisations/listings.csv')

"""# **Análise dos Dados**


> Nesta fase identificamos as cinco primeiras linhas do Dadaset, verificar as variaveis no Data frame e criar um dicionário de variaveis.
"""

df.columns

"""## **Dicionário de variáveis.**
*   id - número de id gerado para identificar o imóvel
*   name - nome da propriedade anunciado
*   host_id - número de id do proprietário (anfitrião) da propriedade
*   host_name - Nome do anfitrião
*   neighbourhood_group - esta coluna não contém nenhum valor válido
*   neighbourhood - nome do bairro
*   latitude - coordenada da latitude da propriedade
*   longitude - coordenada da longitude da propriedade
*   room_type - informa o tipo de quarto que é oferecido
*   price - preço para alugar o imóvel
*   minimum_nights - quantidade mínima de noites para reservar
*   number_of_reviews - número de reviews que a propriedade possui
*   last_review - data do último review
*   reviews_per_month - quantidade de reviews por mês
*   calculated_host_listings_count - quantidade de imóveis do mesmo anfitrião
*   availability_365 - número de dias de disponibilidade dentro de 365 dias
"""

#5 Primeiras linhas
print('Este Dataset possui %s linhas e %s colunas' % (df.shape[0], df.shape[1]))
df.head(5)

"""**Identificando os bairros(neighbourhoods), deste Dataframe.**"""

df['neighbourhood'].unique()

"""# Variáveis
Identificando as variáveis e a quantidade de entrada em nosso conjunto.
"""

print('Entradas:\t {}'.format(df.shape [0]))
print('Variáveis:\t {}'.format(df.shape [1]))
display (df.dtypes)

"""**Porcentagem de valores ausentes**
Podemos identificar valores nulos e ausentes, que interfere na qualidadae do Dataset.
*   A coluna neighbourhood_group esta com 100% dos seus valores ausente;
*   A coluna reviews_per_month e last_review esta com aproximadadmente 40% dos seus valores faltando;
*   A coluna name e host_name tem 1% dos seus valores nulos.
"""

# Valores ausentes das variáveis
(df.isnull().sum() / df.shape[0]).sort_values(ascending=False)

"""# **Distribuição das variáveis**

> Histograma para visualizar a distruibuição das variáveis e a presença de outliers nos Dados.
"""

df.hist(bins=15, figsize=(15, 15));

"""# Outliers

> Visualizando a distribuição das variáveis no histograma podemos identificar a presença de outliers nas variáveis calculated_host_listings_counts, minimun_nights, neighbourhood_group e price.

> É possivel confirmar a presença de outliers de naneira bem rapida analisando o resumo estatistico e plotando o boxplot para as variáveis.
"""

df[['calculated_host_listings_count', 'minimum_nights', 'neighbourhood_group', 'price', 'availability_365']].describe()

# boxplot para calculated_host_listings_count
df.calculated_host_listings_count.plot(kind='box', vert=False, figsize=(15, 3))
plt.show()

#Ver quantidade de imóveis por anfitrião acima de 4
print('\ncalculated_host_listings_count: valores acima de 4 imóveis:')
print('{}entradas'. format(len(df[df.calculated_host_listings_count >4])))
print('{:.4f}%'.format((len(df[df.calculated_host_listings_count >4]) / df.shape[0])*100))

# boxplot para minimun_nights
df.minimum_nights.plot(kind='box', vert=False, figsize=(15, 3))
plt.show()

#Ver quantidade acima de 30 dias para minimun_nights
print('\nminimun_nights - valores acima de 30 dias:')
print('{} entradas'.format(len(df[df.minimum_nights >30])))
print('{:.4%}'.format((len(df[df.minimum_nights > 30]) / df.shape[0])*100))

# boxplot para price
df.price.plot(kind='box', vert=False, figsize=(15, 3))
plt.show()

#Ver quantidade acima de 500
print('\nprice: valores acima de 500 reais:')
print('{} entradas'.format(len(df[df.price >500])))
print('{:.4%}'.format((len(df[df.price > 500]) / df.shape[0])*100))

"""# Limpeza de outliers - Histograma

> Outliers identificados, excluiremos as informações de calculated_host_listings_count acima de 4 imóveis por anfitrião, minimun_nights acima de 30 dias e de price acima de R$500,00 e plotaremos outro histograma para verificarmos a distribuição.
"""

#Data frame sem outliers
df_clean = df.copy()
df_clean.drop(df_clean[df_clean.calculated_host_listings_count > 4].index, axis = 0, inplace = True)
df_clean.drop(df_clean[df_clean.minimum_nights > 30].index, axis=0, inplace=True)
df_clean.drop(df_clean[df_clean.price > 500].index, axis = 0, inplace = True)

#Plotagem de histograma para variáveis numéricas
df_clean.hist(bins=15,figsize=(15, 10));

"""# Qual o tipo de imóvel mais alugado no Rio de Janeiro?

> No site Airbnb, pode-se aluguar de casa ou apartamentos, penas um quarto ou quartos compartilhados com outras pessoas. Vamos ver a quantidade de cada tipo de alugel.
"""

#Quantidade de cada tipo de imóvel disponível
df_clean.room_type.value_counts()

#Percentual de cada tipo de disponível
df_clean.room_type.value_counts() / df_clean.shape[0]

"""96 % dos imóveis disponíveis no rio de Janeiro são do tipo casa, apartamento e quarto privado, sendo 60% casa ou apartamento e 36% quarto privativo.

# Quais os bairros mais caros e os mais baratos do Rio de Janeiro?

> Comparação de bairros a partir do preço de locação para sabermos quais os bairros com o valor da hospedagem mais altas e mais baixas, considerando o novo Dataframe após a limpeza dos Dados.
"""

#Comparação de bairros com o preço - Localidade mais cara
print('Bairros mais carosdo RJ:')
df_clean.groupby(['neighbourhood']).price.mean().sort_values(ascending=False)[:20]

#Comparação de bairros com o preço - Localidade mais barata
print('Bairros mais baratos do RJ:')
df_clean.groupby(['neighbourhood']).price.mean().sort_values(ascending=True)[:20]

"""Conseguimos comparar os valores de hospegagem mais caros e mais baratos e também os bairros.

> Com as coordenadas de latitude e longitude fornecidas pelos imóveis é possivel plotar cada ponto. Considerando x=Longitude e y=Latitude.
"""

#Plotar os imóveis pelas suas coordenadas de latutude e longitude
df_clean.plot(kind='scatter', x='longitude', y='latitude', alpha=0.4, c=df_clean['price'], s=8, cmap=plt.get_cmap('jet'), figsize=(12, 8)),

"""Plotando o mapa de coordenadas podemos visualizar que a maior concentração de imíveis para aluguel do site Airbnb na cidade do Rio de Janeiro esta concentrada perto das prias cariocas(pontos amarelos e vermelhos), os pontos azuis indicam presença de outliers e valores discrepantes.

## **Conclusão**

> Este Dataset é uma versão resumida, apenas para uma abordagem incicial de quem como eu esta iniciando seu aprendizado em Data Science, estando aberto a correções, dicas e opiniões de quem já tem experiencia.
Foi realizado uma análise superficial, excluindo -se alguns outliers referentes a algumas variáveis, melhorando o dataFrame possibilitando extrair algumas informações de importancia como, tipo de imóvel por bairro, por preço, maior valor por bairro, menor valor por bairro, imóveis com maior disponibilidade, e localização.
> Com essa análise dos Dados do Airbnb da cidade do Rio de Janeiro é possivel perceber a importancia da limpeza dos Dados, pois a presença de outliers distorcem o resultado final.
"""