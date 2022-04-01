This project helps you compress a large number of images in parallel using AWS Batch. The best way to get started is to follow
[this guide on Youtube](https://youtu.be/PhuV42va7Gs)

It combines the following key components

- **File list of images** - A json file that assigns a batch to each image. Each batch job on AWS only compresses images assigned to its own batch. 
An example file-list is given in test_files. Such a file should be uploaded to S3. If you have your images in a text file, you can run create_file_list.py to create the json json file.

Usage: python create_file_list.py <input_file_list>, <number of batches>, <outfile>
the input file should be a line separated list of filenames. Each filename should be in this format:  s3://<bucket-name>/<location>

- **Docker image used to compress the images**
This project uses AWS fargate to run the docker image that contains the compression code. The image can be pulled by running:
docker pull mindkosh/image_compressor:latest

- **compress_images.py** - This is the python code that reads the json file-list from S3, and compresses images. This is run from
within the Docker image.

- **lambda_function.py** - The batch jobs are created by this AWS lambda function.



**Testing the code locally**

Simply set the environment variables to proper values in docker-compose.yml and run docker-compose up from the root directory. All required images will automatically be pulled.


**Environment variables**

Set through AWS lambda function
BATCH_JOB_KEY - What batch number this job is
AWS_REGION - Region where the file-list lives on S3
IN_BUCKET - bucket where the file-list lives
JSON_LOCATION - location where the file-list lives
OUT_BUCKET - bucket where compressed images will be saved
OUT_KEY - location where compressed images will be saved
DIVIDE_CAMERA_WISE - whether to save images ending with "_left", "_right"  and "_front" in their own directories.

Set through AWS Job definition
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY

**Permission roles**
All permission roles required for running the AWS services can be found inside permission_templates.
