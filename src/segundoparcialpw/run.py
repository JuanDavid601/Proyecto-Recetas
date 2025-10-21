from flask import Flask, render_template, request, redirect, url_for, abort
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from urllib.parse import urlparse
from forms import SignupForm, LoginForm, CategoriaForm, IngredienteForm, RecetaForm
from extensions import db

Recetas = []

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ba2e18ce248bab7ce9425333f0420b57a5f07dfef342e1876d3013a524acf416f813af3071a65e3860475fe8e81c3a42c3c8fa65051de39aa2037fa695b305a7bc7044a415eb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://postgres:Felipe1323@localhost:5432/mi_basededatos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Initialize extensions
db.init_app(app)

# Create all database tables
with app.app_context():
    db.create_all()

from models import Usuario, Receta, Categoria, Ingrediente, Preparacion, receta_ingrediente

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.get_by_email(form.email.data)
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
        user = Usuario.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya está registrado'
        else:
            user = Usuario(nombre=name, correo=email, is_admin=False)
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
    return Usuario.get_by_id(int(user_id))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    Recetas = Receta.get_all()
    return render_template("index.html", Recetas=Recetas)

@app.route("/reseta/<string:slug>/")
def show_reseta(slug):
    Reseta = Reseta.get_by_slug(slug)
    if Reseta is None:
        abort(404)
    return render_template("Reseta_view.html", ad=ad)

@app.route('/+Reseta/', methods=['GET', 'POST'])
def reseta_form():
    error = None
    # instantiate three forms with prefixes to avoid name collisions in the POST
    cat_form = CategoriaForm(prefix='cat')
    ing_form = IngredienteForm(prefix='ing')
    rec_form = RecetaForm(prefix='rec')

    # populate choices for receta form
    rec_form.categoria.choices = [(c.id, c.nombre) for c in Categoria.query.order_by(Categoria.nombre).all()]
    # Get only ingredients that are not used in any recipe
    used_ingredients = db.session.query(Ingrediente).join(receta_ingrediente).all()
    unused_ingredients = db.session.query(Ingrediente).filter(~Ingrediente.id.in_([i.id for i in used_ingredients])).order_by(Ingrediente.nombre).all()
    rec_form.ingredientes.choices = [(i.id, i.nombre) for i in unused_ingredients]

    if request.method == 'POST':
        # detect which form was submitted by looking for the prefixed submit name
        if 'cat-submit' in request.form and cat_form.validate():
            categoria = Categoria(nombre=cat_form.nombre.data, tipo=cat_form.tipo.data, descripcion=cat_form.descripcion.data)
            db.session.add(categoria)
            db.session.commit()
            return redirect(url_for('reseta_form'))

        if 'ing-submit' in request.form and ing_form.validate():
            ingrediente = Ingrediente(nombre=ing_form.nombre.data)
            db.session.add(ingrediente)
            db.session.commit()
            return redirect(url_for('reseta_form'))

        if 'rec-submit' in request.form and rec_form.validate():
            receta = Receta(nombre=rec_form.nombre.data, categoria_id=rec_form.categoria.data, tiempo=rec_form.tiempo.data)
            if current_user.is_authenticated:
                receta.autor = current_user

            for ingr_id in rec_form.ingredientes.data or []:
                ingr = Ingrediente.query.get(int(ingr_id))
                if ingr:
                    receta.ingredientes.append(ingr)

            db.session.add(receta)
            db.session.flush()

            pasos_text = rec_form.pasos.data or ''
            pasos_lines = [p.strip() for p in pasos_text.splitlines() if p.strip()]
            for idx, linea in enumerate(pasos_lines, start=1):
                paso = Preparacion(receta_id=receta.id, orden=idx, descripcion=linea)
                db.session.add(paso)

            db.session.commit()
            return redirect(url_for('reseta_form'))

    return render_template('admin/reseta_form.html', cat_form=cat_form, ing_form=ing_form, rec_form=rec_form, error=error)

if __name__ == "__main__":
    app.run(debug=True)
