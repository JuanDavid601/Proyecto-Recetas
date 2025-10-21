from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    TextAreaField,
    BooleanField,
    IntegerField,
    SelectField,
    SelectMultipleField,
)
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange

class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Registrar')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Recuérdame')
    submit = SubmitField('Login')


class CategoriaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=80)])
    tipo = StringField('Tipo', validators=[DataRequired(), Length(max=80)])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Guardar Categoria')


class IngredienteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=120)])
    submit = SubmitField('Guardar Ingrediente')


class PreparacionForm(FlaskForm):
    orden = IntegerField('Orden', validators=[DataRequired(), NumberRange(min=1)])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    tiempo = IntegerField('Tiempo (min)', validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField('Guardar Paso')


class RecetaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=120)])
    categoria = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    tiempo = IntegerField('Tiempo total (min)', validators=[DataRequired(), NumberRange(min=0)])
    ingredientes = SelectMultipleField('Ingredientes', coerce=int, validators=[Optional()])
    pasos = TextAreaField('Pasos (un paso por línea)', validators=[Optional()])
    submit = SubmitField('Guardar Receta')