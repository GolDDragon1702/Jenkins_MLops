pipeline {
    agent any

    triggers {
        GenericTrigger(
            genericVariables: [
                [key: 'WEBHOOK_TRIGGER', value: '$.trigger', defaultValue: '']
            ],
            causeString: 'Triggered by webhook',
            token: 'push_here',
            printContributedVariables: true,
            printPostContent: true
        )
    }

    options {
        skipDefaultCheckout()
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: "main", url: 'https://github.com/GolDDragon1702/Jenkins_MLops.git'
            }
        }

        stage('Run FastAPI Application') {
            steps {
                script {
                    try {
                        sh '''
                        #!/bin/bash

                        # Check if the container already exists
                        if docker ps -a --format '{{.Names}}' | grep -q "^api_running$"; then
                            echo "Container 'api_running' already exists. Removing it..."
                            docker stop api_running
                            docker rm -f api_running
                        fi

                        # Remove existing Docker image
                        if docker images | grep -q "api"; then
                            echo "Removing existing Docker image..."
                            docker rmi -f api
                        fi

                        # Build and run the FastAPI container
                        docker build -t api .
                        docker run --name api_running -p 80:80 -d api
                        '''
                        withChecks('Run FastAPI App') {
                            publishChecks name: 'Run FastAPI App', status: 'COMPLETED', conclusion: 'SUCCESS',
                                         summary: 'FastAPI container built and running successfully.'
                        }
                    } catch (e) {
                        withChecks('Run FastAPI App') {
                            publishChecks name: 'Run FastAPI App', status: 'COMPLETED', conclusion: 'FAILURE',
                                         summary: 'Pipeline failed while running the FastAPI container.'
                        }
                        throw e
                    }
                }
            }
        }
        
        stage('Testing') {
            steps {
                script {
                    try {
                        sh '''
                        echo "Running tests inside Docker container..."
                        docker exec api_running python3 check.py
                        '''
                        withChecks('Testing') {
                            publishChecks name: 'Testing', status: 'COMPLETED', conclusion: 'SUCCESS',
                                         summary: 'All tests passed successfully.'
                        }
                    } catch (e) {
                        withChecks('Testing') {
                            publishChecks name: 'Testing', status: 'COMPLETED', conclusion: 'FAILURE',
                                         summary: 'Some tests failed.'
                        }
                        throw e
                    }
                }
            }
        }
    }

    post {
        always {
            withChecks('Run FastAPI App') {
                publishChecks name: 'Run FastAPI App', status: 'COMPLETED', conclusion: 'NEUTRAL',
                             summary: 'Pipeline has completed execution.'
            }
        }
    }
}
