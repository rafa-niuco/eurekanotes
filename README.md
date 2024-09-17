# EurekaBot

A ideia desse projeto é simplificar a vida de quem tem ideias e fala sozinho sobre elas.

Caso de uso 1: Organizar suas ideias
- Saia caminhar
- Tenha uma ideia
- Mande um audio para você via Whatsaoo
- Chegue em casa e baixe os audios
- Jogue na pasta Transcrever e rode o Eureka.py
- Pronto: todo que falou, será transcrito e sintetizado via chat GPT :D

Caso de uso 2: Construir ideias com amigos
- Converse com alguém via whatsapp Audio
- Tenha uma ideias em conjunto
- Baixe os audios
- Jogue na pasta Transcrever e rode o Eureka.py
- Pronto: todo que falou, será transcrito e sintetizado via chat GPT :D

## Funcionalidades

- Converte automaticamente os arquivos de áudio para o formato MP3 usando o FFmpeg.
- Transcreve os arquivos de áudio utilizando a API da AssemblyAI.
- Oferece opções interativas:
  - Indica se os áudios são parte de uma única conversa ou de várias.
  - Decide se a transcrição deve ser enviada para o ChatGPT para formatação.
- Salva as transcrições em uma pasta organizada por data/hora da execução.
- Transcrições únicas ou múltiplas, de acordo com as respostas do usuário.

## Requisitos

- Python 3.7 ou superior.
- FFmpeg instalado no sistema.
- Chaves de API para AssemblyAI e OpenAI.

## Instalação

### 1. Clone o repositório

Primeiro, clone o repositório para sua máquina local:

```bash
git clone https://github.com/seu-usuario/seu-projeto.git
cd seu-projeto
```

### 2. Crie um ambiente virtual
Crie um ambiente virtual para gerenciar as dependências do projeto:

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as dependências Python
Instale todas as dependências necessárias usando o pip:

```bash
pip install -r requirements.txt
```

### 4. Instale o FFmpeg
Para Ubuntu/Debian (Linux):

```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

Para MacOS:
Se você usa o Homebrew, pode instalar o FFmpeg com o seguinte comando:

```bash
brew install ffmpeg
```

Para Windows:
1. Baixe o FFmpeg da página oficial: [Download FFmpeg](https://ffmpeg.org/download.html).

2. Extraia os arquivos em uma pasta.

3. Adicione a pasta `bin` (que contém `ffmpeg.exe` e `ffprobe.exe`) ao **PATH** do sistema:
   - Clique com o botão direito no **Meu Computador** (ou **Este Computador**) e selecione **Propriedades**.
   - Selecione **Configurações Avançadas do Sistema**.
   - Na aba **Avançado**, clique em **Variáveis de Ambiente**.
   - Nas **variáveis do sistema**, localize a variável `Path`, selecione-a e clique em **Editar**.
   - Clique em **Novo** e adicione o caminho completo da pasta `bin` que contém o `ffmpeg.exe` e o `ffprobe.exe`.
   - Clique em **OK** para salvar as alterações.

4. Verifique se o FFmpeg está instalado corretamente com o comando:

```bash
ffmpeg -version
```

### 5. Configuração das Chaves de API
O projeto utiliza duas APIs: **AssemblyAI** e **OpenAI**. Ambas exigem chaves de API para funcionar corretamente.

#### 5.1. Chave da API do AssemblyAI
1. Crie uma conta ou faça login na [AssemblyAI](https://www.assemblyai.com).
2. Gere uma chave de API e substitua o valor da variável `aai.settings.api_key` no script pelo valor da sua chave.

#### 5.2. Chave da API do OpenAI
1. Crie uma conta ou faça login na [OpenAI](https://platform.openai.com/signup).
2. Gere uma chave de API e substitua o valor da variável `openai.api_key` no script pelo valor da sua chave.

> **Dica**: Para maior segurança, você pode definir essas chaves como variáveis de ambiente e modificá-las no código para usar `os.getenv()`.
