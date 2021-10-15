from app.config.app_config import conf
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_engine = create_engine(conf.DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
