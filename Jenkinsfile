node{
    def app

    //Much code
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
            script: "HOME=/home/ubuntu && env && sudo env && sudo aws ecr get-login --no-include-email --region us-east-1 --debug",
            returnStatus: true
            ) == 0
        LOGIN_WITH_TOKEN = sh(
            script: "${GET_TOKEN}",
            returnStatus: true
            )==0
        
        LOGIN_RESULT = sh("sudo ${LOGIN_WITH_TOKEN}")
        echo "Logged in.."
        
        sh("docker tag jenkins-demo 740976047420.dkr.ecr.us-east-1.amazonaws.com/my-web-interface")
        sh("docker push 740976047420.dkr.ecr.us-east-1.amazonaws.com/my-web-interface")
    }
}