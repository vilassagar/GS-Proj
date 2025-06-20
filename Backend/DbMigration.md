# Complete Database Migration Guide

## 1. Check Migration Status
```bash
# See current migration version
alembic current

# See all migration history
alembic history --verbose

# See pending migrations
alembic show head
```

## 2. Apply Existing Migrations
```bash
# Apply all pending migrations to latest
alembic upgrade head

# Apply to specific revision
alembic upgrade revision_id

# Apply one step forward
alembic upgrade +1
```

## 3. Create New Migrations
```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add new table"

# Create empty migration file (manual)
alembic revision -m "Manual migration"
```

## 4. Rollback Migrations
```bash
# Rollback to previous migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade revision_id

# Rollback all migrations
alembic downgrade base
```

## 5. Reset Database (if needed)
```bash
# Drop all tables and start fresh
alembic downgrade base
alembic upgrade head
```

## 6. Migration File Structure
Your migration files are in: `Backend/alembic/versions/`

Each migration file contains:
- `upgrade()` function - creates/modifies tables
- `downgrade()` function - reverses the changes

## 7. Common Issues and Solutions

### Issue: "target database is not up to date"
```bash
alembic stamp head  # Mark current state as latest
```

### Issue: "Can't locate revision identified by 'head'"
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### Issue: Database connection errors
- Check your DATABASE_URL in .env file
- Ensure PostgreSQL is running
- Verify database exists

## 8. Your Current Models
Based on your code, these tables will be created:
- `departments`
- `districts` 
- `blocks`
- `gram_panchayats`
- `roles`
- `users`
- `yojanas`
- `grs`
- `books`
- `document_types`
- `user_documents`
- `user_otps`

## 9. Verification
After migration, verify tables exist:
```sql
-- Connect to your database
psql -U postgres -d Gs_DB

-- List all tables
\dt

-- Check specific table structure
\d users

-- Exit
\q
```