import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_ANON_KEY")

print(f"URL: {url}")
print(f"Key: {key[:20]}..." if key else "No key")

supabase = create_client(url, key)

# Test connection
try:
    response = supabase.table("profiles").select("*").limit(1).execute()
    print(f"Connection test: {response}")
except Exception as e:
    print(f"Connection error: {e}")
