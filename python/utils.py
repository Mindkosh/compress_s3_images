from datetime import datetime

convert_to_bool = lambda x : True if str(x).lower()=="true" else False

def cli_log( error_type="INFO", msg="" ):
    print( error_type + " : " + str( datetime.now() ) + " - " + msg )

def parse_s3_location( s3_location ):
    if s3_location[:5] == "s3://":
        loc = s3_location[5:]
        parts = loc.split("/")
        return (parts[0], "/".join(parts[1:]))
    return s3_location