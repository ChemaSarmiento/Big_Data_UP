#!/bin/bash
# Script de Inicialización para Dataproc: Instalar dependencias de Hugging Face
set -e

# Actualizar pip e instalar librerías base de IA
/opt/conda/default/bin/pip install --upgrade pip
/opt/conda/default/bin/pip install transformers datasets pandas numpy torch

echo "Dependencias de Hugging Face instaladas correctamente."