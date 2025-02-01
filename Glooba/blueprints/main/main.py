import os
from flask import Blueprint, render_template, redirect, request, url_for, flash, current_app
from flask_login import login_required, current_user
from Glooba.models import Empresa, Oferta, Ubicacion
from sqlalchemy import func
from Glooba import db


main_bp = Blueprint("main", __name__, template_folder="templates")

# @main_bp.route("/mat")
# def bienvenida():
#     return render_template('bienvenida.html')

@main_bp.route("/informacion")
def index():
    return render_template('informative_page.html')

@main_bp.route("/enrolamiento_empresas")
def enrolamiento_empresas():
    return render_template('empresa_enrollment.html')

@main_bp.route("/nosotros")
def nosotros():
    return render_template('about_us.html')

@main_bp.route('/configuracion')
def configuracion():
    return render_template('dashboard-base.html')

@main_bp.route("/")
def empresas():
    # Obtener parámetros de la URL
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    categoria = request.args.get('categoria', '')
    descuento = request.args.get('descuento', type=bool)
    per_page = 8  # Número de empresas por página

    # Construir la consulta base
    query = db.session.query(
        Empresa,
        func.count(Oferta.id).label('total_ofertas'),
        func.count(Ubicacion.id).label('total_ubicaciones')
    ).outerjoin(
        Oferta, (Empresa.id == Oferta.empresa_id) & (Oferta.activa == True)
    ).outerjoin(
        Ubicacion, (Empresa.id == Ubicacion.empresa_id) & (Ubicacion.activa == True)
    ).filter(
        Empresa.activo == True
    )

    # Aplicar filtro de búsqueda si existe
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            db.or_(
                Empresa.nombre.ilike(search_term),
                Empresa.rubro.ilike(search_term),
                Empresa.descripcion.ilike(search_term),
                Oferta.titulo.ilike(search_term),
                Oferta.descripcion.ilike(search_term)
            )
        )

    # Aplicar filtro de categoría si existe
    if categoria:
        query = query.filter(Empresa.rubro == categoria)

    # Aplicar filtro de descuento si está marcado
    if descuento:
        query = query.filter(Oferta.es_descuento == True)

    # Agrupar y ordenar
    query = query.group_by(Empresa.id).order_by(Empresa.nombre)

    # Realizar la paginación
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    empresas = pagination.items

    # Preparar los datos para el template
    empresas_data = []
    for empresa, total_ofertas, total_ubicaciones in empresas:
        sitio_web = empresa.sitio_web
        if sitio_web:
            # Asegurarse de que la URL tenga el protocolo
            if not sitio_web.startswith(('http://', 'https://')):
                sitio_web = 'https://' + sitio_web
            sitio_web = sitio_web.strip()

        # Verificar si existe el logo de la empresa
        logo_filename = f"{empresa.nombre}.png"
        logo_path = os.path.join('static', 'images', 'logos_de_empresas', logo_filename)
        full_logo_path = os.path.join(current_app.root_path, logo_path)
        
        logo_url = (
            url_for('static', filename=f'images/logos_de_empresas/{logo_filename}')
            if os.path.exists(full_logo_path)
            else '/api/placeholder/192/192'
        )

        empresas_data.append({
            'id': empresa.id,
            'nombre': empresa.nombre,
            'descripcion': empresa.descripcion or "Sin descripción disponible",
            'rubro': empresa.rubro or "Rubro no especificado",
            'imagen_perfil': empresa.imagen_perfil_url,  # Llamamos a la propiedad imagen_perfil_url
            'imagen_fondo': empresa.imagen_principal_url,
            'sitio_web': sitio_web,
            'total_ofertas': total_ofertas,
            'total_ubicaciones': total_ubicaciones,
            'logo_url': logo_url
        })

    # Obtener categorías únicas para el filtro
    categorias = db.session.query(Empresa.rubro).distinct().filter(
        Empresa.rubro.isnot(None),
        Empresa.activo == True
    ).all()
    categorias = [cat[0] for cat in categorias if cat[0]]

    # Obtener todas las ubicaciones activas
    ubicaciones = Ubicacion.query.filter_by(activa=True).all()
    api_key = current_app.config['GOOGLE_MAPS_API_KEY']
    
    return render_template(
        'main_page.html',
        empresas=empresas_data,
        pagination=pagination,
        search=search,
        categoria_actual=categoria,
        categorias=categorias,
        descuento=descuento,
        ubicaciones=ubicaciones,
        api_key=api_key
    )

@main_bp.route('/empresas/<int:empresa_id>')
def perfil_empresa(empresa_id):
    empresa = Empresa.query.get_or_404(empresa_id)
    ubicaciones = Ubicacion.query.filter_by(empresa_id=empresa_id).all()
    api_key = current_app.config['GOOGLE_MAPS_API_KEY']
    ofertas = Oferta.query.filter_by(empresa_id=empresa_id).all()
    return render_template(
        'empresa_profile.html', 
        empresa=empresa, 
        ubicaciones=ubicaciones, 
        api_key=api_key,
        ofertas=ofertas)