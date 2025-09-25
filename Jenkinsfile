pipeline{
    agent any

    stages{
        stage('Cloning from Github'){
            steps{
                script{
                    echo 'Cloning from Github'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'jenkins-github-token', url: 'https://github.com/ZeyOliveira/MLOps_Recommendation_System.git']])
                }
            }
        }
    }
}