pipeline {
    agent any

    environment {
        MODEL_NAME = 'ml-project'
        GCP_PROJECT = 'groovy-treat-471720-n1'
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
        KUBECTL_AUTH_PLUGIN = "/usr/lib/google-cloud-sdk/bin"
        DOCKER_IMAGE_TAG = "${env.BUILD_NUMBER}"
        GCR_IMAGE = "gcr.io/${GCP_PROJECT}/${MODEL_NAME}:${DOCKER_IMAGE_TAG}"
    }

    stages {
        stage('Cloning from Github') {
            steps {
                script {
                    echo 'Cloning from Github'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'jenkins-github-token', url: 'https://github.com/ZeyOliveira/MLOps_Recommendation_System.git']])
                }
            }
        }

        stage('Setup Python Environment and Install Dependencies') {
            steps {
                script {
                    echo 'Setting up Python virtual environment and installing dependencies on Jenkins agent'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    pip install dvc
                    '''
                }
            }
        }

        stage('Model Training and DVC Push') {
            steps {
                withCredentials([file(credentialsId:'gcp-key', variable:'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Starting model training and pushing artifacts with DVC to GCS'
                        sh '''
                        . ${VENV_DIR}/bin/activate

                        # Garante que o diretório 'artifacts' e 'artifacts/model' existam antes de salvar o modelo
                        mkdir -p artifacts/model

                        # Executa o script de treinamento.
                        # ESTE SCRIPT DEVE SALVAR O MODELO EM 'artifacts/model/'
                        python pipeline/pipeline_training.py

                        # Adiciona o diretório 'artifacts/model' ao DVC e faz o push
                        dvc add artifacts/model/ # <-- AJUSTE AQUI
                        dvc push
                        '''
                    }
                }
            }
        }

        stage('DVC Pull Latest Model') {
            steps {
                withCredentials([file(credentialsId:'gcp-key', variable:'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Pulling latest trained model artifacts with DVC from GCS'
                        sh '''
                        . ${VENV_DIR}/bin/activate
                        # Garante que o diretório 'artifacts' exista antes de puxar o modelo
                        mkdir -p artifacts
                        dvc pull artifacts/model/ # <-- AJUSTE AQUI
                        '''
                    }
                }
            }
        }

        stage('Build and Push Image to GCR') {
            steps {
                withCredentials([file(credentialsId:'gcp-key', variable:'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Building and Pushing Image to GCR'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet
                        docker build -t ${GCR_IMAGE} .
                        docker push ${GCR_IMAGE}
                        '''
                    }
                }
            }
        }

        stage('Deploying to Kubernetes') {
            steps {
                withCredentials([file(credentialsId:'gcp-key', variable:'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Deploying to Kubernetes'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}:${KUBECTL_AUTH_PLUGIN}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud container clusters get-credentials ml-recomend-anime-cluster --region us-central1 --zone us-central1-c
                        sed -i "s|image: gcr.io/${GCP_PROJECT}/${MODEL_NAME}:latest|image: ${GCR_IMAGE}|g" deployment.yaml
                        kubectl apply -f deployment.yaml
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}