
pipeline {
    agent any

    environment {
        IMAGE_NAME = 'erigelahimaja/appointment-booking'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Test Application') {
            steps {
                bat 'python -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% -t %IMAGE_NAME%:latest .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin'
                    bat 'docker push %IMAGE_NAME%:%BUILD_NUMBER%'
                    bat 'docker push %IMAGE_NAME%:latest'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f k8s/'
                bat 'kubectl set image deployment/appointment-booking appointment-booking=%IMAGE_NAME%:%BUILD_NUMBER%'
                bat 'kubectl rollout status deployment/appointment-booking --timeout=180s'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Appointment Booking System deployed!'
        }
        failure {
            echo 'FAILED: Check the Jenkins console output.'
        }
    }
}
