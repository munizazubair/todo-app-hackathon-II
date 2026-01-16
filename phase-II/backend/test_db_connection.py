"""Test database connection."""
from db.database import engine
from sqlmodel import Session, text
import time

print("Attempting to connect to Neon database...")
print("This may take 10-15 seconds if the database is suspended...")

try:
    start_time = time.time()
    with Session(engine) as session:
        result = session.exec(text("SELECT 1")).first()
        elapsed = time.time() - start_time
        print(f"\n[OK] Database connection successful!")
        print(f"  Time taken: {elapsed:.2f} seconds")
        print(f"  Query result: {result}")

        # Check if todos table exists
        tables = session.exec(text("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """)).all()
        print(f"\n  Tables in database: {[t[0] for t in tables]}")

except Exception as e:
    print(f"\n[FAIL] Connection failed!")
    print(f"  Error: {e}")
    print("\nPossible solutions:")
    print("  1. Check if your Neon database is active (visit Neon dashboard)")
    print("  2. Verify DATABASE_URL in .env file")
    print("  3. Try again - Neon databases auto-suspend and may need 10-15s to wake up")
