# Pipeline MLOps — Monitoring et Prédiction de la Qualité de l'Air

**Conception et déploiement d’une architecture MLOps complète** pour le monitoring environnemental automatisé : de l’ingestion de données temps réel via API jusqu’au déploiement d’une interface de simulation interactive.

> 🚀 **Impact :** Transformation d’un modèle exploratoire en un **service de prédiction opérationnel**, automatisé et reproductible, exploitant des flux de données environnementales en continu.

<div class="project-hero">
  <img src="/images/marseille.png" alt="Dashboard Qualité de l'Air" style="width: 100%; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.4);">
  <p class="image-caption" style="text-align:center; font-style:italic; color:#888; margin-top:10px;">
    <strong>Interface interactive :</strong> Simulation de l'indice AQI à partir des données environnementales de Marseille.
  </p>
</div>


## 🌍 CONTEXTE & ENJEUX

La pollution atmosphérique constitue un enjeu sanitaire majeur, nécessitant des outils capables de surveiller, anticiper et interpréter les variations des polluants atmosphériques.

Ce projet vise à **industrialiser la prédiction de l’indice de qualité de l’air (AQI)** à partir de données environnementales réelles, en combinant data engineering, machine learning et bonnes pratiques MLOps.

### Objectifs du projet :

- **Automatisation** : Suppression de toute intervention manuelle dans la collecte, le traitement et l’entraînement.
- **Fiabilité** : Garantir des prédictions stables et généralisables malgré la saisonnalité.
- **Vulgarisation** : Rendre la donnée exploitable via un dashboard d’aide à la décision.


## 🛠️ ARCHITECTURE DU PIPELINE (ML LIFE CYCLE)

Le défi principal résidait dans l’automatisation complète du cycle de vie du modèle.

### 1. Ingestion Automatisée (Data Engineering)

- Développement de scripts Python interrogeant l’API publique [aqicn.org](https://aqicn.org).
- Nettoyage, normalisation et historisation des données de pollution et de météo.
- Séparation claire entre données brutes, features transformées et données prêtes à l’entraînement.

### 2. Entraînement & Optimisation (Machine Learning)

- **Modèle** : Utilisation de **XGBoost Regressor**, adapté aux relations non linéaires entre polluants et variables météorologiques.

- **Feature engineering** :

  - Polluants : PM₁₀, PM₂.₅, NO₂, O₃, SO₂, CO

  - Variables météo : température, humidité, pression, vent

- **Évaluation** : Découpage **train / test** afin de contrôler la généralisation et limiter le surapprentissage.

### 3. CI/CD & Déploiement (Approche MLOps)

- **GitLab CI/CD** :

  - Validation du pipeline

  - Entraînement automatisé du modèle

  - Versioning et sauvegarde des artefacts (`.pkl`)

- **Serving** :

  - Application interactive développée avec **Streamlit**

  - Déploiement continu sur **Streamlit Cloud**


## 📊 SIMULATION & LOGIQUE DU MODÈLE

L’utilisateur peut manipuler les concentrations de polluants et les paramètres météorologiques afin d’observer leur impact immédiat sur l’indice de qualité de l’air.

<div class="code-block">
<pre><code>
from sklearn.model_selection import train_test_split
import xgboost as xgb

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = xgb.XGBRegressor(
    n_estimators=200,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror"
)

model.fit(X_train, y_train)
</code></pre>
</div>


## 📊 Fonctionnalités & Simulation

L’interface permet de tester différents scénarios environnementaux et d’en analyser l’impact :

- **Variables polluantes** : Ajustement des taux de $NO_2$, $O_3$, $PM_{10}$ et $PM_{2.5}$.

- **Variables météorologiques** : Température, humidité, vitesse du vent.

- **Interprétation métier** : Mapping automatique vers des catégories de qualité de l’air compréhensibles
  ("Bon", "Modéré", "Dégradé").


## 📉 RÉSULTATS & TAKEAWAYS

- ⚡ Pipeline opérationnel et reproductible : ingestion, entraînement et prédiction automatisés.
- 📊 Évaluation maîtrisée : performances cohérentes entre jeux d’entraînement et de test.
- 🛠️ Architecture scalable : conçue pour être étendue à d’autres villes ou sources de données.


## Stack Technique

<div class="tech-stack">
  <span class="badge">Python</span>
  <span class="badge">Pandas</span>
  <span class="badge">Scikit-learn</span>
  <span class="badge">XGBoost</span>
  <span class="badge">MLOps</span>
  <span class="badge">GitLab CI/CD</span>
  <span class="badge">Streamlit</span>
</div>

<div class="project-links" style="margin-top: 20px;">
  <a href="https://gz9q26ekxwcfae7y7oymfg.streamlit.app/" target="_blank" class="btn-code">
    🌐 Accéder à l'application en direct
  </a>
</div>
