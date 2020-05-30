import time
import logging
import os
import sys
from chalice import Chalice, Rate
from certbot.main import main as runner
import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


app = Chalice(app_name='CertMan')

_CERTMAN_DIR = '/tmp/certman'


def renew(email, domain):
    '''Obtain or renew a certificate

    :param email
    :param domain
    '''
    # https://certbot.eff.org/docs/using.html#certbot-command-line-options
    return runner([
        # Run without ever asking for user input
        '-n',
        # Agree to the ACME server's Subscriber Agreement
        '--agree-tos',
        # Obtain or renew a certificate, but do not install it
        'certonly',
        # config
        '--config-dir', _CERTMAN_DIR,
        '--work-dir', _CERTMAN_DIR,
        '--logs-dir', _CERTMAN_DIR,
        '--server', 'https://acme-v02.api.letsencrypt.org/directory',
        # Email address for important account notifications
        '-m', email,
        # https://certbot-dns-route53.readthedocs.io/en/stable/
        '--preferred-challenges', 'dns-01',
        '--dns-route53',
        '--dns-route53-propagation-seconds', '30',
        '-d', domain,

    ])


def flush(region, bucket):
    """flush live cert to s3

    :param region
    :param bucket

        - live
          - $domain
            - cert.pem
            - chain.pem
            - fullchain.pem
            - privkey.pem
    """

    s3 = boto3.client('s3', region_name=region)
    cert_home = os.path.join(_CERTMAN_DIR, 'live')
    for dirpath, dirnames, filenames in os.walk(cert_home):
        for filename in filenames:
            abspath = os.path.join(dirpath, filename)
            s3_key = os.path.relpath(abspath, cert_home)
            logger.info("Flushing From: %s To: s3://%s/%s" %
                        (abspath, bucket, s3_key))
            s3.upload_file(abspath, bucket, s3_key)


@app.schedule(Rate(30, unit=Rate.DAYS))
def run(event):
    since = time.time()
    logger.info("CertMan Working")

    try:
        email = os.getenv("EMAIL")
        domain = os.getenv("DOMAIN")
        s3_bucket = os.getenv("BUCKET")
        region = os.getenv("REGION")
        assert email
        assert domain
        assert s3_bucket
        assert region
        renew(email, domain)
        flush(region, s3_bucket)
        logger.info("Job Done. Took %2f" % (time.time() - since,))
    finally:
        pass
