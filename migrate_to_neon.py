"""
Database migration script for Neon PostgreSQL
Creates all tables and enables Row-Level Security
"""
from database import engine, Base
from models import User, Account, Category, Transaction
from sqlalchemy import text

def create_tables():
    """Create all tables in Neon database"""
    print("Creating tables in Neon PostgreSQL...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

def enable_rls():
    """Enable Row-Level Security policies"""
    print("\nEnabling Row-Level Security...")
    
    with engine.connect() as conn:
        # Enable RLS on all tables
        conn.execute(text("ALTER TABLE accounts ENABLE ROW LEVEL SECURITY"))
        conn.execute(text("ALTER TABLE categories ENABLE ROW LEVEL SECURITY"))
        conn.execute(text("ALTER TABLE transactions ENABLE ROW LEVEL SECURITY"))
        
        # Drop existing policies if they exist
        conn.execute(text("DROP POLICY IF EXISTS user_accounts_policy ON accounts"))
        conn.execute(text("DROP POLICY IF EXISTS user_categories_policy ON categories"))
        conn.execute(text("DROP POLICY IF EXISTS user_transactions_policy ON transactions"))
        
        # Create RLS policies for accounts
        conn.execute(text("""
            CREATE POLICY user_accounts_policy ON accounts
            FOR ALL
            USING (user_id = NULLIF(current_setting('app.user_id', TRUE), '')::INTEGER)
        """))
        
        # Create RLS policies for categories
        conn.execute(text("""
            CREATE POLICY user_categories_policy ON categories
            FOR ALL
            USING (user_id = NULLIF(current_setting('app.user_id', TRUE), '')::INTEGER)
        """))
        
        # Create RLS policies for transactions
        conn.execute(text("""
            CREATE POLICY user_transactions_policy ON transactions
            FOR ALL
            USING (user_id = NULLIF(current_setting('app.user_id', TRUE), '')::INTEGER)
        """))
        
        conn.commit()
    
    print("✅ Row-Level Security enabled!")

def create_indexes():
    """Create indexes for better performance"""
    print("\nCreating indexes...")
    
    with engine.connect() as conn:
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_accounts_user_id ON accounts(user_id)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_categories_user_id ON categories(user_id)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(date)"))
        conn.commit()
    
    print("✅ Indexes created!")

if __name__ == "__main__":
    print("🚀 Starting Neon PostgreSQL Migration...\n")
    
    try:
        create_tables()
        enable_rls()
        create_indexes()
        
        print("\n✅ Migration completed successfully!")
        print("Your database is ready for multi-user authentication!")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        raise
