**Used when running lambda.**

This role should allow permissions to AWS S3, AWS Cloudwatch (for logging) and AWS Batch. You can mention the specific resources on S3 and Batch that you need access to.

The following policies will the job for you. However they are way to open and *should not be used in production setting*

AmazonS3FullAccess
CloudWatchFullAccess
AWSBatchFullAccess