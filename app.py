import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Analyse Prix Logements Californie", layout="wide")

# Titre centré
st.markdown(
    """
    <div style="text-align: center">
        <h1 style="color:blue">Statistique des prix des logements en Californie</h1>
        <p> Analyse exploratoire et descriptive du marché immobilier californien </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar navigation
st.sidebar.title("Application d'analyse des données :")
menu = st.sidebar.selectbox('Navigation', [
    'Chargement',
    'Aperçu des données',
    'Statistiques descriptives',
    'Corrélation',
    'Visualisation',
    'Rapport final'
])

# Chargement des données
@st.cache_data

def load_data():
    fichier = 'data/housing.csv'
    try:
        data = pd.read_csv(fichier)
        return data
    except Exception as e:
        st.error(f'Erreur de lecture du fichier : {e}')
        return None

data = load_data()

if menu == 'Chargement':
    st.subheader('Chargement des données')
    if data is not None:
        st.success('Jeu de données chargé avec succès !')
        st.write(f"Nombre de lignes : {data.shape[0]}")
        st.write(f"Nombre de colonnes : {data.shape[1]}")
        st.write('Colonnes :', list(data.columns))
    else:
        st.error('Impossible de charger les données.')

elif menu == 'Aperçu des données':
    st.subheader('Aperçu des données :')
    st.dataframe(data)
    st.subheader('5 premières lignes :')
    st.dataframe(data.head())
    st.subheader('5 dernières lignes :')
    st.dataframe(data.tail())
    st.subheader('Dimensions :')
    st.write(data.shape)
    st.write(f"Nombre de colonnes: {data.shape[1]}")
    st.write(f"Nombre de lignes: {data.shape[0]}")
    st.subheader('Types de données :')
    st.write(data.dtypes)

elif menu == 'Statistiques descriptives':
    st.subheader('Statistiques descriptives des données :')
    st.write(data.describe())
    st.subheader('Distribution du prix médian des logements :')
    fig, ax = plt.subplots()
    ax.hist(data['median_house_value'], bins=30, color='skyblue', edgecolor='black')
    ax.set_xlabel('Prix médian des logements')
    ax.set_ylabel('Fréquence')
    st.pyplot(fig)

elif menu == 'Corrélation':
    st.subheader('Étude de corrélation des données :')
    corr = data.corr(numeric_only=True)
    st.write(corr)
    st.subheader('Heatmap de corrélation :')
    fig_corr, ax_corr = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, ax=ax_corr, fmt='.2f', cmap='coolwarm')
    st.pyplot(fig_corr)

elif menu == 'Rapport final':
    st.markdown("""
    <div style="text-align: center">
        <h2 style="color:darkblue">Rapport Final - Analyse des facteurs influençant le prix des logements en Californie</h2>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    **Résumé du projet :**
    
    Ce projet vise à comprendre les facteurs qui influencent le prix des logements en Californie, à travers une analyse exploratoire et descriptive du jeu de données California Housing. L'objectif est d'aider les agences immobilières à mieux cibler leurs stratégies commerciales et à anticiper les évolutions du marché.
    
    ---
    
    **Principales observations :**
    
    - Les variables les plus corrélées au prix médian des logements sont :
        - Le revenu médian des ménages (`median_income`)
        - L'emplacement géographique (`longitude`, `latitude`)
        - Le nombre moyen de pièces par logement (`total_rooms` et `households`)
    - Les zones côtières et urbaines affichent des prix nettement supérieurs à la moyenne.
    - Les logements situés dans des quartiers à revenu élevé valent significativement plus cher.
    - Les corrélations négatives avec la latitude montrent que le sud de la Californie est plus cher que le nord.
    
    ---
    
    **Recommandations stratégiques pour les agences immobilières :**
    
    1. **Cibler les zones à fort revenu médian** : privilégier les campagnes marketing et les investissements dans les quartiers où le revenu médian est élevé.
    2. **Valoriser la localisation** : mettre en avant la proximité des côtes, des grandes villes et des commodités.
    3. **Optimiser l’offre** : proposer des biens avec un nombre de pièces adapté à la demande locale et à la taille des ménages.
    4. **Suivre l’évolution démographique** : surveiller les tendances de population et d’urbanisation pour anticiper les hausses de prix.
    
    ---
    
    **Conclusion :**
    
    L’analyse met en évidence l’importance du revenu, de la localisation et de la taille des logements dans la formation des prix. Ces résultats permettent d’orienter efficacement les décisions stratégiques et opérationnelles des professionnels de l’immobilier californien.
    
    _Pour plus de détails, consultez les analyses et visualisations dans les autres sections de l’application._
    """)

else:
    st.subheader('Visualisation des données :')
    # Histogramme de la superficie
    fig, ax = plt.subplots()
    ax.hist(data['total_rooms'], bins=30, color='orange', edgecolor='black')
    ax.set_xlabel('Nombre total de pièces')
    ax.set_ylabel('Fréquence')
    ax.set_title('Histogramme du nombre total de pièces')
    st.pyplot(fig)

    # Distribution de la population
    st.subheader('Distribution de la population')
    fig, ax = plt.subplots()
    ax.hist(data['population'], bins=30, color='green', edgecolor='black')
    ax.set_xlabel('Population')
    ax.set_ylabel('Fréquence')
    ax.set_title('Histogramme de la population')
    st.pyplot(fig)

    # Histogramme général
    st.subheader('Histogramme général')
    data.hist(bins=15, figsize=(10, 15), color='blue', edgecolor='black')
    plt.suptitle('Histogramme des données')
    st.pyplot(plt.gcf())

    # Répartition des tranches de valeurs de prix
    st.subheader('Répartition des tranches de prix')
    fig, ax = plt.subplots()
    data['median_house_value'].plot(kind='hist', bins=20, color='purple', ax=ax)
    ax.set_xlabel('Prix médian des logements')
    st.pyplot(fig)

    # Boîtes à moustaches
    st.subheader('Boîtes à moustaches')
    data.plot(kind='box', layout=(3, 3), figsize=(18, 12), sharex=False, sharey=False, subplots=True)
    st.pyplot(plt.gcf())

    # Graphes de densité
    st.subheader('Graphes de densité')
    data.plot(kind='density', subplots=True, layout=(3, 3), figsize=(18, 12), sharex=False, sharey=False)
    st.pyplot(plt.gcf())

    # Pairplot
    st.subheader('Pairplot')
    import seaborn as sns
    sns.pairplot(data.sample(200), diag_kind='kde')
    st.pyplot(plt.gcf())

    # Filtrage interactif
    st.subheader('Filtrage interactif des données')
    min_rooms = int(data['total_rooms'].min())
    max_rooms = int(data['total_rooms'].max())
    rooms_range = st.slider("Sélectionnez une plage de nombre de pièces", min_rooms, max_rooms, (min_rooms, max_rooms))
    data_filtre = data[(data['total_rooms'] >= rooms_range[0]) & (data['total_rooms'] <= rooms_range[1])]
    st.dataframe(data_filtre)

