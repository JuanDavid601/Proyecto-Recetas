import psycopg
from src.segundoparcialpw.run import app, db
from src.segundoparcialpw.models import User, Receta, Categoria, Ingredientes, Preparacion

def init_db():
    # Create database if it doesn't exist
    conn = psycopg.connect('dbname=mi_basededatos user=postgres password=Felipe1323')
    conn.autocommit = True
    cur = conn.cursor()
    try:
        cur.execute('CREATE DATABASE mi_basededatos')
        print('Database created successfully')
    except psycopg.errors.DuplicateDatabase:
        print('Database already exists')
    finally:
        cur.close()
        conn.close()

    # Create all tables
    with app.app_context():
        db.drop_all()  # This will drop all tables to ensure we start fresh
        db.create_all()
        print('All tables created successfully')

if __name__ == '__main__':
    init_db()