# Remember

## AWS App Deployment

Create S3 bucket and upload a `quotes.json` file

Setup `TO_ADDRESS` and `SOURCE_ADDRESS` email as Identities in Amazon Simple Email Service 

Deploy the service using AWS Serverless Application Model (SAM)

```
sam build
sam deploy --guided
```

You can delete the app using: `aws cloudformation delete-stack --stack-name remember`

### Example quotes.json

```
{
    "count": 1,
    "quotes": [
        {
            "text": "",
            "count": 0
        }
    ]
}
```