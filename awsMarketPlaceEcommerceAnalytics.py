## AWS-MarketPlace-EcommerceAnalytics-Start-Support-Data
# 
import datetime 
import boto3

client = boto3.client('marketplacecommerceanalytics')

response = client.start_support_data_export(dataSetType='test_customer_support_contacts_data',
    fromDate=datetime.datetime.now() - datetime.timedelta(days=7),
    roleNameArn='arn:aws:iam::212445883776:role/MarketplaceCommerceAnalyticsRole',
    destinationS3BucketName='intuzcloud-ami-support',
    destinationS3Prefix='intuzcloud-ami-customer',
    snsTopicArn='arn:aws:sns:us-west-2:212445883776:intuzcloud-ami-support-sns'
    ) 