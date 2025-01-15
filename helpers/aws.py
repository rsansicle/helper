import boto3
import dotenv
from io import StringIO

dotenv.load_dotenv()

class Operations:
    def __init__(self,
                 s3 = True,
                 secret_manager = True,
                 region = "us-east-1"):
        try:
            self.s3 = boto3.client('s3') if s3 else None
            self.secret_manager = boto3.client('secretsmanager', region_name = region) if secret_manager else None
        except Exception as e:
            raise(f"Error with client setups: {e}")

    def send_to_s3(self, filename, upload_bucket, upload_key):
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
            return message

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
            return message

    def get_secret(self, secret_key):
        try:
            response = self.secret_manager.get_secret_value(SecretId= secret_key)
            secret_dict = eval(response['SecretString'])
            secrets = list(secret_dict.values())[0]

            message = {
                'status': True,
                'value': secrets,
                'message': f"Secret value for {secret_key} extracted successfully"
            }
            return message

        except Exception as e:
            message = {
                'status': False,
                'value': None,
                'message': f"Unable to extract secret for {secret_key} with exception:\n{str(e)}"
            }

            return message

    def df_to_s3(self, df, bucket: str, key:str, file_name):
        csv_buffer = StringIO()
        df.to_csv(csv_buffer)

        s3 = boto3.resource('s3')
        object = s3.Object(bucket, key + file_name)

        object.put(Body=csv_buffer.getvalue())
