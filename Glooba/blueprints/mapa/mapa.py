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
    
    logger.debug(f"Número de ubicaciones encontradas: {len(ubicaciones)}")
    
    return render_template('mapa.html',
                         api_key=api_key,
                         ubicaciones=ubicaciones, empresas=empresas)

@mapa_bp.route('/ubicaciones')
def get_ubicaciones():
    try:
        ubicaciones = Ubicacion.query.filter_by(activa=True).all()
        ubicaciones_data = []
        
        for u in ubicaciones:
            # Obtener ofertas asociadas a esta ubicación
            ofertas = [o.oferta for o in u.ofertas if o.oferta.activa]
            tipos_oferta = list(set(o.tipo.value for o in ofertas))
            
            data = {
                'id': u.id,
                'nombre': u.nombre,
                'lat': float(u.latitud),
                'lng': float(u.longitud),
                'direccion': u.direccion,
                'empresa': u.empresa.nombre,
                'empresa_id': u.empresa_id,
                'ciudad': u.ciudad,
                'region': u.region,
                'rubro': u.empresa.rubro,
                'tipos_oferta': tipos_oferta
            }
            ubicaciones_data.append(data)
            
        return jsonify(ubicaciones_data)
    except Exception as e:
        logger.error(f"Error obteniendo ubicaciones: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500