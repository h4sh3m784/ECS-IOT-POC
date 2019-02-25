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


    stage('Push Image'){
        LOGIN = sh(
            script: "aws --version",
            returnStatus: true
            ) == 0
        echo "${LOGIN}"
    }
}