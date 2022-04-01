import json
import boto3

def lambda_handler(event, context):
    session = boto3.session.Session()
    client = session.client('batch')
    number_of_batches = 3

    for i in range( number_of_batches ):
        job1 = client.submit_job(
            jobName="batch_"+ str(i+1) + "_job",
            
            jobQueue="job_queue_name",
            
            jobDefinition='job_definition_name',
            
            containerOverrides={
                'environment': [
                    {
                        'name': "BATCH_JOB_KEY",
                        'value': "batch_"+ str(i+1)
                    },
                    {
                        'name': "AWS_REGION",
                        'value': "s3 region where the file-list is located"
                    },
                    {
                        "name": "IN_BUCKET",
                        'value': "bucket where file-list is saved"
                    },
                    {
                        "name": "JSON_LOCATION",
                        'value': "location of file-list"
                    },
                    {
                        "name": "OUT_BUCKET",
                        'value': "bucket where compressed images will be saved"
                    },
                    {
                        "name": "OUT_KEY",
                        'value': "location where compressed images will be saved"
                    },
                    {
                        "name": "DIVIDE_CAMERA_WISE",
                        'value': "false"
                    },
                ]
            }
        )
    return {
        'statusCode': 200,
        'body': json.dumps("Started Job: {}".format(job1['jobName']))
    }
