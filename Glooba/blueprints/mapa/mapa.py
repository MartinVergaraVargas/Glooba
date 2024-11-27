from flask import Blueprint, render_template, current_app, jsonify
from flask_login import login_required
from Glooba.models import Ubicacion, Empresa
import logging 

mapa_bp = Blueprint('mapa', __name__, template_folder='templates')
logger = logging.getLogger(__name__)

@mapa_bp.route('/')
def mostrar_mapa():
    # Obtener todas las ubicaciones activas
    ubicaciones = Ubicacion.query.filter_by(activa=True).all()
    api_key = current_app.config['GOOGLE_MAPS_API_KEY']
    empresas = Empresa.query.all()
    logger.debug(f"API Key presente: {'Sí' if api_key else 'No'}")
    
    # Obtener todas las ubicaciones activas
    ubicaciones = Ubicacion.query.filter_by(activa=True).all()
    logger.debug(f"Número de ubicaciones encontradas: {len(ubicaciones)}")
    
    return render_template('mapa.html',
                         api_key=api_key,
                         ubicaciones=ubicaciones, empresas=empresas)

@mapa_bp.route('/ubicaciones')
@login_required
def get_ubicaciones():
    ubicaciones = Ubicacion.query.filter_by(activa=True).all()
    ubicaciones_data = [{
        'id': u.id,
        'nombre': u.nombre,
        'lat': u.latitud,
        'lng': u.longitud,
        'direccion': u.direccion,
        'empresa': u.empresa.nombre,
        'ciudad': u.ciudad,
        'region': u.region
    } for u in ubicaciones]
    return jsonify(ubicaciones_data)
