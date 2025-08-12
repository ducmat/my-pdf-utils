#!/bin/bash

# Script de test pour vérifier le fonctionnement local des workflows

echo "🧪 Test des workflows PDF Generator"
echo "=================================="

# Créer une image de test
echo "📸 Création d'une image de test..."
python3 -c "
from PIL import Image
img = Image.new('RGB', (400, 400), color='blue')
img.save('test_image.png')
print('✅ Image de test créée: test_image.png')
"

# Test avec 3 images
echo ""
echo "📄 Génération du PDF avec 3 images..."
poetry run my-pdf-utils test_image.png 3 --output-path "test_output_3.pdf" --title "Test 3 Images"

# Test avec 6 images  
echo ""
echo "📄 Génération du PDF avec 6 images..."
poetry run my-pdf-utils test_image.png 6 --output-path "test_output_6.pdf" --title "Test 6 Images"

# Test avec 12 images
echo ""
echo "📄 Génération du PDF avec 12 images..."
poetry run my-pdf-utils test_image.png 12 --output-path "test_output_12.pdf" --title "Test 12 Images"

echo ""
echo "📋 Résultats:"
ls -la test_output_*.pdf 2>/dev/null || echo "❌ Aucun PDF généré"

echo ""
echo "🧹 Nettoyage..."
rm -f test_image.png test_output_*.pdf

echo "✅ Tests terminés!"
