· Crear bucket de S3 con las distintas capas
	aws s3 mb s3://bucket-data-layers --region us-east-1
	
· Crear carpetas de cada capa en el bucket
	aws s3api put-object --bucket bucket-data-layers --key bronze/
	aws s3api put-object --bucket bucket-data-layers --key silver/
	aws s3api put-object --bucket bucket-data-layers --key gold/

· Ejemplo para conectarse a los datos del S3
	import boto3

	s3 = boto3.client('s3')
	for obj in s3.list_objects(Bucket='mi-bucket-unico', Prefix='gold/')['Contents']:
    	print(obj['Key'])

· Crear role para SageMaker
	aws iam create-role --role-name SageMakerExecutionRole --assume-role-policy-document file://trust-policy.json

· Políticas:
	{
		"Version": "2012-10-17",
		"Statement": [
			{
			"Effect": "Allow",
			"Principal": {
				"Service": "sagemaker.amazonaws.com"
			},
			"Action": "sts:AssumeRole"
			}
		]
	}

	aws iam attach-role-policy --role-name SageMakerExecutionRole --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
	aws iam attach-role-policy --role-name SageMakerExecutionRole --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess

· Crear instancia de SageMaker
	aws sagemaker create-notebook-instance --notebook-instance-name "NotebookInstanceCarlosYJesus" --instance-type "ml.t2.medium" --role-arn "arn:aws:iam::<tu-id-de-aws>:role/SageMakerExecutionRole"


· Crear proyecto streamlit dentro de una instancia de elastic beanstalk:
	eb init -p python-3.8 mi-aplicacion-streamlit --region tu-region
	eb create mi-ambiente-streamlit


· En AWS 
	aws ec2 create-key-pair --key-name MyKeyPair --query 'KeyMaterial' --output text > MyKeyPair.pem
	aws ec2 create-security-group --group-name StreamlitSecurityGroup --description "Security Group for Streamlit application"
	aws ec2 authorize-security-group-ingress --group-id <SecurityGroupId> --protocol tcp --port 8501 --cidr 0.0.0.0/0
	aws ec2 run-instances --image-id ami-0c02fb55956c7d316 --count 1 --instance-type t3.small --key-name <YourKeyName> --security-group-ids <SecurityGroupId> --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=StreamlitApp}]'

· Conectar a instancia EC2
	ssh -i "MyKeyPair.pem" ec2-user@ec2-54-164-63-50.compute-1.amazonaws.com

· Mover codigo 
	scp -i /path/to/your-key-pair.pem /path/to/your-streamlit-app.py ec2-user@your-instance-public-dns:/home/ec2-user

· Ejecutar codigo
	streamlit run your-streamlit-app.py --server.port 8501

· comprimir proyecto
	tar -czvf streamlit.gz proyecto_streamlit/

· descomprimir proyecto
	tar -xvf streamlit.gz
	# Para desplegar -> eb deploy (desde local)
	# Usar github actions para automatizar estos despliegues?


	

