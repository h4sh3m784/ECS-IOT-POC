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

    stage("Serverless/Cloudformation"){
        if(params.isServerlessActive){
            sh("cd serverless && sls deploy -v && cd ..")
            sh('echo "kekekekek"')
        }
    }
    
    stage('Push To AWS Repo'){
        
        GET_TOKEN = sh(
            script: "sudo aws ecr get-login --no-include-email --region ${AWS_REGION} --debug",
            returnStdout: true
            ).trim()
        
        LOGIN = sh(
            script: "sudo ${GET_TOKEN}",
            retrunStdout: true
            )
            
        sh("sudo docker tag jenkins-demo ${AWS_ECR_REPO}")
        sh("sudo docker push ${AWS_ECR_REPO}")
    }

    stage("Start ECS-Task"){
        GET_TASKS = sh(
            script:"sudo aws ecs list-tasks --cluster default --region ${AWS_REGION} --output text --query taskArns[0]",
            returnStdout: true
            ).trim()
            
         if("${GET_TASKS}" == "None"){
            sh("echo 'Nothings running..'")
            sh("sudo aws ecs run-task --cluster default --task-definition ${AWS_TASK_DEFINITION} --region ${AWS_REGION} --launch-type FARGATE --network-configuration 'awsvpcConfiguration={subnets='${AWS_TASK_SUBNET}',securityGroups='${AWS_TASK_SECURITY_GROUP}',assignPublicIp='ENABLED'}'")
        }else{
            sh("echo 'Tasks are running..'")
            sh("echo Stopping Tasks")

            sh("sudo aws ecs stop-task --cluster default --region ${AWS_REGION} --task ${GET_TASKS}")
            sh("sudo aws ecs run-task --cluster default --task-definition ${AWS_TASK_DEFINITION} --region ${AWS_REGION} --launch-type FARGATE --network-configuration 'awsvpcConfiguration={subnets='${AWS_TASK_SUBNET}',securityGroups='${AWS_TASK_SECURITY_GROUP}',assignPublicIp='ENABLED'}'")
        }
    }
}