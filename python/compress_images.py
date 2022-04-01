import os
import boto3
import json
from io import BytesIO
from PIL import Image as pil, ImageFile
from utils import convert_to_bool, cli_log, parse_s3_location

# Needed to load truncated image withot endfile
ImageFile.LOAD_TRUNCATED_IMAGES = True

batch_job_key = os.getenv( "BATCH_JOB_KEY", None )
runtime_region = os.getenv( "AWS_REGION", "us-east-2" )

bucket = os.getenv( "IN_BUCKET", None )
json_key = os.getenv( "JSON_LOCATION", None )

out_bucket = os.getenv( "OUT_BUCKET", None )
out_key = os.getenv( "OUT_KEY", None )

aws_key = os.getenv( "AWS_ACCESS_KEY_ID", None )
aws_secret_key = os.getenv( "AWS_SECRET_ACCESS_KEY", None )

# If filenames end with _left, _right or _front, this will save the compressed 
# files in their respective directories
divide_camera_wise = convert_to_bool(os.getenv( "DIVIDE_CAMERA_WISE", "false" ))

def main():
    if batch_job_key is None:
        cli_log("ERROR", "Could not find Batch job key")
        return 0

    if bucket is None:
        cli_log("ERROR", "Could not find file list bucket name")
        return 0

    if json_key is None:
        cli_log("ERROR", "Could not find file list location")
        return 0

    if out_bucket is None:
        cli_log("ERROR", "Could not find output bucket")
        return 0

    if out_key is None:
        cli_log("ERROR", "Could not find output location")
        return 0

    session = boto3.Session(
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret_key,
    )

    s3_resource = session.resource('s3', runtime_region)

    cli_log("INFO", "Reading file-list")

    obj = s3_resource.Object(bucket, json_key)
    data = obj.get()['Body'].read()

    compressed = 0

    try:
        json_obj = json.loads( data )
        cli_log("INFO", "Parsed filelist")

        if batch_job_key not in json_obj:
            cli_log("ERROR", "Could not find key - " + batch_job_key + " in the filelist")
            return 0
        else:
            files_to_compress = json_obj[batch_job_key]
            for filekey in files_to_compress:
                parse_s3_key = parse_s3_location(filekey)
                cli_log("INFO", filekey)

                try:
                    obj = s3_resource.Object(parse_s3_key[0], parse_s3_key[1])
                    input_file = BytesIO(obj.get()['Body'].read())

                    img = pil.open(input_file)
                    tmp = BytesIO()
                    img.save(tmp, 'JPEG', quality=70)
                    tmp.seek(0)
                    output_data = tmp.getvalue()

                    content_type = 'image/jpeg'
                    content_length = len(output_data)

                    image_filename = os.path.basename(filekey)

                    if divide_camera_wise:
                        camera = image_filename.split("_")[-1].split(".")[0]
                        if camera == "left":
                            outfile_key = os.path.join( out_key, "left", image_filename.replace(".png", ".jpeg") )
                        elif camera == "right":
                            outfile_key = os.path.join( out_key, "right", image_filename.replace(".png", ".jpeg") )
                        elif camera == "front":
                            outfile_key = os.path.join( out_key, "front", image_filename.replace(".png", ".jpeg") )
                        else:
                            outfile_key = os.path.join( out_key, "others", image_filename.replace(".png", ".jpeg") )
                    else:
                        outfile_key = os.path.join( out_key, image_filename.replace(".png", ".jpeg") )

                    obj_out = s3_resource.Object( out_bucket, outfile_key )
                    obj_out.put(Body=output_data, ContentLength=content_length, ContentType=content_type)
                    
                    tmp.close()
                    input_file.close()
                    compressed += 1

                except Exception as exception_obj:
                    cli_log("ERROR CONVERTING FILE")
                    print(exception_obj)
                    continue
                

        cli_log("INFO", "Compressed " + str(compressed) + "/" + str( len(files_to_compress) ) + " files.")
        return 1

    except Exception as exception_obj:
        cli_log("INFO", "Compressed " + str(compressed) + "/" + str( len(files_to_compress) ) + " files.")
        cli_log("ERROR")
        print(exception_obj)
        return 0


if __name__ == "__main__":
    main()