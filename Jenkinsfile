pipeline {
    agent {
        docker {
            image "python:3.8"
            args "-u root:root"
        }
    }
    stages {
        stage('Environment Setup') {
            steps { 
                echo "The build number is ${env.BUILD_NUMBER}"
                echo "You can also use \${BUILD_NUMBER} -> ${BUILD_NUMBER}"
                sh 'apt-get -y update'
                sh 'apt-get -y install gcc build-essential zlib1g-dev make'
                sh "pip install -r requirements.txt"
                }
        }
        stage('Build-test') {
            steps {
                sh 'python manage.py test'
            }
        }
        stage('Staging deploy') {
            steps {
                echo 'Build-test-t'
            }
        }
    }
}
