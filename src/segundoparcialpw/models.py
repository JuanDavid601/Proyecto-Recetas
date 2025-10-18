from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from werkzeug.security import generate_password_hash, check_password_hash


Base = declarative_base()

receta_ingrediente = Table(
    'receta_ingrediente', Base.metadata,
    Column('receta_id', Integer, ForeignKey('recetas.id'), primary_key=True),
    Column('ingrediente_id', Integer, ForeignKey('ingredientes.id'), primary_key=True),
    Column('cantidad', String, nullable=True)
)

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(120), nullable=False)
    correo = Column(String(120), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    recetas = relationship('Receta', back_populates='autor')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Categoria(Base):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(80), nullable=False)
    tipo = Column(String(80), nullable=False)
    descripcion = Column(Text, nullable=False)

    recetas = relationship('Receta', back_populates='categoria')

class Receta(Base):
    __tablename__ = 'recetas'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(120), nullable=False)
    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=False)
    autor_id = Column(Integer, ForeignKey('usuarios.id'), nullable=True)
    tiempo = Column(Integer, nullable=False)

    categoria = relationship('Categoria', back_populates='recetas')
    autor = relationship('Usuario', back_populates='recetas')
    ingredientes = relationship('Ingrediente', secondary=receta_ingrediente, back_populates='recetas')
    pasos = relationship('Preparacion', back_populates='receta', cascade='all, delete-orphan', order_by='Preparacion.orden')

class Ingrediente(Base):
    __tablename__ = 'ingredientes'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(120), nullable=False, unique=True)

    recetas = relationship('Receta', secondary=receta_ingrediente, back_populates='ingredientes')

class Preparacion(Base):
    __tablename__ = 'preparaciones'
    id = Column(Integer, primary_key=True)
    receta_id = Column(Integer, ForeignKey('recetas.id'), nullable=False)
    orden = Column(Integer, nullable=False)
    descripcion = Column(Text, nullable=False)
    tiempo = Column(Integer, nullable=True)

    receta = relationship('Receta', back_populates='pasos')