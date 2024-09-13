import assemblyai as aai
import os
import openai
import subprocess
from datetime import datetime

# Chaves de API - Certifique-se de manter essas chaves em segurança.
aai.settings.api_key = ""
openai.api_key = ""

# Diretório onde estão os arquivos para transcrição
PASTA_TRANSCRICAO = 'Transcrever'
PASTA_SAIDA = 'Transcricao'

# Função para verificar se o arquivo de áudio existe
def validar_arquivo(file_url):
    if not os.path.exists(file_url):
        raise FileNotFoundError(f"O arquivo '{file_url}' não foi encontrado.")
    return True

# Função para converter o áudio para MP3 usando FFmpeg através de subprocess
def converter_para_mp3(input_file, pasta_destino):
    formato = os.path.splitext(input_file)[1][1:].lower()
    output_file = os.path.join(pasta_destino, os.path.splitext(os.path.basename(input_file))[0] + ".mp3")

    if formato == "mp3":
        print(f"O arquivo {input_file} já está em formato MP3. Não é necessário converter.")
        return input_file  # Retorna o arquivo original se já for MP3

    try:
        # Usar FFmpeg para converter o arquivo de áudio para MP3
        comando = ["ffmpeg", "-i", input_file, output_file]

        print(f"Convertendo {input_file} de {formato} para MP3 usando FFmpeg...")
        resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if resultado.returncode != 0:
            print(f"Erro ao converter o arquivo: {resultado.stderr.decode('utf-8')}")
            return None

        print(f"Conversão concluída: {output_file}")
        return output_file

    except Exception as e:
        print(f"Erro ao converter o arquivo: {e}")
        return None

# Configuração de transcrição
config = aai.TranscriptionConfig(language_code="pt")

# Função para transcrever o áudio
def transcrever_audio(file_url, config):
    transcriber = aai.Transcriber()
    
    try:
        print(f"Iniciando a transcrição do arquivo: {file_url}")
        transcript = transcriber.transcribe(file_url, config)
        
        if transcript.status == aai.TranscriptStatus.error:
            print(f"Erro durante a transcrição: {transcript.error}")
        else:
            print("Transcrição concluída com sucesso!")
            return transcript.text
    except Exception as e:
        print(f"Ocorreu um erro ao tentar transcrever o arquivo: {e}")
        return None

# Salvar o texto transcrito em um arquivo
def salvar_transcricao_em_arquivo(texto, arquivo_destino):
    try:
        with open(arquivo_destino, "w", encoding="utf-8") as file:
            file.write(texto)
        print(f"Transcrição salva em '{arquivo_destino}'")
    except Exception as e:
        print(f"Erro ao salvar a transcrição: {e}")

# Função para enviar a transcrição para o ChatGPT e obter a resposta
def enviar_para_chatgpt(transcricao):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Organize em bullet essa transcrição de conversa:\n\n{transcricao}",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7
        )
        
        resposta_chatgpt = response.choices[0].text.strip()
        return resposta_chatgpt
    except Exception as e:
        print(f"Erro ao enviar para o ChatGPT: {e}")
        return None

# Salvar a resposta do ChatGPT em um arquivo
def salvar_resposta_chatgpt_em_arquivo(resposta, arquivo_destino):
    try:
        with open(arquivo_destino, "w", encoding="utf-8") as file:
            file.write(resposta)
        print(f"Resposta do ChatGPT salva em '{arquivo_destino}'")
    except Exception as e:
        print(f"Erro ao salvar a resposta do ChatGPT: {e}")

# Perguntar ao usuário sobre a conversa e envio para o ChatGPT
def obter_input_usuario():
    mesma_conversa = input("Os áudios são da mesma conversa? (s/n): ").strip().lower() == 's'
    enviar_chatgpt = input("Deseja enviar as transcrições para o ChatGPT? (s/n): ").strip().lower() == 's'

    if mesma_conversa and not enviar_chatgpt:
        salvar_unico_arquivo = input("Deseja salvar todas as transcrições em um único arquivo? (s/n): ").strip().lower() == 's'
    else:
        salvar_unico_arquivo = None

    return mesma_conversa, enviar_chatgpt, salvar_unico_arquivo

# Criar pasta para salvar as transcrições e MP3
def criar_pasta_saida():
    data_hora_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    caminho_pasta = os.path.join(PASTA_SAIDA, data_hora_atual)
    
    if not os.path.exists(caminho_pasta):
        os.makedirs(caminho_pasta)
    
    return caminho_pasta

# Função principal para processar todos os arquivos na pasta "Transcrever"
def processar_pasta_transcrever(pasta):
    if not os.path.exists(pasta):
        raise FileNotFoundError(f"A pasta '{pasta}' não foi encontrada.")
    
    arquivos = [f for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f))]
    
    if not arquivos:
        print(f"Não foram encontrados arquivos na pasta '{pasta}'.")
        return

    # Ordenar arquivos pelo nome para garantir que o processamento ocorra do mais antigo ao mais recente
    arquivos.sort()

    # Criar pasta de saída para as transcrições e MP3
    pasta_saida = criar_pasta_saida()

    mesma_conversa, enviar_chatgpt, salvar_unico_arquivo = obter_input_usuario()
    transcricoes = []

    for arquivo in arquivos:
        caminho_arquivo = os.path.abspath(os.path.join(pasta, arquivo))
        print(f"Processando o arquivo: {caminho_arquivo}")

        try:
            arquivo_mp3 = converter_para_mp3(caminho_arquivo, pasta_saida)

            if arquivo_mp3:
                transcricao = transcrever_audio(arquivo_mp3, config)

                if transcricao:
                    transcricoes.append((arquivo_mp3, transcricao))

        except Exception as e:
            print(f"Erro ao processar o arquivo {arquivo}: {e}")

    if mesma_conversa:
        # Transcrição única para todos os arquivos, ordenada conforme os nomes
        transcricao_final = "\n\n".join([t[1] for t in transcricoes])

        if salvar_unico_arquivo is not None and salvar_unico_arquivo:
            salvar_transcricao_em_arquivo(transcricao_final, os.path.join(pasta_saida, "transcricao_unica.txt"))
        else:
            for arquivo, transcricao in transcricoes:
                nome_arquivo_transcricao = os.path.splitext(os.path.basename(arquivo))[0] + "_transcricao.txt"
                salvar_transcricao_em_arquivo(transcricao, os.path.join(pasta_saida, nome_arquivo_transcricao))

        if enviar_chatgpt:
            resposta_chatgpt = enviar_para_chatgpt(transcricao_final)
            if resposta_chatgpt:
                salvar_resposta_chatgpt_em_arquivo(resposta_chatgpt, os.path.join(pasta_saida, "resposta_chatgpt_unica.txt"))

    else:
        # Transcrição separada para cada arquivo
        for arquivo, transcricao in transcricoes:
            nome_arquivo_transcricao = os.path.splitext(os.path.basename(arquivo))[0] + "_transcricao.txt"
            salvar_transcricao_em_arquivo(transcricao, os.path.join(pasta_saida, nome_arquivo_transcricao))

            if enviar_chatgpt:
                resposta_chatgpt = enviar_para_chatgpt(transcricao)
                if resposta_chatgpt:
                    nome_arquivo_resposta = os.path.splitext(os.path.basename(arquivo))[0] + "_resposta_chatgpt.txt"
                    salvar_resposta_chatgpt_em_arquivo(resposta_chatgpt, os.path.join(pasta_saida, nome_arquivo_resposta))

# Executar o processamento da pasta "Transcrever"
processar_pasta_transcrever(PASTA_TRANSCRICAO)
