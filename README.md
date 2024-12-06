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
git clone https://github.com/tuusuario/glooba.git
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
glooba/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   ├── static/
│   └── templates/
├── migrations/
├── tests/
├── venv/
├── config.py
├── requirements.txt
└── README.md
```

## 🔒 Seguridad
- Autenticación robusta
- Encriptación de contraseñas
- Protección CSRF
- Certificados SSL

## 🤝 Contribuir
1. Fork el proyecto
2. Crear rama de características (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia
Este proyecto está bajo la Licencia [NOMBRE_LICENCIA] - ver el archivo [LICENSE.md](LICENSE.md) para detalles.

## ✉️ Contacto
Martin Vergara - [@twitter_handle](https://twitter.com/twitter_handle)
Link del Proyecto: [https://github.com/tuusuario/glooba](https://github.com/tuusuario/glooba)

## 🙏 Agradecimientos
- Javier Alvarado San Feliú (Tutor)
- Fabio Durán Verdugo (Profesor Informante)
- Universidad de Talca