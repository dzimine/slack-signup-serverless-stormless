# StackStorm Community Signup Serverless Service: Stormless!


> This time, with [StackStorm Exchange](https://exchange.stackstorm.org) and [serverless-plugin-stackstorm](https://github.com/StackStorm/serverless-plugin-stackstorm)

This is a 'take three' on Community & Slack Signup with AWS Lambda and Serverless. 

* take 1: [Slack Signup with AWS Lambda](https://github.com/dzimine/slack-signup-lambda) was simple and functional, but working with AWS raw is such a pain in the butt...

* take 2: with [Serverless framework](https://serverless.com) and AWS StepFunctions. Happily done and had been running in production for [StackStorm community signup](https://stackstorm.com/community-signup). 

Now with [serverless-plugin-stackstorm](https://github.com/StackStorm/serverless-plugin-stackstorm) I can just use the actions from [StackStorm Exchange](https://exchange.stackstorm.org) instead of copying the code and creating 1001st "slack invite" Lambda. 

## WIP 

-[x] Part 1. "Slack invite service". 

```
# Explore the action parameters, write transformations in `serverless.yml`: 
#
sls stackstorm info --action slack.users.admin.invite

# Build and package (takes long 1st time but OK after)
#
sls package

# Test locally:
#
sls stackstorm docker run --function InviteSlack --passthrough --data '{"email":"dmitri@example.com", "first_name":"Dmitri"}'

# Deploy
#
sls deploy

# Test by running with sls. Note the `--raw` flag, it passes the payload as string. 
# 
sls invoke -l --function InviteSlack --raw --data '{"body":{"email":"dmitri@example.com", "first_name":"Dmitri"}}'

# Test with httpie: 
# Note that POST with JSON body will end up as a string under `body` key with most common `lambda-proxy` API-Gateway configuration. 
http --json POST  https://cxpqxgecbl.execute-api.us-east-1.amazonaws.com/dev/invite  email=test@example.com first_name=Markus

# Check the logs
sls logs --function InviteSlack
```