# API de Upload, Indexação e Gerenciamento de Arquivos com Redis e Azure Blob Storage

**Versão:** 1.0.0  
**Data de Lançamento:** 21/09/2024

## Descrição Geral
Esta API foi desenvolvida para processar arquivos de diferentes formatos (**PDF**, **DOCX**, **TXT**), extrair o conteúdo, gerar **embeddings** usando o **OpenAI**, indexar os dados no **Redis** e armazenar os arquivos no **Azure Blob Storage**. Além disso, oferece endpoints para **listar** e **deletar** arquivos, com gerenciamento de dados tanto no Redis quanto no Azure Blob.

Essa solução é ideal para sistemas de **busca de documentos** e **recuperação de informações** baseada em embeddings de texto, fornecendo alta performance na indexação e busca de grandes volumes de dados.

## Funcionalidades Principais
- **Upload e Processamento de Arquivos**:
  - Suporte ao upload de arquivos nos formatos **PDF**, **DOCX** e **TXT**.
  - Realiza a sanitização dos nomes dos arquivos para garantir compatibilidade no armazenamento.
  - Extrai o conteúdo dos arquivos e divide em **chunks** configuráveis para melhorar a indexação.

- **Geração de Embeddings**:
  - Usa o **OpenAI** para gerar embeddings dos chunks de texto extraídos.
  - Implementa uma lógica de tentativas automáticas para lidar com falhas temporárias no serviço de embeddings.

- **Indexação no Redis**:
  - Cria um índice vetorial no **Redis** para armazenar embeddings e permitir buscas eficientes.
  - Utiliza o algoritmo **K-Nearest Neighbors (KNN)** para realizar buscas baseadas na similaridade dos embeddings.

- **Armazenamento no Azure Blob Storage**:
  - Armazena os arquivos processados no **Azure Blob Storage** para fácil acesso e gerenciamento.
  - Suporte à **listagem** e **exclusão** de arquivos diretamente do Blob Storage.

## Endpoints da API

### 1. `POST /upload`
Endpoint para upload de arquivos, processamento do conteúdo, geração de embeddings e armazenamento no Redis e Blob Storage.

#### Exemplo de Requisição (Multipart Form Data)

```bash
curl -X POST "https://<sua-api-azure>.azurewebsites.net/api/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/caminho/do/arquivo.pdf" \
  -F "redis_host=seu_host_redis" \
  -F "redis_port=6379" \
  -F "redis_password=sua_senha_redis" \
  -F "openai_embedding_key=sua_chave_openai" \
  -F "openai_embedding_model=text-embedding-3-small" \
  -F "azure_storage_connection_string=sua_string_de_conexao_blob" \
  -F "container_name=nome_do_container" \
  -F "chunk_size=1000" \
  -F "chunk_overlap=200"
```

### 2. `GET /list-files`

Este endpoint permite **listar** todos os arquivos armazenados em um container específico do Azure Blob Storage. É útil para visualizar quais arquivos estão disponíveis para operações futuras, como processamento, download ou exclusão.


#### **Parâmetros**

Os parâmetros devem ser enviados no corpo da requisição como dados de formulário (`multipart/form-data`):

- `azure_storage_connection_string` (obrigatório): A string de conexão ao Azure Blob Storage.
- `container_name` (obrigatório): O nome do container no Azure Blob Storage onde os arquivos estão armazenados.

#### **Exemplo de Requisição**

```bash
curl -X GET "https://<sua-api-azure>.azurewebsites.net/api/list-files" \
  -H "Content-Type: multipart/form-data" \
  -F "azure_storage_connection_string=sua_string_de_conexao_blob" \
  -F "container_name=nome_do_container"
```

### 3. `DELETE /delete-file`

Este endpoint permite **deletar** um arquivo específico do Azure Blob Storage e remover as entradas associadas no Redis. Isso é útil quando você deseja limpar arquivos antigos ou não mais necessários e garantir que o índice de busca esteja atualizado.


#### **Parâmetros**

Os parâmetros devem ser enviados no corpo da requisição como dados de formulário (`multipart/form-data`):

- `redis_host` (obrigatório): O host do Redis para conexão.
- `redis_port` (obrigatório): A porta do Redis (geralmente `6379`).
- `redis_password` (obrigatório): A senha do Redis para autenticação.
- `azure_storage_connection_string` (obrigatório): A string de conexão ao Azure Blob Storage.
- `container_name` (obrigatório): O nome do container no Azure Blob Storage onde o arquivo está armazenado.
- `file_name` (obrigatório): O nome do arquivo que deve ser excluído.

#### **Exemplo de Requisição**

```bash
curl -X DELETE "https://<sua-api-azure>.azurewebsites.net/api/delete-file" \
  -H "Content-Type: multipart/form-data" \
  -F "redis_host=seu_host_redis" \
  -F "redis_port=6379" \
  -F "redis_password=sua_senha_redis" \
  -F "azure_storage_connection_string=sua_string_de_conexao_blob" \
  -F "container_name=nome_do_container" \
  -F "file_name=nome_do_arquivo.pdf"
```