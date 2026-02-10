import os
from supabase import create_client, Client

# User Provided Credentials (Hackathon Mode)
# Project ID: twqskvagxyxexyyjptvk
SUPABASE_URL = "https://twqskvagxyxexyyjptvk.supabase.co"

# Using 'Anon Key' as provided by user. 
# This is the public key, so ensuring RLS policies are set correctly in SQL is important,
# but for the Hackathon demo, we will proceed with this.
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR3cXNrdmFneHl4ZXh5eWpwdHZrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA3MDkyMjEsImV4cCI6MjA4NjI4NTIyMX0.D_02DSZMRfKwGvkx9aqhM_4sdF1m6rfioEeaE2uzjhk"

# Fallback/Override from Environment
if os.environ.get("SUPABASE_URL"):
    SUPABASE_URL = os.environ.get("SUPABASE_URL")
if os.environ.get("SUPABASE_KEY"):
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
try:
    if SUPABASE_URL and SUPABASE_KEY:
        supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    else:
        supabase_client = None
except Exception as e:
    print(f"Failed to init Supabase: {e}")
    supabase_client = None
# supabase_client is initialized above
