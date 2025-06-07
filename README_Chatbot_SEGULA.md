
# 🤖 Chatbot RH – SEGULA Technologies

Ce projet est un chatbot RH intelligent développé dans le cadre de mon stage au sein de SEGULA Technologies. Il vise à assister les collaborateurs sur les questions RH les plus fréquentes (congés, maternité, procédures RH…) à travers une interface simple et intuitive.

---

## ✅ Fonctionnalités principales

- 🔍 Recherche sémantique dans une base FAQ RH (questions/réponses)
- 🤖 Requête automatique à l’IA Gemini (Google) si la réponse est absente
- 📎 Lecture de fichiers PDF, Excel, TXT pour analyse de contenu RH
- 💬 Interface conversationnelle type WhatsApp (avec historique)
- 💾 Enregistrement automatique des échanges dans un fichier Excel

---

## ⚙️ Technologies utilisées

- Python 3.10+
- Streamlit
- pandas, openpyxl, sentence-transformers
- google-generativeai
- PyMuPDF pour lecture de PDF

---

## 📁 Contenu du projet

| Fichier | Description |
|--------|-------------|
| app.py | Interface principale du chatbot RH |
| ai_gemini.py | Fichier d’appel à l’API Gemini |
| questions_reponses_rh_segula.xlsx | Base de données des questions/réponses RH |
| chat_segula_log.xlsx | Historique des discussions |
| .env | Contient la clé API Gemini |
| requirements.txt | Dépendances nécessaires |
| SEGULA_Technologies_logo_DB.jpg | Logo intégré dans l’interface |

---

## 🚀 Lancement de l’application

1. Installer les dépendances :

```bash
pip install -r requirements.txt
```

2. Créer un fichier .env avec la clé API Gemini :

```env
GEMINI_API_KEY=VOTRE_CLE_GEMINI_ICI
```

3. Lancer l’application :

```bash
streamlit run app.py
```

---

## ❗ Important

- Les questions/réponses sont lues depuis le fichier questions_reponses_rh_segula.xlsx
- Si une réponse est absente ou vide, le chatbot interroge automatiquement Gemini
- L’historique est enregistré dans chat_segula_log.xlsx

---

## 👩‍💼 Utilisation par le service RH

- Le service RH peut modifier le fichier questions_reponses_rh_segula.xlsx directement via Excel
- Aucune compétence technique n’est requise pour ajouter ou mettre à jour les réponses

---

## 📌 Exemple de question :

> 💬 Je suis enceinte, que dois-je faire vis-à-vis de mon travail ?  
> 🧠 Le chatbot répondra depuis la FAQ, ou utilisera Gemini si la réponse est absente.

---

## 🙏 Remerciements

Je remercie Mme Rita (RH) et toute l’équipe de SEGULA pour leur accompagnement, leurs retours et leur soutien dans la réalisation de ce projet.

---

## 📅 Réalisé par :

**Fatima Zahra Mghizlat Idrissi**  
Stagiaire Développement Digital – SEGULA Technologies  
Stage réalisé entre [date début] et [date fin]
