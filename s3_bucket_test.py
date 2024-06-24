import boto3
import os

# Constants
BUCKET_NAME = 'org-report-storage-bucket'
LOCAL_FILE_TO_UPLOAD = 'test_upload.txt'  # Local file to be created and uploaded
S3_KEY_FOR_UPLOAD = 'test_upload.txt'
LOCAL_DOWNLOAD_FILE = 'downloaded_file.txt'

# Create content for the new file
file_content = "This is a test file created for upload to S3."

# Create a new local file and write content to it
with open(LOCAL_FILE_TO_UPLOAD, 'w') as local_file:
    local_file.write(file_content)

# Create a connection to S3
s3 = boto3.resource('s3')

try:
    # Upload the local file to S3
    with open(LOCAL_FILE_TO_UPLOAD, 'rb') as data:
        bucket = s3.Bucket(BUCKET_NAME)
        bucket.put_object(Key=S3_KEY_FOR_UPLOAD, Body=data)

    print("File uploaded successfully!")

    # Download the file from S3
    bucket.download_file(S3_KEY_FOR_UPLOAD, LOCAL_DOWNLOAD_FILE)

    print("File downloaded successfully!")

    # Read the downloaded file and print its content
    with open(LOCAL_DOWNLOAD_FILE, 'r') as downloaded_file:
        print("Content of the downloaded file:")
        print(downloaded_file.read())

finally:
    # Clean up: delete the local files
    if os.path.exists(LOCAL_FILE_TO_UPLOAD):
        os.remove(LOCAL_FILE_TO_UPLOAD)
    if os.path.exists(LOCAL_DOWNLOAD_FILE):
        os.remove(LOCAL_DOWNLOAD_FILE)

    print("Local files deleted successfully!")
