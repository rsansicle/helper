import boto3
import dotenv

dotenv.load_dotenv()

class Operations:
    def __init__(self):
        try:
            self.s3 = boto3.client('s3')
            self.secret_manager = boto3.client('secretsmanager')
        except Exception as e:
            raise(f"Error with client setups: {e}")

    def send_to_s3(self, filename, client, upload_bucket, upload_key):
        """Will take a file from the root folder in which the function is being run from and upload to the respective S3 bucket (upload bucket + upload key)
        """
        upload_key = upload_key + filename

        try:
            self.s3.upload_file(filename, upload_bucket, upload_key)
            message = {
                'status': True,
                'message': f'{filename} uploaded into {upload_bucket} successfully'
            }

            return message

        except Exception as e:
            message = {
                'status': False,
                'message': f"{filename} upload unsuccessful with error:\n{str(e)}"
            }

    def pull_from_s3(self, bucket, key, filename):
        try:
            self.s3.download_file(bucket, key, filename)
            message = {
                'status': True,
                'message': f"{filename} downloaded from S3 successfully"
            }
            return message
        except Exception as e:
            message = {
                'status': False,
                'message': f"Unable to download {filename} from {bucket} with error:\n{str(e)}"
            }

    def get_secret(self, secret_key):
        try:
            response = self.secret_manager.get_secret_value(secret_key)
            secret_value = response['SecretString']

            message = {
                'status': True,
                'value': secret_value,
                'message': f"Secret value for {secret_key} extracted successfully"
            }
            return message

        except Exception as e:
            message = {
                'status': False,
                'value': None,
                'message': f"Unable to extract secret for {secret_key} with exception:\n{str(e)}"
            }