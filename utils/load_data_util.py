import boto3
import botocore
import json
import pandas as pd
import requests
import random
import os
from pathlib import Path

BUCKET_NAME = "safe-ucosp-2017"

pd.set_option('display.max_columns', 500)
pd.set_option('display.expand_frame_repr', False)
s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)

this_files_directory = os.path.dirname(os.path.realpath(__file__))
project_root_directory = os.path.join(this_files_directory, "..")
cache_file_directory = os.path.join(project_root_directory, "cache")
if not os.path.exists(cache_file_directory):
    os.makedirs(cache_file_directory)

def load_data(number_of_files, to_output_csv = True, cache_s3_data = False):
    """Load the files from the beginning of the bucket
    Keyword arguments:
    number_of_files -- number of files to load
    to_output_csv -- boolean to save the result of the data into a csv file called result.csv (default True)
    cache_s3_data -- boolean to cache each file once downloaded in a json file to speed up future data loads. (default False)
    """
    file_number = 0
    frames = []
    
    #Take the first number_of_files and transform them into dataframes
    for bucket_data_object in bucket.objects.limit(number_of_files):
        file_number += 1
        data_frame = load_data_to_dataframe(bucket_data_object, file_number, cache_s3_data)
        frames.append(data_frame)
    
    #Concat DataFrames generated from each file into a large DataFrame
    result = pd.concat(frames)
    
    #Output the results to a csv if desired
    if (to_output_csv):
        result.to_csv('result.csv', header=True, index=False, encoding='utf-8')        
    return result


def transform_into_dataframe(data, file_number):
    """Process the data, read it into a pandas DataFrame and add a column for file number
    Keyword arguments:
    data -- the string containing the file data
    file_number -- the file number the data came from
    """
    frame = pd.read_json(data)
    frame['file_number'] = file_number
    return frame


def process_string(data):
    return "[" + data[1:-1] + "]"


def create_file_index():
    """Function used to create the file index file"""
    count = 0
    with open("file_index.json", "a+") as f:
        for key in bucket.objects.all():
            count += 1
            f.write(key.key + "\n")
            if (count%1000 == 0):
                print(count)


def validate_file_fetch():
    """Function used to validate the file index has unique entries"""
    with open("file_index.json") as f:
        index_list = f.readlines()
        index_set = set(index_list)

    return len(index_list) == len(index_set)


def fetch_file(file_url, file_name, mode):
    """Fetch file from base_url and store it in the project root directory.
    Keyword arguments:
    file_url -- url of where the file is
    file_name -- name of the file to be saved as
    mode -- mode of the file to open it in (for example: wb+)     
    """
    file = requests.get(file_url + file_name)

    file_path = os.path.join(project_root_directory, file_name)
    with open(file_path, mode) as f:
        f.write(file.content)


def load_index_file():
    """Load the file containing all indexes of the bucket and return it as an array of indexes - will download the index file if it's not in local storage"""
    file_name = "file_index.txt"
    file_path = os.path.join(project_root_directory, file_name)
    if not os.path.isfile(file_path):
        fetch_file("http://www.arewedatayet.com/", file_name, 'wb+')

    with open(file_path, "r") as f:
        lines = f.readlines()
    return lines


def load_random_data(number_of_files, to_output_csv = True, seed = None, cache_s3_data = False):
    """Load random files from the bucket
    Keyword arguments:
    number_of_files -- number of files to load
    to_output_csv -- boolean to save the result of the data into a csv file called result.csv (default True)
    seed -- seed for generating random samples (default None)
    cache_s3_data -- boolean to cache each file once downloaded in a json file to speed up future data loads. (default False) 
    """

    frames = []
    file_number = 0
    
    lines = load_index_file()
    
    random.seed(seed)
    #Get x number of random files
    samples = random.sample(lines, number_of_files)
    
    #Take the first number_of_files and transform them into dataframes
    for sample in samples:
        sample = sample.strip()
        file_number += 1

        bucket_data_object = s3.ObjectSummary(BUCKET_NAME, sample)
        data_frame = load_data_to_dataframe(bucket_data_object, file_number, cache_s3_data)
        frames.append(data_frame)
        
    #Concat DataFrames generated from each file into a large DataFrame
    result = pd.concat(frames)
    
    #Output the results to a csv if desired
    if (to_output_csv):
        result.to_csv('result.csv', header=True, index=False, encoding='utf-8')        
    return result


def get_json_data(bucket_data_object, cache_s3_data):
    """Get the json data from either the given s3 bucket or the cache. 
    Keyword arguments:
    bucket_data_object -- a boto3 ObjectSummary class that is connected to the json data we want to load
    cache_s3_data -- boolean which determines if we cache the downloaded data in a file in the cache directory
    """
    file_name = os.path.join(cache_file_directory, bucket_data_object.key)

    if os.path.isfile(file_name): # get data from file
        json_data = json.load(open(file_name))

        return json.dumps(json_data)
    else: # get data from S3
        bucket_json_data = bucket_data_object.get()

        # data is in a byte format so we must decode it to utf-8.
        json_data = bucket_json_data['Body'].read().decode("utf-8")
        json_data = process_string(json_data)

        if cache_s3_data:
            data_file = open(file_name, "w")

            # pretty print json data to file
            json_dump = json.dumps(json.loads(json_data), sort_keys=True, indent=2)
            data_file.write(json_dump)
            data_file.close()

        return json_data

def load_data_to_dataframe(bucket_data_object, file_number, cache_s3_data):
    """Download the file from the given bucket object and transform it into a DataFrame
    Keyword arguments:
    bucket_data_object -- a boto3 ObjectSummary class that is connected to the json data we want to load
    file_number -- file number to be attached to the DataFrame
    """
    
    data = get_json_data(bucket_data_object, cache_s3_data)

    return transform_into_dataframe(data, file_number)

def extract_column_json_to_list(series_to_be_processed):
    """Parse the selected column, transform the string into json, and throw the values into a list
    Keyword arguments:
    series_to_be_processed -- a pandas Series that contains strings in the form of json
    """
    return series_to_be_processed.map(lambda arguments: list(json.loads(arguments).values()) if isinstance(arguments, str) else [])

