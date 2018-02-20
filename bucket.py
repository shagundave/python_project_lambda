# Create bucket
import boto3
#s3 = boto3.resource('s3')
#response = s3.create_bucket(Bucket='testlambda-abc')
#print(response.name)

# Bucket List
s3 = boto3.resource('s3')
#for bucket in s3.buckets.all():
#        print(bucket.name)

# Delete Bucket
#db = s3.Bucket('testlambda-abc')
#dlt = db.delete()
#print(dlt)

## Put object in Bucket
#a = s3.Bucket('testlambda-xyz').upload_file('/tmp/hello.txt', 'hello.txt')
#print(a)
# check object
your_bucket = s3.Bucket('testlambda-xyz')
for s3_file in your_bucket.objects.all():
    print(s3_file.key)