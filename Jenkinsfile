pipeline {
    agent any
    environment {
        IMAGE = "iris-mlops"
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Install & Train') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                python train.py
                '''
            }
        }
        stage('Test') {
            steps {
                sh '. venv/bin/activate && pytest -v'
            }
        }
        stage('Docker Build') {
            steps { sh 'docker build -t $IMAGE:${BUILD_NUMBER} -t $IMAGE:latest .' }
        }
        stage('Deploy') {
            steps {
                sh '''
                docker rm -f iris-app || true
                docker run -d --name iris-app -p 5000:5000 $IMAGE:latest
                sleep 5
                curl -f http://localhost:5000/health
                '''
            }
        }
    }
    post {
        success { echo 'Pipeline succeeded' }
        failure { echo 'Pipeline failed' }
    }
}
