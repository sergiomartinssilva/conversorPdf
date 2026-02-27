#!/bin/bash
APP_DIR="/home/s-rgio-martins/apps/conversorPdf"
cd "$APP_DIR" || exit

mkdir -p "1_COLOCAR_PDF_AQUI" "2_AUDIOS_PRONTOS" "engine"

# Baixar Piper se necessário
if [ ! -f "engine/piper" ]; then
    echo "Baixando motor Piper..."
    wget -q --show-progress https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz
    tar -xf piper_amd64.tar.gz -C engine --strip-components=1
    rm piper_amd64.tar.gz
fi

# Baixar Voz se necessário
if [ ! -f "engine/pt_BR-faber-medium.onnx" ]; then
    echo "Baixando voz PT-BR..."
    wget -q --show-progress -O engine/pt_BR-faber-medium.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx
    wget -q --show-progress -O engine/pt_BR-faber-medium.onnx.json https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json
fi

if [ ! -d "venv" ]; then python3 -m venv venv; fi
./venv/bin/pip install -q pypdf tqdm

echo "--- Iniciando Conversão (Piper + FFmpeg) ---"
./venv/bin/python3 converter.py

echo ""
echo "Concluído! Seus MP3 estão na pasta 2_AUDIOS_PRONTOS."
echo "Pressione qualquer tecla para sair."
read -n 1
