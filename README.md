# 📚 PDF to Study Audio (Piper TTS)

Um conversor robusto e **100% offline** de PDFs acadêmicos para áudio (MP3), projetado para facilitar o estudo de livros universitários. O script detecta automaticamente capítulos, unidades e tópicos, dividindo o conteúdo em arquivos organizados e gerando um mapa de navegação com timestamps.

## ✨ Diferenciais

- **Privacidade & Offline:** Não envia dados para nuvem. Todo o processamento é feito localmente usando o motor **Piper TTS**.
- **Divisão Inteligente:** Identifica palavras-chave como "Unidade", "Capítulo" ou "Tópico" para segmentar os áudios.
- **Mapa de Estudo:** Gera um arquivo `.txt` único com o índice de cada página dentro dos arquivos de áudio.
- **Interface Intuitiva:** Barra de progresso visual (`tqdm`) e logs em tempo real que avisam assim que um capítulo está pronto para ouvir.
- **Conversão Otimizada:** Utiliza **FFmpeg** para garantir arquivos MP3 leves e compatíveis com qualquer player/celular.

## 🛠️ Pré-requisitos (Linux)

Antes de rodar o script, garanta que você possui as dependências de sistema instaladas:

sudo apt update
sudo apt install python3-venv ffmpeg wget -y
🚀 Como instalar e usar
Clone o repositório:


git clone git@github.com:sergiomartinssilva/conversorPdf.git
cd conversorPdf
Dê permissão de execução ao script de inicialização:

chmod +x iniciar_conversao.sh

Coloque seus arquivos:
Insira os livros em PDF na pasta 1_COLOCAR_PDF_AQUI/.

Execute:


./iniciar_conversao.sh
Nota: Na primeira execução, o script baixará automaticamente o motor do Piper e o modelo de voz em português brasileiro (~100MB).

📁 Estrutura do Projeto
Plaintext
.
├── 1_COLOCAR_PDF_AQUI/   # Coloque seus PDFs aqui
├── 2_AUDIOS_PRONTOS/     # Seus MP3s e Mapas estarão aqui
├── engine/               # Binários do Piper e Vozes (Auto-gerado)
├── converter.py          # Script principal (Maestro)
├── iniciar_conversao.sh  # Script de automação (Venv + Run)
└── README.md
⚙️ Tecnologias Utilizadas
Python 3

Piper TTS - Síntese de voz local via Redes Neurais.

PyPDF - Extração de texto de PDFs.

FFmpeg - Conversão e compressão de áudio.

TQDM - Barras de progresso para CLI.

Desenvolvido com foco em acessibilidade e produtividade nos estudos. 🎓
