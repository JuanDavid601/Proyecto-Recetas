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
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Guardar Ingrediente')


class PreparacionForm(FlaskForm):
    # Según models.py Preparacion tiene: tiempo, ingredientes (string) y descripcion
    tiempo = IntegerField('Tiempo (min)', validators=[DataRequired(), NumberRange(min=0)])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Guardar Preparación')


class RecetaForm(FlaskForm):
    # En models.py Receta tiene: name, categoria_id, preparacion_id, slug, descripcion
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    categoria = SelectField('Categoría', coerce=int, validators=[Optional()])
    preparacion = SelectField('Preparación', coerce=int, validators=[DataRequired()])
    descripcion = TextAreaField('Descripción', validators=[DataRequired()])
    # Mantenemos selección múltiple de ingredientes (relación many-to-many)
    ingredientes = SelectMultipleField('Ingredientes', coerce=int, validators=[Optional()])
    submit = SubmitField('Guardar Receta')