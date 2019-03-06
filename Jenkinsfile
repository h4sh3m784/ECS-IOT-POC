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
    
    stage('Push To AWS Repo'){
        
        GET_TOKEN = sh(
            script: "sudo aws ecr get-login --no-include-email --region eu-west-1 --debug",
            returnStdout: true
            ).trim()
        
        LOGIN = sh(
            script: "sudo ${GET_TOKEN}",
            retrunStdout: true
            )
            
        sh("sudo docker tag jenkins-demo 740976047420.dkr.ecr.eu-west-1.amazonaws.com/web-interface")
        sh("sudo docker push 740976047420.dkr.ecr.eu-west-1.amazonaws.com/web-interface")
    }

    stage("Start ECS-Task"){
        GET_TASKS = sh(
            script:"sudo aws ecs list-tasks --cluster default --region eu-west-1 --output text --query taskArns[0]",
            returnStdout: true
            ).trim()
            
        sh("echo ${GET_TASKS}")
            //Check if a task is already running.
         if("${GET_TASKS}" == "None"){
            sh("echo 'Nothings running..'")
            sh("sudo aws ecs run-task --cluster default --task-definition Web-Api --region eu-west-1 --launch-type FARGATE --network-configuration 'awsvpcConfiguration={subnets='subnet-c6211f9d',securityGroups='sg-ad5ae8d7',assignPublicIp='ENABLED'}'")
        }else{
            sh("echo 'Tasks are running..'")
            sh("echo Stopping Tasks")

            sh("sudo aws ecs stop-task --cluster default --region eu-west-1 --task ${GET_TASKS}")
            sh("sudo aws ecs run-task --cluster default --task-definition Web-Api --region eu-west-1 --launch-type FARGATE --network-configuration 'awsvpcConfiguration={subnets='subnet-c6211f9d',securityGroups='sg-ad5ae8d7',assignPublicIp='ENABLED'}'")
        }
    }
}