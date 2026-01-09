# Chatbot RAG Industriel — ArcelorMittal

**Système d’accès intelligent à la connaissance industrielle**, conçu et expérimenté en environnement **R&D**, basé sur une architecture avancée de **Retrieval-Augmented Generation (RAG)**.

> 📍 **Contexte :** Projet déployé en milieu industriel réel, répondant à des contraintes strictes de performance, de fiabilité et de confidentialité des données.


<div class="project-hero">
  <img src="/images/photo_visite.jpg" alt="Site industriel ArcelorMittal" style="width:100%; border-radius:12px; box-shadow: 0 4px 20px rgba(0,0,0,0.4);">
  <p class="image-caption" style="text-align:center; font-style:italic; color:#888; margin-top:10px;">
    Site industriel ArcelorMittal (Fos-sur-Mer)
  </p>
</div>


## 🏭 CONTEXTE & ENJEUX MÉTIERS

Au sein d'un complexe industriel international, l’accès rapide à la **connaissance critique** est freiné par la dispersion de l'information :

- **Corpus hétérogène :** Milliers de documents (PDF techniques, procédures ISO, rapports R&D, scans).
- **Limites de la recherche classique :** La recherche par mots-clés échoue sur la sémantique et ne permet pas la synthèse.
- **Risque opérationnel :** Le temps perdu à chercher une information peut impacter la maintenance ou la sécurité.

🎯 **L'Objectif :** Transformer ce corpus passif en un **agent conversationnel proactif**, capable de fournir des réponses fiables, sourcées et contextualisées.


## 🛠️ ARCHITECTURE DU SYSTÈME

Le projet repose sur une approche **Data-Centric**, où chaque étape du pipeline est optimisée pour minimiser le bruit :

### 1. Ingestion & Traitement (Parsing Robuste)

- **Parsing avancé :** Utilisation de `PyMuPDF` et `Marker` pour extraire proprement le texte des documents industriels (tableaux, colonnes, métadonnées).
- **Chunking Dynamique :** Segmentation en fenêtres de **1000 tokens** avec un overlap de **50 tokens** pour préserver la continuité sémantique.

### 2. Retrieval (Recherche Vectorielle)

- **Embeddings :** Utilisation de modèles de pointe (`BGE-Large`, `E5`) optimisés pour le français et l'anglais technique.
- **Vector Index :** Indexation haute performance via `FAISS` ou `ChromaDB` (algorithme HNSW).

### 3. Generation (LLMs Maîtrisés)

- **Modèles Open-Source :** Déploiement local (**Mistral**, **Llama 3**, **DeepSeek**) via `Ollama` pour garantir la **confidentialité on-premise**.
- **Prompt Engineering :** Système de "System Prompt" strict pour limiter les réponses au seul contexte fourni (**Grounding**).

<div class="project-hero" style="text-align: center; margin-bottom: 30px;">
  <img src="/images/architect.png" 
       alt="RAG Architect" 
       style="width: 100%; max-width: 900px; height: auto; display: block; margin: 0 auto; border-radius: 8px;">
  <p class="image-caption" style="font-style: italic; color: #888; margin-top: 10px;">
    Architecture du système de Retrieval-Augmented Generation (RAG)
  </p>
</div>

## 🔬 L'INNOVATION : "OPTIRAG" (ANALYSE DE PERFORMANCE)

Contrairement aux approches "boîte noire", une analyse systématique a été menée pour trouver le point d'équilibre du système :

- **Analyse de sensibilité :** Étude de l'impact de la taille des chunks et du Top-K sur la précision.
- **Clustering de Performance :** Utilisation de `K-Means` pour identifier les configurations les plus stables et réduire les hallucinations.

### Exemple : clustering des configurations RAG

<div class="code-block">

<pre><code>

from sklearn.cluster import KMeans


def optimize_rag(data):
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(data)
    return clusters


</code></pre>

</div>



### Apports Méthodologiques

🔬 Cette approche permet :

- d’identifier des **régimes de performance** stables du système RAG  
- de **réduire significativement les hallucinations** des LLMs  
- d’**objectiver les choix d’architecture** et d’hyperparamètres  

## 🧭 Démarche de Travail

- Approche incrémentale : tests contrôlés avant toute généralisation
- Mesure systématique des effets (qualité, cohérence, stabilité)
- Priorité à la robustesse plutôt qu’à la complexité inutile
- Documentation et traçabilité des choix techniques

## Résultats & Impact Métier

- ⚡ **Accès quasi instantané** à l’information critique  
- ⏱️ **Réduction significative** du temps de recherche documentaire  
- 🧠 **Amélioration de la cohérence et de la précision** des réponses générées  
- 🔐 Architecture **compatible avec des contraintes industrielles** (on-premise, confidentialité)  
- ♻️ Stack **100 % open-source**, industrialisable et maintenable  


## Stack Technique

<div class="tech-stack">
  <span class="badge">RAG</span>
  <span class="badge">LLMs Open-Source</span>
  <span class="badge">PyMuPDF</span>
  <span class="badge">Vector Search</span>
  <span class="badge">Python</span>
  <span class="badge">LangChain</span>
</div>




