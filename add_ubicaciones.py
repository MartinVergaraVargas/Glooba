from Glooba import db
from Glooba.models import Ubicacion, Empresa

def add_sample_locations():
    """
    Agrega ubicaciones de ejemplo para las empresas existentes en la base de datos.
    """
    # Lista de ubicaciones de ejemplo en Talca y alrededores
    sample_locations = [
        {
            'nombre': 'Tienda Central',
            'latitud': -35.4264,
            'longitud': -71.6553,
            'direccion': '1 Sur 1234',
            'ciudad': 'Talca',
            'region': 'Maule',
            'es_propia': True
        },
        {
            'nombre': 'Sucursal Mall',
            'latitud': -35.4284,
            'longitud': -71.6673,
            'direccion': 'Av. San Miguel 3333',
            'ciudad': 'Talca',
            'region': 'Maule',
            'es_propia': True
        },
        {
            'nombre': 'Local Curicó',
            'latitud': -34.9854,
            'longitud': -71.2395,
            'direccion': 'Calle Merced 567',
            'ciudad': 'Curicó',
            'region': 'Maule',
            'es_propia': False
        },
        {
            'nombre': 'Punto de Venta Linares',
            'latitud': -35.8466,
            'longitud': -71.5927,
            'direccion': 'Independencia 890',
            'ciudad': 'Linares',
            'region': 'Maule',
            'es_propia': False
        }
    ]

    try:
        # Obtener todas las empresas activas
        empresas = Empresa.query.filter_by(activo=True).all()
        
        if not empresas:
            print("No hay empresas activas en la base de datos.")
            return
        
        # Distribuir las ubicaciones entre las empresas existentes
        for i, empresa in enumerate(empresas):
            # Asignar una ubicación a cada empresa
            location_data = sample_locations[i % len(sample_locations)].copy()
            location_data['empresa_id'] = empresa.id
            
            # Verificar si la ubicación ya existe
            existing_location = Ubicacion.query.filter_by(
                latitud=location_data['latitud'],
                longitud=location_data['longitud'],
                empresa_id=empresa.id
            ).first()
            
            if not existing_location:
                nueva_ubicacion = Ubicacion(**location_data)
                db.session.add(nueva_ubicacion)
                print(f"Agregada ubicación '{location_data['nombre']}' para empresa '{empresa.nombre}'")
        
        db.session.commit()
        print("Ubicaciones agregadas exitosamente")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error al agregar ubicaciones: {str(e)}")

if __name__ == '__main__':
    add_sample_locations()