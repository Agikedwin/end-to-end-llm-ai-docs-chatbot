##Create virtual environment
```bash
python3 -m venv cvenv 
```
##Activate virtual environment

```bash
source cvenv/bin/activate
```

```bash
python3 app.py
```

##Stack
- Pinecone
- Flask
- GPT
- LangChain
- Python

## 1.  AWS CICD
Create User
Give user permissions(Access policy)
- generate:
Access key
Secret access key

## 2. create ECR repo to store/save docker image
https://eu-west-1.console.aws.amazon.com/ecr/home?region=eu-west-1

URL : 283016452145.dkr.ecr.eu-west-1.amazonaws.com/mmlchatbot

## 3. Create EC2 machine and setup the requirements
- sudo apt-get update -y
- sudo apt-get upgrade

- curl -fsSL https://get.docker.com -o get-docker.sh
- sudo sh get-docker.sh
- sudo usermod -aG docker ubuntu
- newgrp docker

## 5.  Configure EC2 as a self-hosted runner
- connect it to github

## 6. Setup all gitgub secretes
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_DEFAULT_REGION
- ECR_REPO
- PINECONE_API_KEY
- OPENAI_API_KEY
- 














