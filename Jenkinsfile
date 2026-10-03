pipeline {
    agent any

    environment {
        IMAGE_NAME = "localhost:5000/project-nexus"
        IMAGE_TAG  = "${BUILD_NUMBER}"
        KUBECONFIG = "/var/lib/jenkins/.kube/config"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --no-cache-dir -r applications/requirements.txt
                    python -m py_compile applications/app.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                      -t ${IMAGE_NAME}:${IMAGE_TAG} \
                      -t ${IMAGE_NAME}:latest \
                      .
                '''
            }
        }

        stage('Push Image') {
            steps {
                sh '''
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    docker push ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Deploy to K3s') {
            steps {
                sh '''
                    kubectl apply -f k8s/namespace.yaml
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml

                    kubectl -n project-nexus \
                      set image deployment/project-nexus \
                      project-nexus=${IMAGE_NAME}:${IMAGE_TAG}

                    kubectl -n project-nexus \
                      rollout status deployment/project-nexus --timeout=120s
                '''
            }
        }

        stage('Verify') {
            steps {
                sh '''
                    kubectl -n project-nexus get pods
                    kubectl -n project-nexus get service
                '''
            }
        }
    }

    post {
        success {
            echo 'Project Nexus deployment completed successfully.'
        }

        failure {
            echo 'Project Nexus pipeline failed.'
        }
    }
}
