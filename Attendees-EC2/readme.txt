Hay que darle permisos al docker para que pueda ejecutar sentencias de boto3 con 'nuestras' credenciales

Documento que explica como darle permisos al contenedor para que pueda ejecutar sentencias de boto3
https://www.baeldung.com/ops/docker-container-pass-aws-credentials

Hay que crear un IAM role en:
https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-1#/roles/create

Trusted entity type seleccionamos AWS Service > Use Case seleccionamos EC2 > Next

En las poíticas de IAM role añadimos AmazonSQSFullAccess y AmazonSNSFullAccess

De nombre lleva: Attendees_role xd

Hay usar labrole

Ejecutar la ec2 Al final igual toca hacer un ECR