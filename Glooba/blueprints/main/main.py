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
    return render_template('pagina_principal.html')

@main_bp.route("/enrolamiento_empresas")
def enrolamiento_empresas():
    return render_template('pagina_empresas.html')

@main_bp.route("/ofertas")
def ofertas():
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    tipo = request.args.get('tipo', None)
    search = request.args.get('search', '')
    per_page = 12  # Number of offers per page

    # Query for offers with pagination
    offers_query = db.session.query(
        Oferta,
        Empresa.nombre.label('empresa_nombre')
    ).join(
        Empresa, Oferta.empresa_id == Empresa.id
    ).filter(
        Oferta.activa == True,
        Empresa.activo == True
    ).order_by(
        Oferta.fecha_inicio.desc()
    )

    # Apply type filter if specified
    if search:
        search_term = f"%{search}%"
        offers_query = offers_query.filter(
            db.or_(
                Oferta.titulo.ilike(search_term),
                Oferta.descripcion.ilike(search_term),
                Empresa.nombre.ilike(search_term),
                Empresa.descripcion.ilike(search_term)
            )
        )

    if tipo:
        offers_query = offers_query.filter(Oferta.tipo == tipo.upper())

    # Order by date
    offers_query = offers_query.order_by(Oferta.fecha_inicio.desc())

    # Apply pagination
    pagination = offers_query.paginate(page=page, per_page=per_page, error_out=False)
    ofertas_paginadas = pagination.items

    # Process offers for template
    ofertas_procesadas = []
    for oferta, empresa_nombre in ofertas_paginadas:
        precio_mostrar = ""
        
        if oferta.tipo == 'PRODUCTO' or oferta.tipo == 'SERVICIO':
            if oferta.precio is not None:
                precio_mostrar = f"${oferta.precio:,.0f} CLP"
        elif oferta.tipo == 'DESCUENTO':
            if oferta.porcentaje_descuento is not None:
                precio_mostrar = f"{oferta.porcentaje_descuento}% OFF"

        # Obtener la URL del logo de la empresa
        logo_filename = f"{empresa_nombre}.png"
        logo_path = os.path.join('static', 'images', 'logos_de_empresas', logo_filename)
        full_logo_path = os.path.join(current_app.root_path, logo_path)
        
        if os.path.exists(full_logo_path):
            logo_url = url_for('static', filename=f'images/logos_de_empresas/{logo_filename}')
        else:
            logo_url = '/api/placeholder/200/200'


        tipo_oferta = oferta.tipo.value if hasattr(oferta.tipo, 'value') else str(oferta.tipo).split('.')[-1].capitalize()

        ofertas_procesadas.append({
            'id': oferta.id,
            'titulo': oferta.titulo,
            'descripcion': oferta.descripcion or "",
            'precio_mostrar': precio_mostrar,
            'tipo': tipo_oferta,
            'empresa': empresa_nombre,
            'logo_url': logo_url,
        })

    return render_template('ofertas.html', 
                         ofertas=ofertas_procesadas, 
                         pagination=pagination,
                         tipo_actual=tipo,
                         search=search)



@main_bp.route("/nosotros")
def nosotros():
    return render_template('about.html')

# @main_bp.route('/empresa_dashboard')
# @login_required
# def empresa_dashboard():
#     return render_template('empresa_dashboard.html')

@main_bp.route('/Bienvenido/<nombre>')
def Bienvenida_nombre(nombre):
    return f'!Bienvenid@, {nombre}'

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
    per_page = 10  # Número de empresas por página

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
        'empresas.html',
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
        'perfil_empresa.html', 
        empresa=empresa, 
        ubicaciones=ubicaciones, 
        api_key=api_key,
        ofertas=ofertas)