import os

class S3_Sync:
    
    def sync_folder_to_s3(self,folder_path,aws_bucket_url):
        command=f"aws s3 sync {folder_path} {aws_bucket_url}"
        os.system(command=command)

    def sync_s3_to_folder(self,folder_path,aws_bucket_url):
        command=f"aws s3 sync {aws_bucket_url} {folder_path}"
        os.system(command=command)
