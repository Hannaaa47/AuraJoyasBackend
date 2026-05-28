import os
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from dotenv import load_dotenv

from db import get_connection
from validators import validar_registro, validar_login, validar_contacto, validar_catalogo
from security import verificar_password
from email_service import enviar_correo_contacto
from models import Registro

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "clave_temporal_desarrollo")

CORS(app, supports_credentials=True, 
origins=["https://aura-joyas.vercel.app")

@app.route("/")
def inicio():
    return jsonify({
        "mensaje": "Backend Flask activo",
        "proyecto": "Plantilla genérica de negocio"
    }), 200



# ── REGISTROS ────────────────────────────────────────────────────────────────

@app.route("/registros", methods=["GET"])
def obtener_registros():
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM registros")
    registros = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(registros), 200

@app.route("/registros/<int:id>", methods=["GET"])
def obtener_registro(id):
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, categoria, descripcion, precio, activo, destacado FROM registros WHERE id = %s", (id,))
    registro = cursor.fetchone()
    cursor.close()
    conexion.close()
    if not registro:
        return jsonify({"mensaje": "Registro no encontrado"}), 404
    return jsonify(registro), 200

@app.route("/registros", methods=["POST"])
def agregar_registro():
    data = request.json
    errores = validar_registro(data)
    if errores:
        return jsonify({"errores": errores}), 400

    conexion = get_connection()
    cursor = conexion.cursor()
    sql = """
        INSERT INTO registros (nombre, categoria, descripcion, precio, activo, destacado)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (
        data.get("nombre"),
        data.get("categoria"),
        data.get("descripcion"),
        float(data.get("precio", 0)),
        bool(data.get("activo", 1)),
        bool(data.get("destacado", 0))
    )
    cursor.execute(sql, valores)
    conexion.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Registro agregado correctamente", "id": nuevo_id}), 201

@app.route("/registros/<int:id>", methods=["PUT"])
def actualizar_registro(id):
    data = request.json
    errores = validar_registro(data)
    if errores:
        return jsonify({"errores": errores}), 400

    conexion = get_connection()
    cursor = conexion.cursor()
    sql = """
        UPDATE registros
        SET nombre = %s, categoria = %s, descripcion = %s, precio = %s, activo = %s, destacado = %s
        WHERE id = %s
    """
    valores = (
        data.get("nombre"),
        data.get("categoria"),
        data.get("descripcion"),
        float(data.get("precio", 0)),
        bool(data.get("activo", True)),
        bool(data.get("destacado", False)),
        id
    )
    cursor.execute(sql, valores)
    conexion.commit()
    filas_afectadas = cursor.rowcount
    cursor.close()
    conexion.close()
    if filas_afectadas == 0:
        return jsonify({"mensaje": "Registro no encontrado"}), 404
    return jsonify({"mensaje": "Registro actualizado correctamente"}), 200

@app.route("/registros/<int:id>/desactivar", methods=["PUT"])
def desactivar_registro(id):
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("UPDATE registros SET activo = 0 WHERE id = %s", (id,))
    conexion.commit()
    filas_afectadas = cursor.rowcount
    cursor.close()
    conexion.close()
    if filas_afectadas == 0:
        return jsonify({"mensaje": "Registro no encontrado"}), 404
    return jsonify({"mensaje": "Registro desactivado correctamente"}), 200



# ── CATÁLOGO ─────────────────────────────────────────────────────────────────

@app.route("/catalogo", methods=["GET"])
def obtener_catalogo():
    """Obtiene todos los productos activos del catálogo."""
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM catalogo WHERE activo = 1")
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(productos), 200

@app.route("/catalogo/<int:id>", methods=["GET"])
def obtener_producto(id):
    """Obtiene un producto del catálogo por ID."""
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM catalogo WHERE id = %s AND activo = 1", (id,))
    producto = cursor.fetchone()
    cursor.close()
    conexion.close()
    if not producto:
        return jsonify({"mensaje": "Producto no encontrado"}), 404
    return jsonify(producto), 200

@app.route("/catalogo", methods=["POST"])
def agregar_producto():
    """Agrega un nuevo producto al catálogo."""
    data = request.json
    errores = validar_catalogo(data)
    if errores:
        return jsonify({"errores": errores}), 400

    conexion = get_connection()
    cursor = conexion.cursor()
    sql = """
        INSERT INTO catalogo (nombre, descripcion, precio, existencia, imagen, activo)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (
        data.get("nombre"),
        data.get("descripcion"),
        float(data.get("precio", 0)),
        int(data.get("existencia", 0)),
        data.get("imagen", None),
        bool(data.get("activo", True))
    )
    cursor.execute(sql, valores)
    conexion.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Producto agregado correctamente", "id": nuevo_id}), 201

@app.route("/catalogo/<int:id>", methods=["PUT"])
def actualizar_producto(id):
    """Actualiza un producto existente del catálogo."""
    data = request.json
    errores = validar_catalogo(data)
    if errores:
        return jsonify({"errores": errores}), 400

    conexion = get_connection()
    cursor = conexion.cursor()
    sql = """
        UPDATE catalogo
        SET nombre = %s, descripcion = %s, precio = %s, existencia = %s, imagen = %s
        WHERE id = %s
    """
    valores = (
        data.get("nombre"),
        data.get("descripcion"),
        float(data.get("precio", 0)),
        int(data.get("existencia", 0)),
        data.get("imagen", None),
        id
    )
    cursor.execute(sql, valores)
    conexion.commit()
    filas_afectadas = cursor.rowcount
    cursor.close()
    conexion.close()
    if filas_afectadas == 0:
        return jsonify({"mensaje": "Producto no encontrado"}), 404
    return jsonify({"mensaje": "Producto actualizado correctamente"}), 200

@app.route("/catalogo/<int:id>/desactivar", methods=["PUT"])
def desactivar_producto(id):
    """Desactiva un producto del catálogo sin eliminarlo."""
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("UPDATE catalogo SET activo = 0 WHERE id = %s", (id,))
    conexion.commit()
    filas_afectadas = cursor.rowcount
    cursor.close()
    conexion.close()
    if filas_afectadas == 0:
        return jsonify({"mensaje": "Producto no encontrado"}), 404
    return jsonify({"mensaje": "Producto desactivado correctamente"}), 200



# ── LOGIN Y SESIÓN ────────────────────────────────────────────────────────────

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    errores = validar_login(data)
    if errores:
        return jsonify({"errores": errores}), 400

    correo   = data.get("correo")
    password = data.get("password")

    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
    usuario = cursor.fetchone()
    cursor.close()
    conexion.close()

    if not usuario:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    if not verificar_password(password, usuario["password"]):
        return jsonify({"mensaje": "Contraseña incorrecta"}), 401

    session["usuario_id"]    = usuario["id"]
    session["nombreUsuario"] = usuario["nombre"]
    session["correo"]        = usuario["correo"]
    session["autenticado"]   = True

    return jsonify({
        "mensaje": "Sesión iniciada correctamente",
        "sesion": {
            "nombreUsuario": usuario["nombre"],
            "correo":        usuario["correo"],
            "autenticado":   True
        }
    }), 200

@app.route("/sesion", methods=["GET"])
def obtener_sesion():
    if session.get("autenticado"):
        return jsonify({
            "nombreUsuario": session.get("nombreUsuario"),
            "correo":        session.get("correo"),
            "autenticado":   True
        }), 200
    return jsonify({"nombreUsuario": "Invitado", "correo": None, "autenticado": False}), 200

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"mensaje": "Sesión cerrada correctamente"}), 200



# ── CONTACTO ──────────────────────────────────────────────────────────────────

@app.route("/contacto", methods=["POST"])
def contacto():
    data = request.json
    errores = validar_contacto(data)
    if errores:
        return jsonify({"errores": errores}), 400

    enviar_correo_contacto(
        data.get("nombre"),
        data.get("correo"),
        data.get("mensaje")
    )
    return jsonify({"mensaje": "Correo enviado correctamente"}), 200


if __name__ == "__main__":
    app.run(debug=True)