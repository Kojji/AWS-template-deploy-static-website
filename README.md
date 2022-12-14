# AWS CodeCommit replication to S3 website hosting

This pattern implements the solution outlined on my Medium article ["Creating an AWS template to deploy my online Portfolio Pt.1"]().

Important: this application uses a variety of AWS resources and there may be costs associated with these services after the Free Tier usage - please see the [AWS Pricing page](https://aws.amazon.com/pricing/) for details. You are responsible for any AWS costs incurred. No warranty is implied in the use of this template.

## Requirements

* [Create an AWS account](https://portal.aws.amazon.com/gp/aws/developer/registration/index.html) if you do not already have one and log in. The IAM user that you use must have sufficient permissions to make necessary AWS service calls and manage AWS resources.
* [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) installed and configured
* [Git Installed](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* [AWS Serverless Application Model](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) (AWS SAM) installed

## Deployment Instructions

1. Create a new directory, navigate to that directory in a terminal and clone this GitHub repository:
    ``` 
    git clone https://github.com/Kojji/AWS-template-deploy-static-website
    ```
1. Change directory to the pattern directory:
    ```
    cd AWS-template-deploy-static-website
    ```
1. From the command line, use AWS SAM to deploy the AWS resources for the pattern as specified in the template.yml file:
    ```
    sam deploy --capabilities CAPABILITY_NAMED_IAM CAPABILITY_AUTO_EXPAND --template template.yaml
    ```
1. During the prompts:
    * Enter a stack name
    * Enter the desired AWS Region
    * Enter the page domain (it just impacts on some of the resources naming)
    * Allow SAM CLI to create IAM roles with the required permissions.

    Once you have run `sam deploy --guided` mode once and saved arguments to a configuration file (samconfig.toml), you can use `sam deploy` in future to use these defaults.

1. Note the outputs from the SAM deployment process. These contain information S3 bucket where your build will be stored, the CodeCommit repository which the builds will be pushed into and the cloudfront distribution that delivers the bucket content.

2. For this template, to use a custom domain, you have to manually acquire the domain and create a certificate on "AWS Certificate Manager" and link it to the generated Cloudfront Distribution. 

## How it works

When the content of the CodeCommit repository is modified (for example, by a git push command), it notifies EventBridge of the repository change. EventBridge then invokes AWS CodeBuild with the CodeCommit repository information. CodeBuild cleans the bucket and then clones the entire CodeCommit repository and uploads the it to an S3 bucket which is fronted by a CloudFront distribution.
During deployment, the pattern uses a Lambda function and a CloudFormation Custom Resource to create the CodeBuild's buildspec.yml template and stores into a secondary bucket.

## Testing

1. Use the CodeCommit repository created by this template
2. Update the repository content
3. Verify that the files are replicated on the S3 bucket that hosts the page

Important: For the scope of this project, there isn't a conditional control over which branch will be replicated. So, for any branch of the repository that is updated it's contents will replace the old files inside the S3 bucket for the builds.