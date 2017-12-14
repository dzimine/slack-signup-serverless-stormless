### Create a project, add first action

### Add a second action 

Second, I'm adding [Action Campaign](https://exchange.stackstorm.org/#activecampaign) action. 
Same thing: start with finding a new action, inspect the action, and add a section to the `serverless.yml`. 

```
sls stackstorm info --action activecampaign.contact_add
activecampaign.contact_add .... Add new contact.
Parameters
  api_action [string]  ........ contact_add
  api_key [string]  ........... Your API key
  api_output [string]  ........ xml, json, or serialize (default is XML)
  email [string] (required) ... Email of the new contact. Example: 'test@example.com'
  field [object]  ............. 'value' (You can also use the personalization tag to specify which field you want updated)
  first_name [string]  ........ First name of the contact. Example: 'FirstName'
  form [string]  .............. Optional subscription Form ID, to inherit those redirection settings. Example: 1001. This will allow you to mimic adding the contact through a subscription form, where you can take advantage of the redirection settings.
  instantresponders [object]  . Use only if status = 1. Whether or not to set "send instant responders." Examples: 1 = yes, 0 = no.
  ip4 [string]  ............... IP address of the contact. Example: '127.0.0.1' If not supplied, it will default to '127.0.0.1'
  last_name [string]  ......... Last name of the contact. Example: 'LastName'
  lastmessage [object]  ....... Whether or not to set "send the last broadcast campaign." Examples: 1 = yes, 0 = no.
  noresponders [object]  ...... Whether or not to set "do not send any future responders." Examples: 1 = yes, 0 = no.
  orgname [string]  ........... Organization name (if doesn't exist, this will create a new organization) - MUST HAVE CRM FEATURE FOR THIS.
  p [object]  ................. Assign to lists. List ID goes in brackets, as well as the value.
  phone [string]  ............. Phone number of the contact. Example: '+1 312 201 0300'
  sdate [object]  ............. Subscribe date for particular list - leave out to use current date/time. Example: '2009-12-07 06:00:00'
  status [object]  ............ The status for each list the contact is added to. Examples: 1 = active, 2 = unsubscribed
  tags [string]  .............. Tags for this contact (comma-separated). Example: "tag1, tag2, etc"
Config
  api_key [string] (required) . ActiveCampaign API Key.
  url [string] (required) ..... ActiveCampaign Account URL
  webhook [object]  ........... Webhook sensor specific settings.
```

With that, a function will look like this in `serverless.yml`. While with this, lets limit memory use as it's just one tiny call.

```yaml:
  RecordAC:
    memorySize: 256
    stackstorm:
      action: activecampaign.contact_add
      input:
        email: "{{ input.body.email }}"
        first_name: "{{ input.body.first_name }}"
        last_name: "{{ input.body.last_name }}"
      config: ${file(env.yml):activecampaign}
```  




This time I don't bother to expose it to AWS API Gateway - we can perfectly test it with `sls`. Ah, while with that I've removed the extra `body` key from all the functions. From now on, the event is:
```
{
    "first_name": "Santa", 
    "last_name": "Clause", 
    "email": "santa@mad.russian.xmas.com"
}
```


```
# Build the bundle
sls package

# Test locally 
sls stackstorm docker run --function RecordAC --passthrough --verbose --data '{"email":"santa@mad.russian.xmas.com", "first_name":"Santa", "last_name": "Clause"}'

# Deploy to AWS 
sls deploy



# Test: call Lambda on AWS with sls 
sls invoke --function RecordAC --logs --data '{"email":"santa@mad.russian.xmas.com", "first_name":"Santa", "last_name": "Clause"}'

# Check the logs
sls logs --function RecordAC


```

and I checked: Santa Clause appeared in ActiveCampaign indeed, and how do I know it's our Lambda? because I no longer believe Santa is real enough to subscribe to StackStorm community without our help. [^todo-ac]

Let's add the final action, RecordDB, that writes contact info into DynamoDB table. AWS pack on StackStorm Exchange heavily used and well maintained. I could have used `aws.dynamodb_put_item` action from there, but decided to keep it native: it's 15 lines of code, and no build as Boto library is already in AWS Lambda environment. Besides it's good to see both kinds of functions side by side in `serverless.com`.

Deploy, invoke, logs. Rinse repeat.

```
sls deploy 
...
sls invoke --function RecordDB --logs --data '{"email":"santa@mad.russian.xmas.com", "first_name":"Santa", "last_name": "Clause"}'
...

sls logs --function RecordDB. 
```

NOTE: I wanted to make a tiny change to RecordDB. As deployment takes a while, I wanted to use the new cool Cloud9 editor and hack right on the cloud... But I couldn't: deployment package is too big. REALLY?RecordDB size is the same as for other actions. On second though, it's right: one serverless service - one deployment package (you can check it in `./.serverless/SERVICE_NAME.zip`). So either native or Exchange, actions are bundled together and all dependencies of all actions got deployed 


### Coming up: Add a workflow

### Conclusion

# TODO's and notes
* [NOTE] I like how data flow is visible in `serverless.yml`. In typical lambda, it's hidden inside lambda handlers and it's not obvious what goes in and what comes out. Here it's a clear view. 

* [FEATURE] StackStorm Exchange improvements: 1) see actions on pack 2) see open PRs across exchange + PRs per pack ? 



[^todo-ac]: [BUG] ActiveCampaign.contact_add shall not throw exception if the user already exist, but return the 200 and message just like AC API does. 



[todo-change-AC-action]: "TODO d "
