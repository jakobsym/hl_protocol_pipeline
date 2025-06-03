pipeline {
    agent {
        docker {
            image 'docker:latest'
            args '-v /var/run/docker.sock:/var/run/docker.sock --user root'
        }
    }
    
    triggers {
        cron('H 2 * * *')
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/jakobsym/hl_protocol_pipeline.git'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building docker image...'
                    sh 'docker build -t hl_protocol_pipeline:latest .'
                }
            }
        }
        
        stage('Run ETL Job') {
            steps {
                script {
                    echo 'Running ETL job...'
                    sh 'docker run -d --name hl_pipeline \
                    -e AZURE_CONNECTION_STRING=${AZURE_CONNECTION_STRING} \
                    -e TIMESCALE_CONNECTION_STRING=${TIMESCALE_CONNECTION_STRING} \
                    hl_protocol_pipeline:latest'
                    // sh 'docker run --rm hl_protocol_pipeline:latest'
                }
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed'
            // clean up
            sh 'docker image prune -f || true'
        }
        failure {
            echo 'Pipeline failed!'
            // notification logic
        }
        success {
            echo 'Pipeline succeeded!'
        }
    }
}