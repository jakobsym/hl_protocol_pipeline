pipeline {
    agent {
        docker {
            image 'docker:latest'
            args '-v /var/run/docker.sock:/var/run/docker.sock --user root'
        }
    }
    
    triggers {
        cron('0 */4 * * *') // every 4hrs
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
                withCredentials([
                    string(credentialsId: 'AZURE_CONNECTION_STRING', variable: 'AZURE_CONNECTION_STRING'),
                    string(credentialsId: 'TIMESCALE_CONNECTION_STRING', variable: 'TIMESCALE_CONNECTION_STRING'),
                ]) {
                    script {
                        echo 'Running ETL job with credentials...'
                        sh '''
                            docker run --rm \
                                -e AZURE_CONNECTION_STRING="${AZURE_CONNECTION_STRING}" \
                                -e TIMESCALE_CONNECTION_STRING="${TIMESCALE_CONNECTION_STRING}" \
                                hl_protocol_pipeline:latest \
                                python src/main.py
                        '''
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline completed'
            // clean up if needed
            sh 'docker image prune -f || true'
        }
        failure {
            echo 'Pipeline failed!'
            //notification logic
        }
        success {
            echo 'Pipeline succeeded!'
        }
    }
}