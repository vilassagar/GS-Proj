from sqlalchemy import create_engine, Table, MetaData
import datetime

engine = create_engine("postgresql://postgres:#Mystack9393#@localhost:5432/Gs_devDB")
metadata = MetaData()
conn = engine.connect()

departments = Table('departments', metadata, autoload_with=engine)
conn.execute(departments.insert(), [
    {'id': 1, 'name': 'कृषी विभाग', 'created_at': datetime.datetime.utcnow(), 'updated_at': None, 'is_active': True}
])
# Repeat for other tables...

conn.close()