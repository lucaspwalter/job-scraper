from app.db.database import SessionLocal
from app.models.job import Job
from app.models.source import Source


db = SessionLocal()
db.query(Job).delete()
db.commit()
db.close()
print("Jobs limpos.")
