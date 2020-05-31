# CertMan

Automatic Renew Cert Without Server.

## How it Works

Cloudwatch scheduled event Call A lamada Function（Do Cert Request [Let's Encrypt](https://letsencrypt.org/) Every 30 days, All Cert files flush to S3 bucket.

## ENV

- `REGION` aws region
- `BUCKET` s3 bucket as the cert storage
- `EMAIL` certbot email address for important account notifications
- `DOMAIN` Domain names to apply
  
## Configuration

- [IAM Policy Template](man/.chalice/policy-dev.json)

## Deploy

- set up aws credentials
- install [pipenv](https://github.com/pypa/pipenv#installation)
- `pipenv install`
- `cd man`
- `pipenv run chalice deploy --no-autogen-policy`

## Powered By

- chalice
- aws lamada
- aws s3
- aws cloudwatch
- certbot
- certbot-dns-*
  - route53
