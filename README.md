#### This is the documentation for the Web API running in ECS Fargate.

The API Path is an HTTP proxy passthrough, so every device will have it's own path making it RESTfull:

    www.example.amazon.com/device-request/{device-id}

##### Serverless
Upload the serverless,yml file to AWS Cloudformation
Which will create a taskdefinition

```
        WebInterfaceTaskDefinition:
      Type: AWS::ECS::TaskDefinition
      DependsOn: [iotExecutionRole, iotExecutionPolicy, XrayDaemonRepo, WebInterfaceRepo]
      Properties:
          Cpu: 512
          Memory: 1024
          Family: "Web-Api"
          NetworkMode: "awsvpc"
          TaskRoleArn: 
            Ref: iotExecutionRole
          ExecutionRoleArn: !GetAtt iotExecutionRole.Arn
          RequiresCompatibilities: 
            - FARGATE
          ContainerDefinitions:
          - Name: "xray-daemon"
            Image: !Ref XrayDaemonRepo
            Cpu: 192
            MemoryReservation: 256
            PortMappings:
              - ContainerPort: 2000
                Protocol: "udp"
                
          - Name: "WebInterface"
            Image: !Ref WebInterfaceRepo
            Cpu: 192
            MemoryReservation: 512
```
