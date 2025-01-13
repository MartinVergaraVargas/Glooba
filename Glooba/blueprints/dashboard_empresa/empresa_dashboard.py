from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, current_app
from flask_login import login_required, current_user
from Glooba.models import db, Empresa, Oferta, Ubicacion
from datetime import datetime
from werkzeug.security import generate_password_hash
from .forms.oferta_forms import OfertaForm
from .forms.ubicacion_forms import UbicacionForm
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os

empresa_bp = Blueprint('empresa', __name__, template_folder='templates')

@empresa_bp.before_app_request
def setup_upload_folder():
    current_app.config['UPLOAD_FOLDER'] = os.path.join(current_app.root_path, 'static/uploads')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def generar_ruta_imagen(empresa, tipo_imagen):
    """
    Genera una ruta para guardar imágenes organizada por:
    - Empresa
    - Tipo de imagen
    """
    nombre_empresa = secure_filename(empresa.nombre)

    ruta = os.path.join(
        current_app.config['UPLOAD_FOLDER'],
        'profile',
        'empresa',
        nombre_empresa,
        'picture',
        tipo_imagen
    )

    os.makedirs(ruta, exist_ok=True)

    return ruta


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@empresa_bp.route('/ofertas')
@login_required
def ofertas():
    if not isinstance(current_user, Empresa):
        flash('No tienes permisos para acceder a esta página', 'error')
        return redirect(url_for('main.index'))

    ofertas_query = Oferta.query.filter_by(empresa_id=current_user.id).order_by(Oferta.fecha_inicio.desc()).all()

    ofertas_procesadas = []
    for oferta in ofertas_query:
        ofertas_procesadas.append({
            'id': oferta.id,
            'titulo': oferta.titulo,
            'precio': oferta.precio,
            'porcentaje_descuento': oferta.porcentaje_descuento,
            'fecha_inicio': oferta.fecha_inicio,
            'fecha_fin': oferta.fecha_fin
        })

    return render_template('ofertas/gestionar_ofertas.html', ofertas=ofertas_procesadas)


