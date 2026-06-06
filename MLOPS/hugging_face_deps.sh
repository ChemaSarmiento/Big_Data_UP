#!/bin/bash
# Forzar la actualización de paquetes e instalar pip para Python 3
apt-get update
apt-get install -y python3-pip

# Instalar las librerías en el entorno global de Python del clúster
# Usamos --no-cache-dir para no llenar el disco del worker
/usr/bin/python3 -m pip install --upgrade pip
/usr/bin/python3 -m pip install transformers datasets torch pandas numpy

echo "Dependencias de Hugging Face instaladas correctamente."