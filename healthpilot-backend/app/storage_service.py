import os
from typing import Optional, Dict, Any
from supabase import create_client, Client
import uuid
from datetime import datetime

class StorageService:
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
        
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
        self.bucket_name = "uploads"

    def upload_file(self, file_content: bytes, filename: str, user_id: str) -> Dict[str, Any]:
        """
        Upload a file to Supabase Storage
        """
        try:
            # Create unique file path
            file_id = str(uuid.uuid4())
            file_extension = os.path.splitext(filename)[1]
            storage_path = f"lab_reports/{user_id}/{file_id}{file_extension}"
            
            # Upload to Supabase Storage
            result = self.client.storage.from_(self.bucket_name).upload(
                path=storage_path,
                file=file_content,
                file_options={"content-type": "application/octet-stream"}
            )
            
            if result:
                # Get public URL
                public_url = self.client.storage.from_(self.bucket_name).get_public_url(storage_path)
                
                return {
                    "success": True,
                    "file_id": file_id,
                    "original_filename": filename,
                    "storage_path": storage_path,
                    "public_url": public_url,
                    "file_size": len(file_content)
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to upload file"
                }
                
        except Exception as e:
            print(f"Storage upload error: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def download_file(self, storage_path: str) -> Optional[bytes]:
        """
        Download a file from Supabase Storage
        """
        try:
            result = self.client.storage.from_(self.bucket_name).download(storage_path)
            return result
        except Exception as e:
            print(f"Storage download error: {e}")
            return None

    def delete_file(self, storage_path: str) -> bool:
        """
        Delete a file from Supabase Storage
        """
        try:
            result = self.client.storage.from_(self.bucket_name).remove([storage_path])
            return True
        except Exception as e:
            print(f"Storage delete error: {e}")
            return False

    def get_file_url(self, storage_path: str) -> Optional[str]:
        """
        Get public URL for a file
        """
        try:
            return self.client.storage.from_(self.bucket_name).get_public_url(storage_path)
        except Exception as e:
            print(f"Storage URL error: {e}")
            return None

    def list_user_files(self, user_id: str) -> list:
        """
        List all files for a user
        """
        try:
            # List files in user's directory
            files = self.client.storage.from_(self.bucket_name).list(
                path=f"lab_reports/{user_id}/"
            )
            return files
        except Exception as e:
            print(f"Storage list error: {e}")
            return []

    def create_bucket_if_not_exists(self):
        """
        Create the uploads bucket if it doesn't exist
        """
        try:
            # Try to list the bucket to see if it exists
            self.client.storage.list_buckets()
        except Exception:
            # Bucket doesn't exist, create it
            try:
                self.client.storage.create_bucket(
                    name=self.bucket_name,
                    public=True
                )
                print(f"Created bucket: {self.bucket_name}")
            except Exception as e:
                print(f"Error creating bucket: {e}")

    def setup_storage_policies(self):
        """
        Set up Row Level Security policies for storage
        """
        # This would typically be done in Supabase dashboard
        # or via SQL migrations
        policies = [
            """
            -- Allow users to upload files to their own directory
            CREATE POLICY "Users can upload to own directory" ON storage.objects
            FOR INSERT WITH CHECK (bucket_id = 'uploads' AND auth.uid()::text = (storage.foldername(name))[1]);
            """,
            """
            -- Allow users to view their own files
            CREATE POLICY "Users can view own files" ON storage.objects
            FOR SELECT USING (bucket_id = 'uploads' AND auth.uid()::text = (storage.foldername(name))[1]);
            """,
            """
            -- Allow users to delete their own files
            CREATE POLICY "Users can delete own files" ON storage.objects
            FOR DELETE USING (bucket_id = 'uploads' AND auth.uid()::text = (storage.foldername(name))[1]);
            """
        ]
        
        # Note: These policies should be applied in Supabase dashboard
        # or via SQL migrations, not in Python code
        print("Storage policies should be configured in Supabase dashboard") 