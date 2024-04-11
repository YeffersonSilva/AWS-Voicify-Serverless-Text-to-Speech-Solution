# AWS-Voicify-Serverless-Text-to-Speech-Solution
This project involves creating a serverless application that captures a phrase entered by the user and converts it into an MP3 audio file using AWS's Polly service.

## 💻 How to Use the System

To start working with this project, follow the steps below to install and set up the repository locally.

### 1. Clone the Repository

First, clone the project repository and access the `api-tts/` folder using the following commands in the terminal:

```bash
git clone https://github.com/YeffersonSilva/AWS-Voicify-Serverless-Text-to-Speech-Solution.git
cd AWS-Voicify-Serverless-Text-to-Speech-Solution

```
### 2. Serverless Framework Installation
The Serverless Framework is necessary for deploying the application. Install it globally on your computer:
```bash
npm install -g serverless
```
### 3. 3. Configuration of Credentials and Environment Variables
After generating your AWS credentials (AWS Access Key and AWS Secret) through IAM, configure them along with the necessary environment variables for the project.
```bash
S3_BUCKET=your-s3-bucket-name
DYNAMODB_TABLE=your-dynamodb-table-name

AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_SESSION_TOKEN=your-aws-session-token-optional

```
### 4. 4. Choose Between Running the Project Locally or on AWS

#### 4.1 Running the Project Locally
To run the project locally with the Serverless Framework, you can use serverless offline to simulate the AWS Lambda and API Gateway environment on your local machine.

```bash
# Install the project dependencies
npm install

#Run the server locally
serverless offline
```

After executing the last command, the available endpoints for the application will be listed in your terminal.

#### 4.2 Project Deployment on AWS
To deploy the project on AWS, you can use the serverless deploy command. Make sure your credentials and environment variables are correctly configured and that you have assigned the necessary permissions to interact with the specified AWS services in the project.

```bash
serverless deploy
```

This will deploy your application on AWS using the provided credentials and settings. Upon successful completion, you will receive the API endpoints that can be publicly accessed.




## 🛠Technologies Used
- AWS Lambda: For executing backend code without managing servers.
- AWS API Gateway: To provide endpoints accessible to the end user.
- AWS S3: For storing the generated audio files.
- AWS Polly: For converting text to speech.
- AWS DynamoDB: For storing references of the conversions made.
- Serverless Framework: To facilitate the deployment of the application on AWS.
  
![AWS Lambda](https://img.shields.io/badge/AWS_Lambda-FF9900.svg?style=for-the-badge&logo=aws-lambda&logoColor=white)
![AWS API Gateway](https://img.shields.io/badge/AWS_API_Gateway-FF4F8B.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![AWS S3](https://img.shields.io/badge/AWS_S3-569A31.svg?style=for-the-badge&logo=amazon-s3&logoColor=white)
![AWS Polly](https://img.shields.io/badge/AWS_Polly-232F3E.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![AWS DynamoDB](https://img.shields.io/badge/AWS_DynamoDB-4053D6.svg?style=for-the-badge&logo=amazon-dynamodb&logoColor=white)
![Serverless](https://img.shields.io/badge/Serverless-FD5750.svg?style=for-the-badge&logo=serverless&logoColor=white)

  ## 🚀 Deploy
The application has been deployed and configured on AWS, using the serverless framework to simplify the deployment process and resource management.
Available endpoints:

- **Version 1: `https://xxxx.execute-api.us-east-1.amazonaws.com/v1/tts`
  - Converts text to speech and stores the result in S3.
- **Version 2: `https://xxx.execute-api.us-east-1.amazonaws.com/v2/tts`
  - Extends version 1 by storing conversion references in DynamoDB.
- **Version 3: `https://xxx.execute-api.us-east-1.amazonaws.com/v3/tts`
  - Checks if a conversion has already been performed before proceeding, optimizing resource usage.
