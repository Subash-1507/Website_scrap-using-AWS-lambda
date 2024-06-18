import os
import requests
from bs4 import BeautifulSoup
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from datetime import datetime

def lambda_handler(event, context):
    # URL of the website you want to scrape
    url = "https://www.karunya.edu"

    # Send a GET request to the website
    response = requests.get(url)

    # If the GET request is successful, the status code will be 200
    if response.status_code == 200:
        # Get the content of the response
        webpage_content = response.content

        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(webpage_content, "html.parser")

        # Extract all text from the webpage
        data = soup.get_text()

        # Debugging: Print a portion of the extracted data to verify it
        print("Extracted Data: ", data[:500])  # Print first 500 characters

        if data:
            # Specify the AWS S3 Bucket
            bucket_name = 'karunya-bucket'

            # Create a session using your AWS credentials (use IAM roles or environment variables)
            s3 = boto3.client('s3')

            # Prepare the data for S3
            file_content = data.encode('utf-8')
            
            # Generate a dynamic file name with a timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            file_name = f'karunya_data_{timestamp}.txt'

            try:
                s3.put_object(Body=file_content, Bucket=bucket_name, Key=file_name)
                print("Upload Successful. File name: ", file_name)
                return True
            except FileNotFoundError:
                print("The file was not found")
                return False
            except NoCredentialsError:
                print("Credentials not available")
                return False
            except ClientError as e:
                print(f"Client error: {e}")
                return False
        else:
            print("Data not found on the webpage")
            return False
    else:
        print(f"Failed to retrieve the webpage, status code: {response.status_code}")
        return False
