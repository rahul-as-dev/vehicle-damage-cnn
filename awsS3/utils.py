import boto3


class AwsHandler:
    aws_access_key_id = None
    aws_secret_access_key = None

    def __init__(self, aws_access_key_id, aws_secret_access_key) -> None:
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key

    def upload_image_to_s3(self, file, bucket_name='autoinspector', object_name='image/image.jpg'):
        # Pass your AWS credentials explicitly
        s3_client = boto3.client(
            's3',
            aws_access_key_id= self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key
        )
        try:
            response = s3_client.put_object(
                Bucket=bucket_name,
                Key=object_name,
                Body=file,
                ACL='bucket-owner-full-control'
            )
            return response
        except Exception as e:
            print(f"Upload failed: {e}")

    def get_image_from_s3(self, bucket_name='autoinspector', image_key='images/image.jpg',
                          ETag='"b226a838d781b447ddfbe8c10b380834"'):
        s3_client = boto3.client(
            's3',
            self.aws_access_key_id,
            self.aws_secret_access_key
        )
        try:
            metadata = {
                'ETag': ETag,
            }
            # Get the image object from S3 using the ETag and other metadata
            response = s3_client.get_object(
                Bucket=bucket_name,
                Key=image_key,
                IfMatch=metadata['ETag'],
            )
            # Get the image data
            image_data = response['Body'].read()

            # Determine the content type based on the image file extension
            content_type = response['ContentType']

            # Create the HTTP response with the image data and content type
            print(response)
            # return HttpResponse(image_data, content_type=content_type)
        except Exception as e:
            # return HttpResponse("Image not found", status=404)
            pass
