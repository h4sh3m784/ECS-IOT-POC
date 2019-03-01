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
    
    stage("Update Stack In CloudFormation"){
                // script: sh("HOME=/home/ubuntu && sudo aws cloudformation update-stack --stack-name My-ECS-stack --region us-east-1 --template-body file://serverless/serverless.yml")
                sh("sudo cd serverless && sudo serverless --region us-east-1 deploy -v")
    }

    stage('Push To AWS Repo'){
        
        GET_TOKEN = sh(
            script: "sudo aws ecr get-login --no-include-email --region us-east-1 --debug",
            returnStdout: true
            ).trim()
        
        LOGIN = sh(
            script: "sudo ${GET_TOKEN}",
            retrunStdout: true
            )
            
        sh("sudo docker tag jenkins-demo 740976047420.dkr.ecr.us-east-1.amazonaws.com/my-web-interface")
        sh("sudo docker push 740976047420.dkr.ecr.us-east-1.amazonaws.com/my-web-interface")
    }

    stage("Start ECS-Task"){
        GET_TASKS = sh(
            script:"sudo aws ecs list-tasks --cluster my-cluster --region us-east-1 --output text --query taskArns[0]",
            returnStdout: true
            ).trim()
            
        sh("echo ${GET_TASKS}")
        
            //Check if a task is already running.
         if("${GET_TASKS}" == "None"){
            sh("echo 'Nothings running..'")
            sh("sudo aws ecs run-task --cluster my-cluster --task-definition logging --region us-east-1 --launch-type FARGATE --network-configuration 'awsvpcConfiguration={subnets='subnet-93eafad8',securityGroups='sg-0891eafe4dbcc756a',assignPublicIp='ENABLED'}'")
        }else{
            sh("echo 'Tasks are running..'")
            sh("echo Stopping Tasks")

            sh("sudo aws ecs stop-task --cluster my-cluster --region us-east-1 --task ${GET_TASKS}")
            sh("sudo aws ecs run-task --cluster my-cluster --task-definition logging --region us-east-1 --launch-type FARGATE --network-configuration 'awsvpcConfiguration={subnets='subnet-93eafad8',securityGroups='sg-0891eafe4dbcc756a',assignPublicIp='ENABLED'}'")
        }
    }
}