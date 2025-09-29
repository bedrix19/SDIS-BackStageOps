import logging
import boto3
from botocore.exceptions import ClientError


def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration={
                                        'LocationConstraint': region
                                    })
    except ClientError as e:
        logging.error(e)
        return False
    return True

if __name__ == "__main__":

    try:
        create_bucket('backstageops-bucket-try', region=None)
        print("Bucket creado correctamente")
    except Exception as e:
        print(f"No se pudo crear el bucket: {e}")