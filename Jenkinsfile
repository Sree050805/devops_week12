pipeline {
    agent any

    environment {
        PATH = "/usr/local/bin:/opt/homebrew/bin:${env.PATH}"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t sreeja6/devops_week12:latest .'
            }
        }

        stage('Docker Login and Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_TOKEN'
                )]) {
                    sh 'echo "$DOCKER_TOKEN" | docker login -u "$DOCKER_USER" --password-stdin'
                    sh 'docker push sreeja6/devops_week12:latest'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f deployment.yaml'
                sh 'kubectl apply -f service.yaml'

                sh 'kubectl rollout restart deployment/week12-deployment'

                sh '''
                    kubectl rollout status deployment/week12-deployment \
                    --timeout=120s
                '''
            }
        }

        stage('Run Selenium Tests') {
            steps {
                sh '''
                   python3 -m venv .venv
            .venv/bin/python -m pip install --upgrade pip
            .venv/bin/python -m pip install pytest selenium webdriver-manager
            .venv/bin/python -m pytest tests/test_registration.py -v -s
                '''
            }
        }
    }

    post {
        success {
            echo 'Week 12 deployment and Selenium testing completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the logs.'
        }
    }
}
