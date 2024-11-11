# Chatbot

Este projeto visa criar um chatbot interativo que aprenda e se adapte com base nas interações do usuário. O chatbot armazena informações relevantes apenas quando o usuário fornece dados verdadeiros ou expressa preferências (como preferir um tom mais formal).

## Instalação 
### 1. Docker:
 - Certifique-se de ter o [Docker](https://www.docker.com/products/docker-desktop/) na sua máquina

### 2. Chave de api Groq:
Para acessar os modelos Groq, você precisará criar uma conta no [Groq](https://groq.com/) para obter uma chave de API.

### 3. Clone o Repositório:
```bash
git clone https://github.com/IzacPS/chatbot.git
cd chatbot
```
### 4. Variáveis de ambiente:
Configure a variável de ambiente **GROQ_API_KEY** com a chave de api que você criou no 
[Groq](https://groq.com/).

bash
```
export GROQ_API_KEY="sua_chave_de_api_aqui"
```
powershell
```
$env:GROQ_API_KEY="sua_chave_de_api_aqui"
```

### 3. Langsmith (opcinal):
Você pode optar por usar a plataforma **Langsmith** para depurar os estados no **Langgraph**.
Crie uma conta, ou logue no [Langsmith](https://www.langchain.com/langsmith) e obtenha uma chave de api.
Após obter a chave você pode configurar da seguinte forma:

bash
```
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_API_KEY="sua_chave_de_api_aqui"
```
powershell
```
$env:LANGCHAIN_TRACING_V2="true"
$env:LANGCHAIN_API_KEY="sua_chave_de_api_aqui"
```

### 3. Executar:

Para executar o projeto basta usar o  *docker compose*.
Primeiro faça o build das imagens.

```bash
docker compose build
```
Em seguida basta subir as imagens com o comando.
```bash
docker compose up
```

Se preferir você pode buildar e executar ao mesmo tempo com o comando. Lembrando que
esse comando irá reconstruir as imagens do zero a cada execução.
```bash
docker compose up --build
```

Agora você pode acessar o chat em `http://localhost:8501`.

(Obs): O chat pode demorar um pouco pra carregar. Por algum motivo que eu ainda desconheço está demorando 
algum tempo pra carregar a página do chat.

<img src="./images/chat.png" alt="drawing" width="500"/>

### Tecnologias Utilizadas

- **Interface de Usuário (UI) com Streamlit**:  Uma ferramenta para a criação de interfaces de chat de forma rápida.
- **LangGraph & Langchain**: Bibliotecas fundamentais para a construção do chatbot, integrando o processamento de linguagem natural e a adaptação de comportamento.
- **LLM (Modelo de Linguagem)**: Foi utilizado o modelo de linguagem llama3-70b-8192 e llama3-8b-8192 disponíves em [Groq](https://groq.com/).
- **Base de Dados Vetorial PGVector**: Armazenamento eficiente das informações relevantes do usuário, usando a base de dados vetorial PGVector.
