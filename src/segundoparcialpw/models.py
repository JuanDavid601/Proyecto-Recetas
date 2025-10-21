from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, Table, Text
from slugify import slugify
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import url_for
from extensions import db




receta_ingrediente = Table(
    'receta_ingrediente',
    db.metadata,
    Column('receta_id', Integer, ForeignKey('recetas.id', ondelete='CASCADE'), primary_key=True),
    Column('ingrediente_id', Integer, ForeignKey('Ingredientes.id', ondelete='CASCADE'), primary_key=True)
)

class User(db.Model, UserMixin):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    recetas = relationship('Receta', back_populates='usuario', cascade='all, delete')


    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

class Receta(db.Model, UserMixin):

    __tablename__ = 'recetas'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    categoria_id = db.Column(db.Integer, ForeignKey('categorias.id'))
    preparacion_id = db.Column(db.Integer, ForeignKey('Preparaciones.id'), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)


    usuario = relationship('User', back_populates='recetas')
    categoria = relationship('Categoria', back_populates='recetas')
    preparacion = relationship('Preparacion', back_populates='recetas')
    ingredientes = relationship('Ingredientes', secondary=receta_ingrediente, back_populates='recetas')



    def save(self):
        if not self.id:
            db.session.add(self)
        if not self.slug:
            self.slug = slugify(self.name)
        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                count += 1
                self.slug = f'{slugify(self.name)}-{count}'

    def drop(self):
        db.session.delete(self)
        db.session.commit()

    def public_url(self):
        return url_for('show_recetas', slug=self.slug)
    
    @staticmethod
    def get_by_slug(slug):
        return Receta.query.filter_by(slug=slug).first()
    
    @staticmethod
    def get_receta_by_id(id):
        return Receta.query.get(id)
    
    @staticmethod
    def get_all():
        return Receta.query.all()

class Categoria(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)

    recetas = relationship('Receta', back_populates='categoria', cascade='all, delete')

    
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def drop(self):
        db.session.delete(self)
        db.session.commit()

class Ingredientes(db.Model):
    __tablename__ = 'Ingredientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)


    recetas = relationship('Receta', secondary=receta_ingrediente, back_populates='ingredientes')

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    
    def drop(self):
        db.session.delete(self)
        db.sessiion.commit()


class Preparacion(db.Model):
    __tablename__ = 'Preparaciones'

    id = db.Column(db.Integer, primary_key=True)
    tiempo = db.Column(db.Integer, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)


    recetas = relationship('Receta', back_populates='preparacion')

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def drop(self):
        db.session.delete(self)
        db.sessiion.commit()
