from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from Glooba import db
from .forms.admin_forms import AdminProfileForm
from .forms.empresa_forms import EmpresaProfileForm
from .forms.usuario_forms import UsuarioProfileForm
import os
from werkzeug.utils import secure_filename

perfil_bp = Blueprint('perfil', __name__, template_folder='templates')

@perfil_bp.before_app_request
def setup_upload_folder():
    # Configuración de la carpeta base de subida
    current_app.config['UPLOAD_FOLDER'] = os.path.join(current_app.root_path, 'static/uploads')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def generar_ruta_imagen(usuario, tipo_imagen):
    """
    Genera una ruta para guardar imágenes organizada por:
    - Tipo de usuario
    - Nombre de usuario
    - Tipo de imagen
    """
    # Determinar el tipo de usuario
    tipo_usuario = usuario.__class__.__name__.lower()

    # Asegurarse de que el nombre del usuario sea válido para un sistema de archivos
    nombre_usuario = secure_filename(usuario.nombre)

    # Crear la ruta completa
    ruta = os.path.join(
        current_app.config['UPLOAD_FOLDER'],
        'profile',
        tipo_usuario,
        nombre_usuario,
        'picture',
        tipo_imagen
    )

    # Crear directorios si no existen
    os.makedirs(ruta, exist_ok=True)

    return ruta


@perfil_bp.route('/')
@login_required
def ver_perfil():
    return render_template('view_profile.html')

@perfil_bp.route('/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    if current_user.__class__.__name__ == 'CommonUser':
        form = UsuarioProfileForm()
    elif current_user.__class__.__name__ == 'Empresa':
        form = EmpresaProfileForm()
    else:
        form = AdminProfileForm()

    if request.method == 'GET':
        for field in form:
            if hasattr(current_user, field.name):
                field.data = getattr(current_user, field.name)

    if form.validate_on_submit():
        try:
            # Procesar y guardar las imágenes del formulario
            for field_name, tipo_imagen in [
                ('imagen_perfil', 'perfil'),
                ('imagen_principal', 'principal'),
                ('imagen_secundaria_arriba', 'secundaria_arriba'),
                ('imagen_secundaria_abajo', 'secundaria_abajo')
            ]:
                field = getattr(form, field_name, None)
                if field and field.data:
                    file = field.data
                    filename = secure_filename(file.filename)
                    
                    # Generar la ruta dinámica
                    ruta_directorio = generar_ruta_imagen(current_user, tipo_imagen)
                    filepath = os.path.join(ruta_directorio, filename)
                    
                    # Guardar el archivo en la ruta generada
                    file.save(filepath)

                    # Eliminar la imagen anterior si existe
                    old_image = getattr(current_user, field_name, None)
                    if old_image:
                        old_image_path = os.path.join(ruta_directorio, old_image)
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)

                    # Actualizar el atributo en el modelo
                    setattr(current_user, field_name, filename)

            # Actualizar los demás datos del formulario
            for field in form:
                if hasattr(current_user, field.name) and field.name not in ['imagen_perfil', 'imagen_principal', 'imagen_secundaria_arriba', 'imagen_secundaria_abajo']:
                    setattr(current_user, field.name, field.data)

            db.session.commit()
            flash('Perfil actualizado correctamente', 'success')
            return redirect(url_for('perfil.view_profile'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el perfil: {str(e)}', 'error')

    return render_template('edit_profile.html', form=form)

