# GitHub Workflows - Génération de PDF

Ce repository contient deux workflows GitHub Actions pour générer des PDFs avec des images :

## 🚀 Workflows disponibles

### 1. Generate PDF with Images (`generate-pdf.yml`)
Workflow qui permet de spécifier une URL d'image à télécharger et utiliser.

**Paramètres d'entrée :**
- **Nombre d'images** : Choisir entre 1 et 12 images
- **URL de l'image** : URL vers une image PNG/JPG (par défaut: placeholder)  
- **Nom du fichier de sortie** : Nom du PDF généré
- **Titre du PDF** : Titre du document

### 2. Generate PDF with Sample (`generate-pdf-sample.yml`)
Workflow qui génère une image colorée aléatoire pour démonstration.

**Paramètres d'entrée :**
- **Nombre d'images** : Choisir entre 1 et 12 images
- **Titre du PDF** : Titre du document
- **Nom du fichier de sortie** : Nom du PDF généré

## 📋 Comment utiliser les workflows

1. Allez dans l'onglet **Actions** de votre repository GitHub
2. Sélectionnez le workflow souhaité dans la liste de gauche
3. Cliquez sur **Run workflow** 
4. Remplissez les paramètres requis
5. Cliquez sur **Run workflow** pour lancer l'exécution

## 📦 Récupération des résultats

Après l'exécution du workflow :
- Le PDF généré sera disponible dans les **Artifacts** 
- L'image utilisée sera également sauvegardée (7 jours de rétention)
- Le PDF est conservé 30 jours

## 🛠️ Structure du projet

```
.github/
└── workflows/
    ├── generate-pdf.yml          # Workflow avec URL d'image
    └── generate-pdf-sample.yml   # Workflow avec image générée
```

## 💡 Exemples d'URLs d'images

Voici quelques exemples d'URLs que vous pouvez utiliser :

- `https://via.placeholder.com/400x400.png` (placeholder coloré)
- `https://picsum.photos/400/400` (photo aléatoire)
- `https://via.placeholder.com/400x400/FF0000/FFFFFF?text=Test` (rouge avec texte)

## 🔧 Configuration locale

Pour tester localement, vous pouvez utiliser :

```bash
# Installation des dépendances
poetry install

# Génération d'un PDF
poetry run my-pdf-utils create-multi-images image.png 6 --output-path output.pdf --title "Mon PDF"
```
