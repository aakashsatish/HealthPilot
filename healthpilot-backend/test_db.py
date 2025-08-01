from dotenv import load_dotenv
load_dotenv()

from app.database import DatabaseService

db = DatabaseService()

# Test saving a report
result = db.save_lab_report(
    user_id="test-user-123",
    file_path="/tmp/test.pdf",
    original_filename="test.pdf"
)

print(f"Database test result: {result}")
