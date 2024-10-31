import os
from Glooba import create_app

# Obtener el entorno de una variable de ambiente, por defecto producción
environment = os.environ.get('FLASK_ENV', 'production')
app = create_app(environment)

if __name__ == '__main__':
    app.run()