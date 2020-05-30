# CertMan

Automatic Renew Cert Without Server.

## ENV

- `REGION` aws region default: us-west-2
- `BUCKET` s3 bucket as the cert storage
- `EMAIL` certbot email address for important account notifications
- `DOMAIN` Domain names to apply
  
## Configuration

- [IAM Policy Template](man/.chalice/policy-dev.json)

## Deploy

- ```chalice deploy --no-autogen-policy```

## Powered By

- chalice
- aws lamada
- aws s3
- certbot
- certbot-dns-*
  - route53
