#base 
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime #para registrar la fecha y hora de creación de la cotización
import random #para generar un número de cotización único
#IA
from ia import analizar_con_ia
from flask import Response
import json
from collections import OrderedDict
#sesiones
from flask import session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'clave-secreta' #sesiones


# Configuro la base de datos local con SQLite.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
USUARIOS = {"admin": "1234"}  #usuarios

# Modelo Cotizacion, tabla en la base de datos
class Cotizacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # ID único, autoincremental
    numero_cotizacion = db.Column(db.String(20), unique=True, nullable=False)  # Código único, COT-2025-XXXX
    nombre_cliente = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    tipo_servicio = db.Column(db.String(100), nullable=False)  # Servicio seleccionado
    precio = db.Column(db.Float, nullable=False)  # Precio según servicio
    fecha = db.Column(db.DateTime, default=datetime.now) # Fecha de creación automática
    descripcion = db.Column(db.Text, nullable=True)  # Texto ingresado por el cliente

# Diccionario con los precios fijos por cada tipo de servicio
PRECIOS = {
    "Constitución de empresa": 1500,
    "Defensa laboral": 2000,
    "Consultoría tributaria": 800
}

#bonus login y logout
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        clave = request.form.get("clave")
        if USUARIOS.get(usuario) == clave:
            session["usuario"] = usuario
            return redirect(url_for("index"))
        return "Credenciales incorrectas", 401
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# Carga el formulario
@app.route('/')
def index():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template('index.html')

# Se activa al enviar el formulario. Procesa y genera cotización.
@app.route('/generar', methods=['POST'])
def generar_cotizacion():
    data = request.form

    # Busco el precio correspondiente
    tipo_servicio = data['tipo_servicio']
    precio = PRECIOS.get(tipo_servicio, 0)
    descripcion = data['descripcion']

    numero_cotizacion = f"COT-2025-{random.randint(1000, 9999)}"

    # Llamar a la IA
    ia_resultado = analizar_con_ia(descripcion, tipo_servicio)

    # Ajustar el precio según IA
    if "ajuste_precio" in ia_resultado:
        try:
            ajuste = int(ia_resultado.get("ajuste_precio", "0%").replace("%", ""))
            precio_final = precio + (precio * ajuste // 100)
        except:
            ajuste = 0
            precio_final = precio

    else:
        precio_final = precio
    
    # Creo una instancia de cotización con los datos del formulario
    cotizacion = Cotizacion(
        numero_cotizacion=numero_cotizacion,
        nombre_cliente=data['nombre'],
        email=data['email'],
        tipo_servicio=tipo_servicio,
        precio=precio,
        descripcion=data['descripcion']
    )

    # Guardo la cotización en la base de datos
    db.session.add(cotizacion)
    db.session.commit()

    # Devuelvo los datos generados en formato JSON para mostrar al cliente
    response = OrderedDict([
        ("numero_cotizacion", numero_cotizacion),
        ("nombre_cliente", data['nombre']),
        ("email", data['email']),
        ("tipo_servicio", tipo_servicio),
        ("precio", precio),
        ("precio_final", precio_final),
        ("fecha", cotizacion.fecha.strftime("%Y-%m-%d %H:%M:%S")),
        ("complejidad", ia_resultado.get("complejidad")),
        ("ajuste_precio", ia_resultado.get("ajuste_precio")),
        ("servicios_adicionales", ia_resultado.get("servicios_adicionales")),
        ("propuesta", ia_resultado.get("propuesta_texto"))
    ])

    #Para asegurar que salga en el orden indicado
    return Response(
        json.dumps(response, indent=4, ensure_ascii=False),
        mimetype='application/json'
    )

if __name__ == '__main__':
    # Aseguro que las tablas de la base de datos estén creadas antes de correr
    with app.app_context():
        db.create_all()
    # Ejecuto la app en modo desarrollo, puedo ver errores en consola
    app.run(debug=True)
