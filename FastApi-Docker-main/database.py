import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Récupération de l'URL de la base de données
DATABASE_URL = os.getenv('DATABASE_URL', "mysql+pymysql://root:@localhost:3306/Item-docker-api")

# Créer un moteur de base de données afin de gérer la connexion
engine = create_engine(DATABASE_URL)

# Créer une session locale pour interagir avec la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer une base déclarative
Base = declarative_base()

# Définir une fonction pour obtenir une session de base de données
def get_db():
    db = SessionLocal()
    try:
        # La session de base de données est ouverte et est utilisée dans la requête
        yield db
    finally:
        # La session de base de données est fermée après la fin de la requête
        db.close()
