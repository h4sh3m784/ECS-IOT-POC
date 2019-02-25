node{
    def app

    stage('Clone repository'){
    /* Let's make sure we have the repository cloned to our workspace */
        checkout scm
    }
    stage('Build Image'){
        /* This builds the actual image: synonymous to
            docker build on the command line */
            docker.build("jenkins-demo")
    }

    stage('Test Image'){
        echo "Image is build!"   
    }
}