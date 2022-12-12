const AWS = require('aws-sdk');
AWS.config.region = process.env.AWS_REGION;
const Git = require("nodegit");
const bucketName = process.env.DestinationBucketName;
const coveredBranch = process.env.CoveredBranch;
const cloneRepoUrl = process.env.CloneRepoUrl

// The Lambda handler
exports.handler = async (event) => {
  
  console.log(bucketName)
  console.log(coveredBranch)
  console.log(cloneRepoUrl)
  // Git.Clone("https://github.com/nodegit/nodegit", "nodegit").then(function(repository) {
  //   // Work with the repository object here.
  // });
  // Params object for SNS
  const params = {
    Message: `Message at ${Date()}`,
    Subject: 'New message from publisher',
    DestinationBucketName: process.env.DestinationBucketName
  }

  console.log(event)
  return 
}