@empresa_bp.route('/nueva_oferta', methods=['GET', 'POST'])
@login_required
def nueva_oferta():
    if not isinstance(current_user, Empresa):
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('main.index'))

    form = OfertaForm()

    if form.validate_on_submit():
        try:
            nueva_oferta = Oferta(
                titulo=form.titulo.data,
                descripcion=form.descripcion.data,
                precio=form.precio.data,
                es_descuento=form.es_descuento.data,
                porcentaje_descuento=form.porcentaje_descuento.data if form.es_descuento.data else None,
                fecha_fin=form.fecha_fin.data,
                sitio_web=form.sitio_web.data,  
                empresa_id=current_user.id
            )

            # Manejo de imagen
            if form.imagen.data and allowed_file(form.imagen.data.filename):
                file = form.imagen.data
                filename = secure_filename(file.filename)

                ruta_directorio = generar_ruta_imagen(current_user, 'oferta')
                filepath = os.path.join(ruta_directorio, filename)
                file.save(filepath)

                nueva_oferta.imagen = filename

            db.session.add(nueva_oferta)
            db.session.commit()
            flash('Oferta creada exitosamente', 'success')
            return redirect(url_for('empresa.ofertas'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la oferta: {str(e)}', 'error')

    return render_template('ofertas/nueva_oferta.html', form=form)


@empresa_bp.route('/editar_oferta/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_oferta(id):
    if not isinstance(current_user, Empresa):
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('main.index'))

    oferta = Oferta.query.get_or_404(id)

    if oferta.empresa_id != current_user.id:
        flash('No tienes permisos para editar esta oferta', 'error')
        return redirect(url_for('empresa.ofertas'))

    form = OfertaForm(obj=oferta)

    if form.validate_on_submit():
        try:
            oferta.titulo = form.titulo.data
            oferta.descripcion = form.descripcion.data
            oferta.precio = form.precio.data
            oferta.es_descuento = form.es_descuento.data
            oferta.porcentaje_descuento = form.porcentaje_descuento.data if form.es_descuento.data else None
            oferta.fecha_fin = form.fecha_fin.data
            oferta.sitio_web = form.sitio_web.data

            # Manejo de imagen
            if form.imagen.data and isinstance(form.imagen.data, FileStorage):
                if allowed_file(form.imagen.data.filename):
                    file = form.imagen.data
                    filename = secure_filename(file.filename)

                    ruta_directorio = generar_ruta_imagen(current_user, 'oferta')
                    filepath = os.path.join(ruta_directorio, filename)
                    file.save(filepath)

                    oferta.imagen = filename
            else:
                oferta.imagen = oferta.imagen  # Mantén la imagen actual

            db.session.commit()
            flash('Oferta actualizada exitosamente', 'success')
            return redirect(url_for('empresa.ofertas'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la oferta: {str(e)}', 'error')


    return render_template('ofertas/editar_oferta.html', form=form, oferta=oferta)


@empresa_bp.route('/eliminar_oferta/<int:id>', methods=['DELETE'])
@login_required
def eliminar_oferta(id):
    if not isinstance(current_user, Empresa):
        return jsonify({'success': False, 'error': 'No tienes permisos para realizar esta acción'})

    oferta = Oferta.query.get_or_404(id)

    if oferta.empresa_id != current_user.id:
        return jsonify({'success': False, 'error': 'No tienes permisos para eliminar esta oferta'})

    try:
        db.session.delete(oferta)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@empresa_bp.route('/ubicaciones')
@login_required
def ubicaciones():
    if not isinstance(current_user, Empresa):
        flash('No tienes permisos para acceder a esta página', 'error')
        return redirect(url_for('main.index'))
    
    ubicaciones = Ubicacion.query.filter_by(empresa_id=current_user.id).all()
    return render_template('ubicaciones/lista_ubicaciones.html', ubicaciones=ubicaciones)


@empresa_bp.route('/nueva_ubicacion', methods=['GET', 'POST'])
@login_required
def crear_ubicacion():
    api_key = current_app.config['GOOGLE_MAPS_API_KEY']
    form = UbicacionForm()
    empresa_id = current_user.id
    empresa_nombre = current_user.nombre
    
    if not isinstance(current_user, Empresa):
        flash('No tienes permisos para realizar estaacción', 'error')
        return redirect(url_for('main.index'))

    if form.validate_on_submit():
        try:
            crear_ubicacion = Ubicacion(
                nombre=form.nombre.data,
                latitud=form.latitud.data,
                longitud=form.longitud.data,
                direccion=form.direccion.data,
                ciudad=form.ciudad.data,
                region=form.pais.data,
                es_propia=form.es_propia.data,
                activa=True,
                empresa_id=empresa_id,
                descripcion=form.descripcion.data
            )
            db.session.add(crear_ubicacion)
            db.session.commit()
            flash('Ubicación creada exitosamente.', 'success')
            return redirect(url_for('empresa.ubicaciones'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la ubicación: {str(e)}', 'error')
            return redirect(url_for('empresa.crear_ubicacion'))

    return render_template('ubicaciones/crear_ubicacion.html', form=form, \
        empresa_nombre=empresa_nombre, api_key=api_key)


@empresa_bp.route('/editar_ubicacion/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_ubicacion(id):
    if not isinstance(current_user, Empresa):
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('main.index'))
    
    api_key = current_app.config['GOOGLE_MAPS_API_KEY']
    empresa_nombre = current_user.nombre
    ubicacion = Ubicacion.query.get_or_404(id)

    form = UbicacionForm(obj=ubicacion)

    if form.validate_on_submit():
        ubicacion.nombre = form.nombre.data
        ubicacion.latitud = form.latitud.data
        ubicacion.longitud = form.longitud.data
        ubicacion.direccion = form.direccion.data
        ubicacion.ciudad = form.ciudad.data
        ubicacion.region = form.pais.data
        ubicacion.es_propia = form.es_propia.data
        ubicacion.descripcion = form.descripcion.data
        db.session.commit()
        flash('Ubicación editada exitosamente', 'success')
        return redirect(url_for('empresa.ubicaciones'))

    return render_template('ubicaciones/editar_ubicacion.html', form=form, ubicacion=ubicacion, \
        api_key=api_key, empresa_nombre=empresa_nombre)

@empresa_bp.route('/eliminar_ubicacion/<int:id>', methods=['DELETE'])
@login_required
def eliminar_ubicacion(id):
    if not isinstance(current_user, Empresa):
        return jsonify({'success': False, 'error': 'No tienes permisos para realizar esta acción'})

    ubicacion = Ubicacion.query.get_or_404(id)
    
    try:
        db.session.delete(ubicacion)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})