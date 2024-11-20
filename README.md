# AWS Helpers

This is a simple package to handle various AWS operations across applications. 

Initializing the `Operations` class in `aws` handles assumes that the required IAM keys have been set as environment variables already. For additional controls you may decide what boto clients are enabled during the initializing process for `Operations`.

Presently only the following boto clients are set up:
- S3
- SecretManager
