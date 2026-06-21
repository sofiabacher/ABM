insert ignore into sucursales (nombre, direccion, ciudad, provincia, telefono, email)
    values ('Casa Central', 'Av. Corrientes 1234', 'La Plata', 'Buenos Aires', '1145678900', 'central@industrialdelsur.com');

insert ignore into categorias (nombre, descripcion)
    values  ('Remeras', 'Prendas superiores'),
            ('Pantalones', 'Prendas inferiores'),
            ('Camperas', 'Prendas de abrigo'),
            ('Buzos', 'Prendas deportivas'),
            ('Accesorios', 'Complementos textiles');

insert ignore into usuarios (nombre, apellido, email, password, rol, id_sucursal)
    values ('Administrador', 'General', 'admin@industrialdelsur.com', 'admin_temporal', 'ADMIN', 1);