node{
    def app

    stage('Clone repository'){
    /* Let's make sure we have the repository cloned to our workspace */
        checkout scm
    }
    stage('Build Image'){
        /* This builds the actual image: synonymous to
            docker build on the command line */
            app = docker.build("jenkins-demo")   
    }

    stage('Login AWS'){
        GET_TOKEN = sh(
            script: "aws ecr get-login --no-include-email --region us-east-1",
            returnStatus: true
            ) == 0
        LOGIN = sh(
            script: "${GET_TOKEN}",
            returnStatus: true
            )==0
        echo "${LOGIN}"
    }
}