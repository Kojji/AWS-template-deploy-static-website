import boto3
import os
import cfnresponse

def handler(event, context):
  filename = "buildspec.yml"
  # buildspec.yml code inside the string
  string = """
version: 0.2
phases:
install:
  commands:
    - pip install git-remote-codecommit
build:
  commands:
    - git clone -b $REFERENCE_NAME codecommit::$REPO_REGION://$REPOSITORY_NAME
    - dt=$(date '+%d-%m-%Y-%H:%M:%S');
    - echo "$dt" 
    - zip -r $dt-$REPOSITORY_NAME-backup.zip $REPOSITORY_NAME
    - timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
    - aws s3 cp $dt-$REPOSITORY_NAME-backup.zip s3://$BUCKET/repositories/"""

  encoded_string = string.encode("utf-8")
  bucket_name = os.environ['bucket']
  s3_path = "codebuild-source/" + filename
  s3 = boto3.resource("s3")
  responseData = {}
  try:
      print("Creating buildspec file")
      s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)
      print("File created")
      responseData['Data'] = "File created"
      cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData)
  except Exception as e:
      print("There was an error creating the file")
      log_exception()
      responseData['Data'] = e
      cfnresponse.send(event, context, cfnresponse.FAILED, responseData)
  return