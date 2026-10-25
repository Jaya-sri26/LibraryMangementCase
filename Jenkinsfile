pipeline {
    agent any

    stages {

        stage('Run Tests with pytest') {
            steps {
                echo "Running Flask tests using pytest"

                bat 'python -m pip install -r requirements.txt'

                bat 'start /B python app.py'

                bat 'ping 127.0.0.1 -n 5 > nul'

                bat 'python -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Build Docker Image"
                bat "docker build -t libraryapp:v1 ."
            }
        }

        stage('Docker Login') {
            steps {
                bat 'docker login -u jaya02sri26 -p Jaya@sri26'
            }
        }

        stage('Push Docker Image to Docker Hub') {
            steps {
                echo "Push Docker Image to Docker Hub"
                bat "docker tag libraryapp:v1 jaya02sri26/library:librarytestimage"
                bat "docker push jaya02sri26/library:librarytestimage"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f deployment.yaml --validate=false'
                bat 'kubectl apply -f service.yaml'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}