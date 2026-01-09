## Prédiction de l’Évolution de Fluides Turbulents par Deep Learning (ConvLSTM2D)

Accélération **data-driven** de simulations physiques haute fidélité grâce à des modèles
**spatio-temporels profonds**, avec déploiement sur infrastructures **HPC**.

> 🎯 Objectif : réduire drastiquement le coût de calcul tout en conservant
> la cohérence physique et statistique des écoulements turbulents.


<div class="project-hero" style="text-align: center; margin-bottom: 30px;">
  <img src="/images/simulation_vortex.gif"
       alt="Simulation de vorticité" 
       style="width: 100%; max-width: 900px; height: auto; display: block; margin: 0 auto; border-radius: 8px;">
  <p class="image-caption" style="font-style: italic; color: #888; margin-top: 10px;">
    <strong>Animation :</strong> Évolution temporelle d’un champ de vorticité prédite par un modèle ConvLSTM2D,
    entraîné sur données DNS haute résolution.
  </p>
</div>

## Contexte Scientifique & Industriel

La **simulation numérique directe (DNS)** de la turbulence est un pilier de nombreux secteurs :

- mécanique des fluides
- aéronautique & spatial
- énergie & combustion
- météorologie & climat

Cependant, ces simulations sont **extrêmement coûteuses** :

- temps de calcul élevé
- dépendance à des supercalculateurs
- faible itérabilité pour l’ingénierie

> 👉 Une seule simulation DNS peut nécessiter **plusieurs jours de calcul** sur cluster HPC.


## Problématique de Recherche

**Comment prédire l’évolution temporelle d’un écoulement turbulent sans résoudre explicitement
les équations physiques à chaque pas de temps ?**

### Approche adoptée

- Hypothèse clé :  
  Les champs de vorticité contiennent des **structures spatio-temporelles apprenables**

- Stratégie :

  - apprendre sur données DNS

  - préserver les statistiques globales

  - accélérer l’inférence de plusieurs ordres de grandeur


## Environnement de Calcul Haute Performance (HPC)

Le projet a été mené dans un cadre **recherche appliquée**, sur les infrastructures du
**Mésocentre d’Aix-Marseille** :

- **Plateforme** : HPC Aix-Marseille Université
- **Accélération** : nœuds GPU
- **Données** : champs de vorticité DNS haute résolution
- **Dimensionnalité** : données 4D (temps + espace)

👉 Travail réalisé dans des conditions proches de l’industrie (volumes, contraintes, reproductibilité).


## Architecture du Modèle Spatio-Temporel (ConvLSTM2D)

Le cœur du système repose sur des **cellules ConvLSTM2D**, combinant :

- 🧠 **Mémoire temporelle** (LSTM)
- 🌀 **Extraction spatiale locale** (convolutions)

Cette architecture permet de capturer :

- la morphologie des tourbillons

- leur dynamique non linéaire

- les corrélations spatio-temporelles longues

<div class="code-block">
<pre><code>

**## dataset.py — Chargement et préparation des données DNS**

import numpy as np

def load_dns_data(path, sequence_length=5):
    """
    Charge les champs de vorticité DNS et crée des séquences temporelles
    pour l'entraînement ConvLSTM.

    Shape attendue : (T, H, W)
    Shape sortie X : (N, sequence_length, H, W, 1)
    Shape sortie y : (N, H, W, 1)
    """

    data = np.load(path)                  # (T, H, W)
    data = data[..., np.newaxis]          # (T, H, W, 1)

    X, y = [], []
    for i in range(len(data) - sequence_length):
        X.append(data[i:i + sequence_length])
        y.append(data[i + sequence_length])

    return np.array(X), np.array(y)


**## model.py — Architecture ConvLSTM2D spatio-temporelle**

from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Input, ConvLSTM2D, Conv2D,
    LayerNormalization, Dropout
)

def build_convlstm_model(input_shape):
    """
    Modèle ConvLSTM2D pour la prédiction de champs de vorticité
    """

    inputs = Input(shape=input_shape)

    x = ConvLSTM2D(
        filters=256,
        kernel_size=(3, 3),
        padding="same",
        return_sequences=False
    )(inputs)

    x = LayerNormalization()(x)

    x = Conv2D(
        filters=8,
        kernel_size=(3, 3),
        activation="relu",
        padding="same"
    )(x)

    x = Dropout(0.2)(x)

    outputs = Conv2D(
        filters=1,
        kernel_size=(3, 3),
        activation="linear",
        padding="same"
    )(x)

    return Model(inputs, outputs)


**## train.py — Entraînement du modèle sur infrastructure HPC**

import tensorflow as tf
from dataset import load_dns_data
from model import build_convlstm_model

