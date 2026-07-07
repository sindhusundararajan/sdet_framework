pipeline {
    agent any
    stages {
        stage('Build'){
            steps {
                sh 'docker compose build'
            }
        }
        stage('Test'){
            steps{
                sh 'docker compose up --abort-on-container-exit'
            }
        }
        stage('Report'){
            steps{
                publishHTML([
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: 'Test Report'
                ])
            }
        }
    }
    post {
        always{
            sh 'docker compose down'
        }
    }
}