pipeline {
    agent any
    environment {
        AZURE_ACCOUNT_NAME = credentials('azure-account-name')
        AZURE_ACCOUNT_KEY = credentials('azure-account-key')
        AZURE_QUEUE_NAME = 'test'
        DOCKER_IMAGE = "muntashir/azure-storage-queue"
        REGISTRY_CREDENTIALS = credentials('your-docker-registry-credentials-id')
        GITOPS_REPO = 'https://your-gitops-repo-url.git'
        K8S_NAMESPACE = 'your-namespace'
    }
    options {
        skipDefaultCheckout true
    }
    stages {
        stage('Checkout') {
            steps {
                script {
                    // Multibranch pipeline: Checkout the branch that triggered the build
                    def branch = env.BRANCH_NAME ?: 'main'
                    checkout([$class: 'GitSCM', branches: [[name: branch]], userRemoteConfigs: [[url: 'https://github.com/muntashir-islam/azure-storage-queue.git']]])
                }
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'pytest'
            }
        }
        stage('Docker Build and Push') {
            steps {
                script {
                    docker.withRegistry('', REGISTRY_CREDENTIALS) {
                        def app = docker.build("${DOCKER_IMAGE}:${env.BRANCH_NAME}-${env.BUILD_ID}")
                        app.push("${env.BRANCH_NAME}-${env.BUILD_ID}")
                        app.push("${env.BRANCH_NAME}-latest")
                    }
                }
            }
        }
        stage('GitOps Deployment') {
            steps {
                script {
                    sh """
                    git clone ${GITOPS_REPO} gitops-repo
                    cd gitops-repo
                    sed -i 's|image: .*|image: ${DOCKER_IMAGE}:${env.BRANCH_NAME}-latest|' k8s/deployment.yaml
                    git config user.name 'jenkins'
                    git config user.email 'jenkins@example.com'
                    git add k8s/deployment.yaml
                    git commit -m 'Deploy ${DOCKER_IMAGE}:${env.BRANCH_NAME}-latest'
                    git push origin main
                    """
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}