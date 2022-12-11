const AWS = require('aws-sdk')
AWS.config.region = process.env.AWS_REGION 

// The Lambda handler
exports.handler = async (event) => {
  // Params object for SNS
  const params = {
    Message: `Message at ${Date()}`,
    Subject: 'New message from publisher',
    DestinationBucketName: process.env.DestinationBucketName
  }

  console.log(event)
  return 
}