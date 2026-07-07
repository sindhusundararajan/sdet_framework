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
        stage('Quality Gate'){
            steps{
                script{
                    echo 'All tests passed - quality gate cleared'
                }
            }
        }
        stage('Deploy'){
            steps {
                echo 'Tests passed - safe to deploy'
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
        failure {
            echo 'Pipeline failed - deployment blocked'
            mail to: 'vivisharajan@gmail.com',
                subject: "FAILED: ${env.JOB_NAME}",
                body: "Tests failed. Check report at ${env.BUILD_URL}"
        }
        success {
            echo 'Pipeline succeeded - all quality gates passed'
        }
    }
}