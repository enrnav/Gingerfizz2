from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models import db, User, InventoryItem, CustomerRequirement, Notification
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gingerfizz_super_secret_key_2026'

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gingerfizz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure session to use filesystem
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Initialize database
db.init_app(app)

with app.app_context():
    db.create_all()

# --- Decorator for requiring login ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# --- Routes ---

@app.route("/")
@login_required
def index():
    return redirect(url_for("dashboard"))
    

@app.route("/dashboard")
@login_required
def dashboard():
    user = User.query.get(session["user_id"])
    inventory = InventoryItem.query.all()
    needs = CustomerRequirement.query.all()
    notifications = Notification.query.filter_by(user_id=user.id).order_by(Notification.created_at.desc()).limit(10).all()
    return render_template("dashboard/index.html", user=user, inventory=inventory, needs=needs, notifications=notifications)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash("Usuario o contraseña incorrectos", "error")
            return render_template("auth/login.html")
            
        session["user_id"] = user.id
        return redirect(url_for("dashboard"))
        
    return render_template("auth/login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        if password != confirmation:
            flash("Las contraseñas no coinciden", "error")
            return render_template("auth/register.html")
            
        if User.query.filter_by(username=username).first():
            flash("El usuario ya existe", "error")
            return render_template("auth/register.html")
            
        new_user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        
        # Opcional: Crear la primera notificación para el usuario
        welcome_notif = Notification(user_id=new_user.id, message="¡Bienvenido a GingerFizz!")
        db.session.add(welcome_notif)
        db.session.commit()
        
        flash("Registro exitoso, por favor inicia sesión.", "success")
        return redirect(url_for("login"))
        
    return render_template("auth/register.html")

@app.route("/inventory", methods=["GET", "POST"])
@login_required
def manage_inventory():
    if request.method == "POST":
        name = request.form.get("name")
        qty_available = int(request.form.get("quantity_available", 0))
        qty_required = int(request.form.get("quantity_required", 0))
        
        item = InventoryItem(name=name, quantity_available=qty_available, quantity_required=qty_required)
        db.session.add(item)
        db.session.commit()
        flash("Ítem agregado al inventario", "success")
        return redirect(url_for("manage_inventory"))
        
    items = InventoryItem.query.all()
    return render_template("dashboard/inventory.html", inventory=items)

@app.route("/inventory/update/<int:item_id>", methods=["POST"])
@login_required
def update_inventory(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    item.quantity_available = int(request.form.get("quantity_available", item.quantity_available))
    item.quantity_required = int(request.form.get("quantity_required", item.quantity_required))
    db.session.commit()
    flash("Inventario actualizado", "success")
    return redirect(url_for("manage_inventory"))

@app.route("/needs", methods=["POST"])
@login_required
def add_need():
    customer_name = request.form.get("customer_name")
    description = request.form.get("description")
    
    new_need = CustomerRequirement(customer_name=customer_name, description=description)
    db.session.add(new_need)
    
    admin_notif = Notification(user_id=session["user_id"], message=f"Nueva necesidad de cliente: {customer_name}")
    db.session.add(admin_notif)
    
    db.session.commit()
    flash("Necesidad de cliente registrada", "success")
    return redirect(url_for("dashboard"))

@app.route("/needs/<int:need_id>/resolve", methods=["POST"])
@login_required
def resolve_need(need_id):
    need = CustomerRequirement.query.get_or_404(need_id)
    need.status = "Resuelto"
    db.session.commit()
    flash("Necesidad marcada como resuelta", "success")
    return redirect(url_for("dashboard"))

@app.route("/notifications/read/<int:notif_id>", methods=["POST"])
@login_required
def read_notification(notif_id):
    notif = Notification.query.get_or_404(notif_id)
    if notif.user_id == session["user_id"]:
        notif.is_read = True
        db.session.commit()
    return jsonify({"success": True})

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
