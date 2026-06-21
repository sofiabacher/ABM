create table sucursales(
	id_sucursal int auto_increment primary key,
    nombre varchar(100) not null,
    direccion varchar(200) not null,
    ciudad varchar(100) not null,
    provincia varchar(100) not null,
    telefono varchar(100) not null,
    email varchar(150) not null unique,
    estado boolean default true
);

create table categorias(
	id_categoria int auto_increment primary key,
    nombre varchar(100) not null unique,
    descripcion text(200)
);

create table usuarios(
	id_usuario int auto_increment primary key,
    nombre varchar(100) not null,
    apellido varchar(100) not null,
    email varchar(150) not null unique,
    password varchar(255) not null,
    rol enum('ADMIN', 'VENTAS', 'COMPRAS', 'CONSULTA') not null,
    estado boolean default true,
    
    id_sucursal int not null,
	foreign key(id_sucursal) references sucursales(id_sucursal)
);

create table clientes(
	id_cliente int auto_increment primary key,
    nombre varchar(100) not null,
    apellido varchar(100) not null,
    dni varchar(20) not null unique,
    telefono varchar(30) not null,
    email varchar(150) not null unique,
    direccion varchar(200) not null,
    fecha_alta datetime default current_timestamp,
    estado boolean default true
);

create table proveedores(
	id_proveedor int auto_increment primary key,
    razon_social varchar(100) not null,
    cuit varchar(20) not null unique,
    email varchar(150) not null unique,
    telefono varchar(30) not null,
    provincia varchar(100) not null,
    direccion varchar(200) not null,
    fecha_alta datetime default current_timestamp,
    estado boolean default true
);

create table productos(
	id_producto int auto_increment primary key,
    codigo varchar(50) not null unique,
    nombre varchar(100) not null,
    descripcion text,
    talle varchar(20),
    color varchar(50),
    precio_compra decimal(10, 2) not null,
    precio_venta decimal(10, 2) not null,
    stock_actual int default 0,
    stock_minimo int default 0,
    estado boolean default true,
    
    id_categoria int not null,  
    foreign key(id_categoria) references categorias(id_categoria)
);

create table compras(
	id_compra int auto_increment primary key, 
    fecha datetime default current_timestamp,
    num_comprobante varchar(50),
    total decimal(12, 2) not null,
    
    id_proveedor int not null,
    id_usuario int not null,
    id_sucursal int not null,
    
    foreign key(id_proveedor) references proveedores(id_proveedor),
    foreign key(id_usuario) references usuarios(id_usuario),
    foreign key(id_sucursal) references sucursales(id_sucursal)
);

create table ventas(
	id_venta int auto_increment primary key, 
    fecha datetime default current_timestamp,
    metodo_pago enum('EFECTIVO', 'DEBITO', 'CREDITO','TRANSFERENCIA') not null,
    total decimal(12, 2) not null,
    
    id_cliente int not null,
    id_usuario int not null,
	id_sucursal int not null,
    
    foreign key(id_cliente) references clientes(id_cliente),
    foreign key(id_usuario) references usuarios(id_usuario),
    foreign key(id_sucursal) references sucursales(id_sucursal)
);

create table detalle_compra(
	id_detalle_compra int auto_increment primary key, 
    cantidad int not null,
    precio_unitario decimal(10, 2) not null,
    subtotal decimal(10, 2) not null,
    
    id_compra int not null,
    id_producto int not null,
    
    foreign key(id_compra) references compras(id_compra),
    foreign key(id_producto) references productos(id_producto)
);

create table detalle_venta(
	id_detalle_venta int auto_increment primary key, 
    cantidad int not null,
    precio_unitario decimal(10, 2) not null,
    subtotal decimal(10, 2) not null,
    
    id_venta int not null,
    id_producto int not null,
    
    foreign key(id_venta) references ventas(id_venta),
    foreign key(id_producto) references productos(id_producto)
);

create table facturas(
	id_factura int auto_increment primary key,
    num_factura varchar(50) not null unique, 
    tipo_factura enum('A', 'B', 'C') not null,
    fecha_emision datetime default current_timestamp,
    subtotal decimal(12, 2) not null,
    impuestos decimal(12, 2) not null,
    total decimal(12, 2) not null,
    estado enum('EMITIDA', 'ANULADA') default 'EMITIDA',
    
    id_venta int not null,
    foreign key(id_venta) references ventas(id_venta)
);

create table bitacora(
	id_bitacora int auto_increment primary key,
    accion varchar(100) not null,
    tabla_afectada varchar(100) not null,
    descripcion text,
    fecha_hora datetime default current_timestamp,
    
    id_usuario int not null,
    foreign key(id_usuario) references usuarios(id_usuario)
);
