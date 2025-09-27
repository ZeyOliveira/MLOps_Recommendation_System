[![author](https://img.shields.io/badge/Zeygler&nbsp;Oliveira-red.svg)](https://www.linkedin.com/in/zeygler-oliveira-a021a92a4/)
[![](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

---

# Sistema de Recomendação de Animes Híbrido

Este repositório é o resultado de uma jornada completa, desde a coleta e processamento de dados de animes até a implantação de um sistema de recomendação em produção, tudo orquestrado com as melhores práticas de Machine Learning Operations (MLOps).

Meu objetivo aqui é mostrar como transformei um problema de negócio real – a necessidade de recomendar conteúdo de forma personalizada – numa solução robusta, escalável e automatizada, utilizando um pipeline de ML de ponta a ponta.

## O Problema e a Solução

Imagine um universo vasto de animes, com milhares de títulos e gêneros. Como ajudar um usuário do seu site a descobrir o próximo anime a ser assistido, de acordo com seus gostos?

*   **O Desafio:** Criar um sistema que entenda as preferências dos usuários e o conteúdo dos animes para oferecer recomendações relevantes.
*   **A Solução:** Um **Sistema de Recomendação de Animes Híbrido**, combinando técnicas de filtragem colaborativa e baseada em conteúdo, desenvolvido com **TensorFlow.Keras**. Este modelo é integrado em um pipeline MLOps completo, garantindo que ele possa ser treinado, versionado, implantado e monitorado de forma contínua e automatizada.

## Projeto: Workflow MLOps

Este projeto foi construído seguindo um workflow MLOps detalhado, garantindo que cada etapa do ciclo de vida do modelo fosse gerenciada de forma eficiente e automatizada. Aqui está um resumo dessa jornada, passo a passo:

### 1. Fonte de Dados e Ingestão

*   **O que foi feito:** Utilizamos o dataset **Anime Recommendation Database 2020 do Kaggle** (`animelist.csv`, `anime_with_synopsis.csv`, `anime.csv`), que contém avaliações de usuários, sinopses para diversos animes.
*   **Ferramenta:** Kaggle Datasets.

### 2. Versionamento de Dados (DVC & Google Cloud Storage)

*   **O que foi feito:** Implementamos o **DVC (Data Version Control)** para versionar o dataset `animelist.csv`, `anime_with_synopsis.csv`, `anime.csv`, `model_checkpont`, `model`, `processed`, `weights` e outros dados intermediários. Os dados são armazenados remotamente em um **Bucket do Google Cloud Storage (GCS)**.
*   **Por que é importante:** Garante a reprodutibilidade dos experimentos. Podemos sempre saber qual versão dos dados foi usada para treinar um modelo específico.
*   **Ferramentas:** DVC, Google Cloud Storage (GCS).
![imagem-docker](https://github.com/ZeyOliveira/MLOps_Recommendation_System/blob/main/docs/screenshots/image_docker_artifact.png)

### 3. Processamento de Dados

*   **O que foi feito:** Limpamos, transformamos e preparamos os dados brutos para o treinamento do modelo. Isso incluiu tratamento de valores ausentes, engenharia de features e codificação de variáveis para o modelo híbrido.
*   **Por que é importante:** Dados de qualidade e bem estruturados são a base para um modelo de Machine Learning performático.
*   **Habilidades:** Python (Pandas, NumPy), pré-processamento de dados, engenharia de features.

### 4. Desenvolvimento e Treinamento do Modelo (TensorFlow.Keras)

*   **O que foi feito:** Desenvolvemos e treinamos um **modelo de recomendação híbrido** utilizando **TensorFlow.Keras**. Este modelo aprende padrões de preferência de usuários e características de animes para gerar recomendações personalizadas.
*   **Por que é importante:** O modelo aprende a complexidade das interações usuário-item.
*   **Habilidades:** Machine Learning (TensorFlow.Keras), arquiteturas de modelos de recomendação, avaliação de modelos.

### 5. Rastreamento de Experimentos (CometML)

*   **O que foi feito:** Utilizamos o **CometML** para rastrear cada experimento de treinamento do modelo. Registramos métricas (loss, mse, mae, etc.), hiperparâmetros, código-fonte, dependências e artefatos do modelo.
*   **Por que é importante:** Essencial para comparar diferentes iterações do modelo, entender qual abordagem performou melhor e garantir a reprodutibilidade dos resultados.
*   **Ferramenta:** CometML.
![cometml](https://github.com/ZeyOliveira/MLOps_Recommendation_System/blob/main/docs/screenshots/graphics_cometml.png)

### 6. Containerização (Docker)

*   **O que foi feito:** Empacotamos o modelo treinado e a lógica de inferência numa **imagem Docker**. Isso inclui todas as dependências e o ambiente necessário para o modelo rodar de forma isolada.
*   **Por que é importante:** Garante que o modelo funcione de forma consistente em qualquer ambiente, do desenvolvimento à produção, eliminando problemas de compatibilidade.
*   **Ferramenta:** Docker (Dockerfile).
![conteiner-docker](https://github.com/ZeyOliveira/MLOps_Recommendation_System/blob/main/docs/screenshots/conteiner_docker.png)

### 7. Registro de Artefatos (Google Artifact Registry)

*   **O que foi feito:** As imagens Docker construídas são versionadas e armazenadas no **Google Artifact Registry (GAR)**.
*   **Por que é importante:** Serve como um repositório centralizado para todas as versões das imagens do nosso sistema, facilitando a implantação e o rollback.
*   **Ferramenta:** Google Container Registry (GAR).

### 8. Pipeline de CI/CD (Jenkins) e Docker-in-Docker

*   **O que foi feito:** Orquestramos todo o fluxo de trabalho com um pipeline de **CI/CD (Integração Contínua/Entrega Contínua)** utilizando **Jenkins**. O `Jenkinsfile` define os estágios de:
    *   Clonagem do repositório
    *   Criação de ambiente virtual e instalação de dependências
    *   `dvc pull` para obter os dados versionados
    *   Construção da imagem Docker do sistema de recomendação
    *   Push da imagem para o GCR
    *   Implantação no Kubernetes
*   **Por que é importante:** Automatiza o ciclo de vida do modelo, garantindo que novas versões sejam testadas e implantadas de forma rápida, segura e consistente.
*   **Ferramenta:** Jenkins (Jenkinsfile, custom_jenkins folder).
![jenkins](https://github.com/ZeyOliveira/MLOps_Recommendation_System/blob/main/docs/screenshots/pipeline_overview_jenkins.png)

### 9. Implantação e Orquestração (Kubernetes no GKE)

*   **O que foi feito:** O sistema de recomendação e sua API são implantados em um cluster **Kubernetes** gerenciado pelo **Google Kubernetes Engine (GKE)**. Utilizamos `deployment.yaml` para definir a infraestrutura.
*   **Por que é importante:** Permite escalar o sistema de recomendação de forma elástica, garantindo alta disponibilidade e resiliência para atender a demanda dos usuários.
*   **Ferramentas:** Clusters, Google Kubernetes Engine (GKE).

### 10. Aplicação do Usuário (Website)

*   **O que foi feito:** Desenvolvemos uma interface web simples (com Flask) para que os usuários possam interagir com o sistema de recomendação e obter sugestões de animes.
*   **Por que é importante:** O modelo só tem valor se puder ser usado! Uma aplicação amigável torna a inteligência artificial acessível e demonstra o impacto do projeto.
*   **Ferramentas:** Python (Flask), desenvolvimento web (HTML/CSS).

---

## Tecnologias e Habilidades em Destaque

Este projeto me permitiu aprofundar e demonstrar minhas habilidades em diversas áreas, essenciais para um profissional de MLOps e Ciência de Dados:

*   **Linguagens de Programação:** Python (intermediário-avançado).
*   **Frameworks de ML:** TensorFlow.Keras (para construção e treinamento do modelo híbrido).
*   **Bibliotecas de Data Science:** Pandas, NumPy, Scikit-learn, Seaborn, Matplotlib.
*   **MLOps:**
    *   **CometML:** Rastreamento de experimentos e registro de modelos.
    *   **DVC (Data Version Control):** Versionamento de dados e modelos.
    *   **Docker:** Containerização de aplicações.
    *   **Jenkins:** Automação de pipelines de CI/CD.
*   **Cloud:** Experiência com Google Cloud Platform (GCP) para:
    *   **Google Cloud Storage (GCS):** Armazenamento de dados.
    *   **Google Container Registry (GCR):** Registro de imagens Docker.
    *   **Google Kubernetes Engine (GKE):** Orquestração e implantação de contêineres.
*   **Desenvolvimento Web:** Flask (para a aplicação de usuário), HTML/CSS.
*   **Versionamento:** Git e GitHub.
*   **Visualização de Dados:** Além das bibliotecas Python, tenho habilidades com Power BI e SQL para dashboards e análises de negócio.

---

## Como Ver o Projeto em Ação

Para explorar este projeto e ver as diferentes etapas em funcionamento, você pode:

*   **Consultar o `Jenkinsfile`:** Entender a automação do pipeline.
*   **Explorar o Código:** Mergulhar na lógica do modelo e da aplicação.
*   **Ver Screenshots:** Imagens das interfaces e resultados. [Screenshots](https://github.com/ZeyOliveira/MLOps_Recommendation_System/tree/main/docs/screenshots)

### Instruções de Execução (Local)

Para rodar o projeto localmente (requer Python 3.11+, `pip`, `git` e `docker` instalados):

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/ZeyOliveira/MLOps_Recommendation_System.git
    cd MLOps_Recommendation_System
    ```
2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Linux/macOS:
    source venv/bin/activate
    # No Windows:
    .\venv\Scripts\activate
    ```
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    pip install -e . # Para instalar o projeto em modo editável
    ```
4.  **Execute o pipeline de treinamento (localmente):**
    ```bash
    python pipeline/pipeline_training.py
    ```
5.  **Rode a aplicação web (localmente):**
    ```bash
    python application.py
    ```

---

Espero que este `README.md` te dê uma visão clara e empolgante do meu trabalho e das minhas capacidades como estudante de Ciência de Dados buscando uma oportunidade na área de TI. Estou aberto a perguntas e ansioso para discutir mais sobre este projeto!

---

**Conecte-se comigo:**

*   **LinkedIn:** https://www.linkedin.com/in/zeygleroliveira/
*   **GitHub:** https://github.com/ZeyOliveira
*   **Gmail:** zeyglerdasilva@gmail.com