DATA_PATH = "../data/vorticity_dns.npy"
SEQUENCE_LENGTH = 5
BATCH_SIZE = 1
EPOCHS = 30

**## Chargement des données**

X, y = load_dns_data(DATA_PATH, SEQUENCE_LENGTH)

**## Construction du modèle**

model = build_convlstm_model(
    input_shape=(SEQUENCE_LENGTH, 512, 512, 1)
)

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-4),
    loss="mse"
)

model.summary()

**## Entraînement**

model.fit(
    X, y,
    validation_split=0.1,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE
)


model.save("multi_weights_full.hdf5")


**## predict.py — Prédiction auto-régressive à horizon étendu**

import numpy as np
import tensorflow as tf

MODEL_PATH = "multi_weights_full.hdf5"
DATA_PATH = "../data/vorticity_dns.npy"
SEQUENCE_LENGTH = 5
N_PRED = 10

model = tf.keras.models.load_model(MODEL_PATH)

data = np.load(DATA_PATH)[..., np.newaxis]

sequence = data[:SEQUENCE_LENGTH]
predictions = []

for _ in range(N_PRED):
    pred = model.predict(sequence[np.newaxis])
    predictions.append(pred[0])
    sequence = np.concatenate([sequence[1:], pred], axis=0)

predictions = np.array(predictions)
np.save("predicted_vorticity.npy", predictions)


**## script.slurm — Exécution sur cluster HPC (SLURM)**

#!/bin/bash
#SBATCH --job-name=LSTM
#SBATCH --partition=skylake
#SBATCH --nodes=3
#SBATCH --ntasks-per-node=1
#SBATCH --time=24:00:00
#SBATCH --output=%x.%j.out
#SBATCH --error=%x.%j.err

module load userspace/all
source ~/.bashrc

python train.py
</code></pre>
</div>



## Analyse des Performances

L’évaluation ne se limite pas à une simple loss :

- **Erreur de reconstruction**
- **Stabilité temporelle**
- **Cohérence des structures turbulentes**
- **Comparaison statistique DNS vs prédiction**


<div class="project-hero" style="text-align: center; margin-bottom: 30px;">
  <img src="/images/loss_vorticite.png" 
       alt="Courbe de loss" 
       style="width: 100%; max-width: 900px; height: auto; display: block; margin: 0 auto; border-radius: 8px;">
  <p class="image-caption" style="font-style: italic; color: #888; margin-top: 10px;">
    Évolution de la fonction de perte pendant l’entraînement.
  </p>
</div>


<div class="project-hero" style="text-align: center; margin-bottom: 30px;">
  <img src="/images/comparaison_dns.png"" 
       alt="Comparaison DNS vs prédiction" 
       style="width: 100%; max-width: 900px; height: auto; display: block; margin: 0 auto; border-radius: 8px;">
  <p class="image-caption" style="font-style: italic; color: #888; margin-top: 10px;">
    Comparaison visuelle entre la simulation DNS et la prédiction du modèle.
  </p>
</div>

## Prédiction du Champ de Vorticité

<div class="project-hero" style="text-align: center; margin-bottom: 30px;">
  <img src="/images/predicted_vorticity3.png"" 
       alt="Champ de vorticité prédit" 
       style="width: 100%; max-width: 900px; height: auto; display: block; margin: 0 auto; border-radius: 8px;">
  <p class="image-caption" style="font-style: italic; color: #888; margin-top: 10px;">
    Champ de vorticité prédit par le modèle ConvLSTM2D à horizon temporel étendu.
  </p>
</div>

## Résultats & Enseignements Clés

- ⚡ **Accélération majeure**
  → inférence jusqu’à **50× plus rapide** qu’une DNS classique

- 📈 **Fidélité statistique élevée**
  → bonne conservation des distributions globales

- 🧠 **Apprentissage spatio-temporel robuste**
  → capture des structures turbulentes dominantes

- ⚠️ **Limites identifiées**
  → perte de précision sur les plus petites échelles (analyse critique assumée)

👉 Capacité démontrée à **analyser, quantifier et documenter les limites** du modèle.


## Perspectives de Recherche & Applications Industrielles

Axes d’évolution explorables :

- **Physics-Informed Neural Networks (PINNs)**
  → intégration explicite des équations de Navier–Stokes

- **Architectures avancées**
  → GANs, Transformers spatio-temporels

- **Couplage IA + simulation**
  → accélération de chaînes de calcul industrielles
  (aéronautique, énergie, climat)


## Stack Technique

<div class="tech-stack">
  <span class="badge">Deep Learning</span>
  <span class="badge">ConvLSTM2D</span>
  <span class="badge">TensorFlow / Keras</span>
  <span class="badge">HPC (Mésocentre)</span>
  <span class="badge">Python</span>
</div>
