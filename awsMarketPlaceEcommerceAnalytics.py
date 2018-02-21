## AWS-MarketPlace-EcommerceAnalytics-Start-Support-Data
# 
import datetime 
import boto3
def lambda_handler(event, context):
    client = boto3.client('marketplacecommerceanalytics')

    response = client.start_support_data_export(dataSetType='test_customer_support_contacts_data',
        fromDate=datetime.datetime.now() - datetime.timedelta(days=7),
        roleNameArn='arn:aws:iam::xxxxxxxxx:role/MarketplaceCommerceAnalyticsRole',
        destinationS3BucketName='cloud-ami-support',
        destinationS3Prefix='cloud-ami-customer-list',
        snsTopicArn='arn:aws:sns:us-west-2:xxxxxxxxx:cloud-ami-support-sns'
        ) 
