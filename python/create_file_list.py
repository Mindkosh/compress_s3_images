import os
import json
import argparse

def main():
    parser = argparse.ArgumentParser( description='Create a json file with input images divided into specified number of batches' )

    # The input file should be a line separated list of filenames. 
    # Each filename should be in this format: s3://<bucket-name>/<location>
    # See test_files/filelist_template.json for an example of an output json file.

    parser.add_argument("--file_list", required=True, action='store')
    parser.add_argument("--batches", required=True, action='store')
    parser.add_argument("--outfile", required=False, action='store')
    args = parser.parse_args()
    
    file_list = args.file_list
    batches = int(args.batches)
    outfile = args.outfile

    all_lines = open(file_list).readlines()
    all_data = [ i.strip().split(" ")[-1].strip() for i in all_lines ]
    
    print("Segmenting " + str(len(all_data)) + " images into " + str(batches) + " batches.")

    segment_size = len(all_data)//batches

    out_json = dict()
    for i in range(batches):
        out_json["batch_" + str(i+1)] = []
    
    for index, i in enumerate(all_data):
        if (index//segment_size) == batches:
            out_json["batch_" + str( batches )].append( i )    
        else:
            out_json["batch_" + str((index//segment_size)+1)].append( i )
    
    if not outfile:
        outfile_name = "segmented_" + os.path.splitext( os.path.basename( file_list ) )[0] + ".json"
    else:
        outfile_name = outfile

    json.dump( out_json, open( outfile_name, "w" ) )
    print("Done.")


if __name__ == "__main__":
    main()