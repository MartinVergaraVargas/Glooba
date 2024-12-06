# Glooba - Plataforma de Ofertas Sustentables

## 📝 Descripción
Fork de appCalcu hecho para el nivel de produccion de la web app final.

Glooba es una aplicación web que conecta a consumidores con empresas comprometidas con la sustentabilidad, permitiendo a las empresas publicar y gestionar ofertas de productos/servicios sustentables y a los usuarios encontrar estas ofertas cerca de su ubicación.

## 🌟 Características Principales
- Sistema de autenticación para múltiples tipos de usuarios (común, empresa, administrador)
- Geolocalización de tiendas mediante Google Maps
- Sistema de gestión de ofertas sustentables
- Dashboard administrativo para gestión de empresas
- Sistema de favoritos para usuarios
- Control de stock por ubicación

## 🛠️ Tecnologías Utilizadas
- Python 3.x
- Flask (Framework web)
- PostgreSQL (Base de datos)
- SQLAlchemy (ORM)
- Google Maps API
- Nginx (Servidor web)
- Certbot (Certificados SSL)

## ⚙️ Requisitos del Sistema
- Python 3.x
- PostgreSQL
- pip (Python package installer)
- Navegador web moderno
- Conexión a Internet

## 📦 Instalación

1. Clonar el repositorio
```bash
git clone https://github.com/MartinVergaraVargas/Glooba
cd glooba
```

2. Crear y activar entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno
```bash
cp .env.example .flaskenv
# Editar .env con tus configuraciones
```

5. Inicializar la base de datos
```bash
flask db upgrade
```

## 🚀 Uso
1. Iniciar el servidor de desarrollo
```bash
flask run
```

2. Abrir el navegador y visitar:
```
http://localhost:5000
```

## 👥 Tipos de Usuario
1. Usuario Común
   - Puede ver ofertas
   - Marcar favoritos
   - Ver ubicaciones en el mapa

2. Usuario Empresa
   - Gestionar ofertas
   - Administrar ubicaciones
   - Ver estadísticas

3. Administrador
   - Gestionar empresas
   - Moderar contenido
   - Administrar sistema

## 📝 Estructura del Proyecto
```
├── archivos_csv
│   ├── credenciales_empresas_20241029_144118.csv
│   ├── empresas_creadas_20241029_144118.csv
│   └── empresas_fallidas_20241029_144118.csv
├── create_admin.py
├── delete_user.py
├── deployment
│   └── glooba.service.example
├── Glooba
│   ├── blueprints
│   │   ├── administracion
│   │   │   ├── administracion.py
│   │   │   ├── forms
│   │   │   │   ├── adminForms_empresa.py
│   │   │   │   └── adminForms_usuario.py
│   │   │   └── templates
│   │   │       ├── actividad_dashboard.html
│   │   │       ├── crear_admin.html
│   │   │       ├── manejo_de_empresas
│   │   │       │   ├── gestionar_empresas.html
│   │   │       │   ├── manejo_de_ofertas
│   │   │       │   │   ├── crear_oferta.html
│   │   │       │   │   ├── editar_oferta.html
│   │   │       │   │   └── lista_ofertas.html
│   │   │       │   ├── manejo_de_ubicaciones
│   │   │       │   │   ├── crear_ubicacion.html
│   │   │       │   │   ├── editar_ubicacion.html
│   │   │       │   │   └── lista_ubicaciones.html
│   │   │       │   └── registrar_empresa.html
│   │   │       └── manejo_de_usuarios
│   │   │           ├── add_user.html
│   │   │           ├── edit_user.html
│   │   │           └── usuarios.html
│   │   ├── auth
│   │   │   ├── auth.py
│   │   │   ├── forms
│   │   │   │   └── log_forms.py
│   │   │   └── templates
│   │   │       ├── login.html
│   │   │       └── signup.html
│   │   ├── calculadora
│   │   │   └── calculadora.py
│   │   ├── dashboard_empresa
│   │   │   ├── empresa_dashboard.py
│   │   │   ├── forms
│   │   │   │   ├── oferta_forms.py
│   │   │   │   └── ubicacion_forms.py
│   │   │   └── templates
│   │   │       ├── empresa_dashboard.html
│   │   │       ├── ofertas
│   │   │       │   ├── crear_oferta.html
│   │   │       │   ├── editar_oferta.html
│   │   │       │   └── lista_ofertas.html
│   │   │       └── ubicaciones
│   │   │           ├── crear_ubicacion.html
│   │   │           ├── editarubicacion.html
│   │   │           └── lista_ubicaciones.html
│   │   ├── main
│   │   │   ├── main.py
│   │   │   └── templates
│   │   │       ├── about.html
│   │   │       ├── bienvenida.html
│   │   │       ├── empresas.html
│   │   │       ├── home.html
│   │   │       ├── pagina_empresas.html
│   │   │       └── pagina_principal.html
│   │   ├── mapa
│   │   │   ├── forms
│   │   │   │   └── mapa_forms.py
│   │   │   ├── __init__.py
│   │   │   ├── mapa.py
│   │   │   │   └── mapa.cpython-311.pyc
│   │   │   └── templates
│   │   │       └── mapa.html
│   │   └── perfil
│   │       ├── forms
│   │       │   ├── admin_forms.py
│   │       │   ├── empresa_forms.py
│   │       │   └── usuario_forms.py
│   │       ├── perfil.py
│   │       └── templates
│   │           ├── editar_perfil.html
│   │           └── ver_perfil.html
│   ├── config.py
│   ├── __init__.py
│   ├── models.py
│   ├── original__init__.py
│   ├── roughModels.py
│   ├── static
│   │   ├── css
│   │   │   ├── bienvenida.css
│   │   │   ├── estilo.css
│   │   │   └── mapa.css
│   │   ├── images
│   │   │   ├── equipo
│   │   │   │   └── IMG_5115.jpg
│   │   │   ├── flavicon.ico
│   │   │   ├── guy_smiling.jpg
│   │   │   ├── logo.png
│   │   │   └── logos_de_empresas
│   │   │       └── empresa_logo.png
│   │   └── js
│   │       └── main.js
│   └── templates
│       ├── dashboard-base.html
│       ├── layout.html
│       └── log-base.html
├── Informe de requisitos - Memoria de título.pdf
├── README.md
├── requerimientos.txt
├── test_db.py
└── wsgi.py
```

## 🔒 Seguridad
- Autenticación robusta
- Encriptación de contraseñas
- Protección CSRF
- Certificados SSL

## 🙏 Agradecimientos
- Javier Alvarado San Feliú (Tutor)
- Fabio Durán Verdugo (Profesor Informante)
- Universidad de Talca