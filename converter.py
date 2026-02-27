import pypdf
import os
import glob
import subprocess
from tqdm import tqdm
import time

# Caminhos dinâmicos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(BASE_DIR, "1_COLOCAR_PDF_AQUI")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "2_AUDIOS_PRONTOS")
PIPER_EXE = os.path.join(BASE_DIR, "engine/piper")
PIPER_MODEL = os.path.join(BASE_DIR, "engine/pt_BR-faber-medium.onnx")

CHARS_PER_SECOND = 18 

def formatar_tempo(segundos):
    minutos = int((segundos % 3600) // 60)
    secs = int(segundos % 60)
    return f"{minutos:02d}:{secs:02d}"

def extrair_estrutura_completa(caminho_pdf):
    leitor = pypdf.PdfReader(caminho_pdf)
    capitulos = []
    capitulo_atual = {"titulo": "00_Introducao", "paginas": []}
    gatilhos = ["CAPÍTULO", "CAPITULO", "UNIDADE", "TÓPICO", "TOPICO"]

    # Barra de progresso para a LEITURA do PDF
    for i in tqdm(range(len(leitor.pages)), desc="🔍 Lendo PDF", unit="pag", leave=False):
        pagina = leitor.pages[i]
        texto = pagina.extract_text()
        if not texto: continue
        
        linhas = texto.split('\n')
        primeira_linha = linhas[0].strip() if linhas else ""
        
        if any(g in primeira_linha.upper() for g in gatilhos):
            if capitulo_atual["paginas"]:
                capitulos.append(capitulo_atual)
            
            titulo_limpo = "".join(c for c in primeira_linha if c.isalnum() or c in (' ', '_', '-')).strip()
            capitulo_atual = {"titulo": titulo_limpo[:60], "paginas": []}
        
        capitulo_atual["paginas"].append({"num": i + 1, "texto": texto})
    
    capitulos.append(capitulo_atual)
    return capitulos

def processar():
    arquivos_pdf = glob.glob(os.path.join(INPUT_FOLDER, "*.pdf"))

    if not arquivos_pdf:
        print("Nenhum arquivo encontrado na pasta 1_COLOCAR_PDF_AQUI.")
        return

    for caminho_pdf in arquivos_pdf:
        nome_livro = os.path.basename(caminho_pdf).replace(".pdf", "")
        pasta_destino = os.path.join(OUTPUT_FOLDER, nome_livro)
        os.makedirs(pasta_destino, exist_ok=True)
        
        print(f"\n>>> Livro: {nome_livro}")
        
        # --- PASSO 1: MAPEAMENTO ---
        capitulos = extrair_estrutura_completa(caminho_pdf)
        
        caminho_mapa = os.path.join(pasta_destino, "MAPA_COMPLETO_DO_LIVRO.txt")
        with open(caminho_mapa, "w", encoding="utf-8") as f_mapa:
            f_mapa.write(f"MAPA DE NAVEGAÇÃO: {nome_livro}\n")
            f_mapa.write("="*60 + "\n\n")
            for idx, cap in enumerate(capitulos):
                nome_audio = f"{idx+1:02d}_{cap['titulo']}.mp3"
                f_mapa.write(f"ARQUIVO: {nome_audio}\n")
                tempo_acumulado = 0
                for pg in cap["paginas"]:
                    f_mapa.write(f"   - Página {pg['num']:03d} inicia em {formatar_tempo(tempo_acumulado)}\n")
                    tempo_acumulado += len(" ".join(pg["texto"].split())) / CHARS_PER_SECOND
                f_mapa.write("\n")

        print(f"✓ Mapa gerado! Iniciando conversão de {len(capitulos)} capítulos.")

        # --- PASSO 2: CONVERSÃO COM BARRA DE LOADING ---
        # Esta barra mostra o progresso GERAL dos capítulos
        for idx, cap in enumerate(tqdm(capitulos, desc="🎧 Convertendo Áudios", unit="cap")):
            num_cap = f"{idx+1:02d}"
            nome_base = f"{num_cap}_{cap['titulo']}"
            caminho_wav = os.path.join(pasta_destino, f"{nome_base}.wav")
            caminho_mp3 = os.path.join(pasta_destino, f"{nome_base}.mp3")
            
            texto_todo = ""
            for pg in cap["paginas"]:
                texto_todo += " ".join(pg["texto"].split()) + "  "

            # Síntese Piper
            processo = subprocess.Popen(
                [PIPER_EXE, "--model", PIPER_MODEL, "--output_file", caminho_wav],
                stdin=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True
            )
            processo.communicate(input=texto_todo)

            # Conversão FFmpeg
            if os.path.exists(caminho_wav):
                subprocess.run([
                    "ffmpeg", "-y", "-i", caminho_wav, "-codec:a", "libmp3lame", 
                    "-qscale:a", "2", caminho_mp3
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                os.remove(caminho_wav)
                
                # O tqdm já mostra a barra, mas manter o print ajuda ela a saber qual arquivo deu play
                tqdm.write(f"   [OK] {nome_base}.mp3 finalizado.")

    print(f"\n✨ Tudo pronto! Os áudios estão na pasta: {nome_livro}")

if __name__ == "__main__":
    processar()
