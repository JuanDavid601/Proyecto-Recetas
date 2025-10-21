from flask import Flask, render_template, request, redirect, url_for, abort
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from urllib.parse import urlparse
from models import User, Receta, Categoria, Ingredientes, Preparacion, receta_ingrediente
from slugify import slugify
from forms import SignupForm, LoginForm, CategoriaForm, IngredienteForm, PreparacionForm, RecetaForm
from extensions import db
from sqlalchemy import text

Recetas = []

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ba2e18ce248bab7ce9425333f0420b57a5f07dfef342e1876d3013a524acf416f813af3071a65e3860475fe8e81c3a42c3c8fa65051de39aa2037fa695b305a7bc7044a415eb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://postgres:Felipe1323@localhost:5432/mi_basededatos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = 'login'

db.init_app(app)

with app.app_context():
    try:
        # Ejecutar DROP de todas las tablas con CASCADE
        #db.session.execute(text('DROP SCHEMA public CASCADE; CREATE SCHEMA public;'))
        #db.session.commit()
        
        # Crear todas las tablas nuevamente
        db.create_all()
        print("All database tables dropped and recreated successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        if "no existe la base de datos" in str(e).lower():
            print("Please create the database 'mi_basededatos' first")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template('login_form.html', form=form)

@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    error = None
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        user = User.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya está registrado'
        else:
            user = User(name=name, email=email, is_admin=False)
            user.set_password(password)
            user.save()
            # usuario logueado
            login_user(user, remember=True)
            next_page = request.args.get('next', None)
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template("admin/signup_form.html", form=form, error=error)


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/delete/<string:slug>/')
@login_required
def delete_receta(slug):
    receta = Receta.get_by_slug(slug)
    if receta.preparacion:
        db.session.delete(receta.preparacion)
    receta.drop()
    
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/')
def index():
    Recetas = Receta.get_all()
    return render_template("index.html", Recetas=Recetas)

@app.route("/receta/<string:slug>/")
def show_reseta(slug):
    receta = Receta.get_by_slug(slug)
    if receta is None:
        abort(404)
    return render_template("Reseta_view.html", Receta=receta)

@app.route('/receta/create/', methods=['GET', 'POST'])
@login_required
def reseta_form():
    error = None
    
    cat_form = CategoriaForm(prefix='cat')
    ing_form = IngredienteForm(prefix='ing')
    rec_form = RecetaForm(prefix='rec')
    prepa_form = PreparacionForm(prefix='prepa')

    rec_form.categoria.choices = [(c.id, c.nombre) for c in Categoria.query.order_by(Categoria.nombre).all()]
    # Poblar opciones de preparaciones (necesario para rec_form.preparacion)
    rec_form.preparacion.choices = [(p.id, f"{p.tiempo} min - {p.descripcion}") for p in Preparacion.query.order_by(Preparacion.id).all()]
    used_ingredients = db.session.query(Ingredientes).join(receta_ingrediente).all()
    unused_ingredients = db.session.query(Ingredientes).filter(~Ingredientes.id.in_([i.id for i in used_ingredients])).order_by(Ingredientes.nombre).all()
    rec_form.ingredientes.choices = [(i.id, i.nombre) for i in unused_ingredients]

    if request.method == 'POST':
        if 'cat-submit' in request.form and cat_form.validate():
            categoria = Categoria(nombre=cat_form.nombre.data, tipo=cat_form.tipo.data, descripcion=cat_form.descripcion.data)
            categoria.save()
            return redirect(url_for('reseta_form'))

        if 'ing-submit' in request.form and ing_form.validate():
            ingrediente = Ingredientes(nombre=ing_form.nombre.data, cantidad=ing_form.cantidad.data)
            ingrediente.save()
            return redirect(url_for('reseta_form'))

        if 'prep-submit' in request.form and prepa_form.validate():
            try:
                preparacion = Preparacion(tiempo=prepa_form.tiempo.data, descripcion=prepa_form.descripcion.data)
                preparacion.save()
                print(f"Preparación guardada: tiempo={preparacion.tiempo}, descripción={preparacion.descripcion}")
                return redirect(url_for('reseta_form'))
            except Exception as e:
                db.session.rollback()
                error = f"Error al guardar la preparación: {str(e)}"
                print(error)
                return redirect(url_for('reseta_form'))
        if 'rec-submit' in request.form and rec_form.validate():
            # Crear la receta usando preparacion_id y descripcion (según models.py)
            receta = Receta(name=rec_form.nombre.data, categoria_id=rec_form.categoria.data, preparacion_id=rec_form.preparacion.data, descripcion=rec_form.descripcion.data,
            )
            # Asignar el usuario actual a la receta (user_id)
            if current_user.is_authenticated:
                receta.user_id = current_user.id

            # Asociar ingredientes seleccionados (many-to-many)
            for ingr_id in rec_form.ingredientes.data or []:
                ingr = Ingredientes.query.get(int(ingr_id))
                if ingr:
                    receta.ingredientes.append(ingr)

            receta.save()
            
            return redirect(url_for('reseta_form'))

    return render_template('admin/reseta_form.html', cat_form=cat_form, ing_form=ing_form, rec_form=rec_form, preparacion_form=prepa_form, error=error)

if __name__ == "__main__":
    app.run(debug=True)
