import sqlite3
import hashlib
import inspect
from datetime import datetime
from zoneinfo import ZoneInfo
import functools
import sqlite3, csv

class Product:
    def __init__(self, name:str, price:int, brand:str, size:any, category:str, description:str, branch_name:str, stock:int, category_path=None, id:int=None):
        self.id = id
        self.name = name
        self.price = price
        self.brand = brand
        self.size = size
        self.stock = stock
        self.category = category
        self.description = description
        self.branch_name = branch_name

    @classmethod
    def from_row(cls, row)->tuple:
        # Crea una instancia de Product a partir de una fila de la base de datos
        return cls(
            id=row[0],
            name=row[1],
            price=row[2],
            brand=row[3],
            size=row[4],
            category=row[5],  
            description=row[6],
            branch_name=row[7],
            stock=row[8],
        )

dataBasePath = './Bd/clothing_store.db'

def create_database()->None:
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    # Creación de tablas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Branches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        address TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Roles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role_id INTEGER NOT NULL,
        branch_id INTEGER,
        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (role_id) REFERENCES Roles(id),
        FOREIGN KEY (branch_id) REFERENCES Branches(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        brand TEXT NOT NULL,
        size TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        branch_name TEXT NOT NULL,
        stock INTEGER DEFAULT 0,
        FOREIGN KEY (branch_name) REFERENCES Branches(name)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        branch_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        price INTEGER NOT NULL,
        category TEXT NOT NULL,
        FOREIGN KEY (category) REFERENCES products (category)
        FOREIGN KEY (product_id) REFERENCES Products(id),
        FOREIGN KEY (user_id) REFERENCES Users(id),
        FOREIGN KEY (branch_name) REFERENCES Branches(name)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Restocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        branch_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES Products(id),
        FOREIGN KEY (user_id) REFERENCES Users(id),
        FOREIGN KEY (branch_name) REFERENCES Branches(name)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT NOT NULL,
        user_id INTEGER,
        product_id INTEGER,
        branch_name TEXT,
        quantity INTEGER,
        price INTEGER,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(id),
        FOREIGN KEY (product_id) REFERENCES Products(id),
        FOREIGN KEY (branch_name) REFERENCES Branches(name)
    )
    ''')

    # Inserta roles por default
    cursor.execute('INSERT OR IGNORE INTO Roles (name) VALUES (?)', ('Normal User',))
    cursor.execute('INSERT OR IGNORE INTO Roles (name) VALUES (?)', ('Admin',))
    cursor.execute('INSERT OR IGNORE INTO Roles (name) VALUES (?)', ('General Admin',))

    # Inserta sucursales de ejemplo
    cursor.execute('INSERT OR IGNORE INTO Branches (name, address) VALUES (?, ?)', ('San miguel', '202'))
    cursor.execute('INSERT OR IGNORE INTO Branches (name, address) VALUES (?, ?)', ('Jose c paz', '197'))
    cursor.execute('INSERT OR IGNORE INTO Branches (name, address) VALUES (?, ?)', ('Retiro', 'LA general pa'))

    conn.commit()
    conn.close()

    print("Database creada.")

def log_action(action: str, user_id: int = None, product_id: int = None, branch_name: str = None, quantity: int = None, price: int = None) -> None:
    """
    Registra una acción en la tabla de Logs.
    :param action: Acción realizada ('Sale', 'Restock', 'Add Product', 'Register User', etc.)
    :param user_id: ID del usuario que realiza la acción (opcional).
    :param product_id: ID del producto afectado (opcional).
    :param branch_name: Nombre de la sucursal afectada (opcional).
    :param quantity: Cantidad de productos afectados (opcional).
    :param price: Precio de la transacción, si aplica (opcional).
    """
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO Logs (action, user_id, product_id, branch_name, quantity, price)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (action, user_id, product_id, branch_name, quantity, price))
    
    conn.commit()
    conn.close()

def log_database_action(action: str):
    """
    Decorador que registra una acción en la tabla Logs.
    :param action: Acción realizada ('Sale', 'Restock', 'Add Product', 'Register User', etc.)
    """
    def decorator_log(func):
        @functools.wraps(func)
        def wrapper_log(*args, **kwargs):
            # Ejecutar la función original y obtener su resultado
            result = func(*args, **kwargs)

            # Obtener los nombres de los argumentos de la función
            signature = inspect.signature(func)
            bound_args = signature.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # Extraer los valores de interés
            user_id = bound_args.arguments.get('user_id')
            product_id = bound_args.arguments.get('product_id')
            branch_name = bound_args.arguments.get('branch_name')
            quantity = bound_args.arguments.get('quantity')
            price = bound_args.arguments.get('price')

            # Registrar la acción
            log_action(action, user_id=user_id, product_id=product_id, branch_name=branch_name, quantity=quantity, price=price)

            return result
        return wrapper_log
    return decorator_log

@log_database_action("Register User")
def register_user(name:str, email:str, password:str, role_id:str, branch_name:str) -> str:
    if branch_exists(branch_name):
        conn = sqlite3.connect(dataBasePath)
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM Users WHERE email = ?', (email,))
        if cursor.fetchone() is not None:
            print("Error: ya existe un usuario con este email.")
            conn.close()
            return "Error: ya existe un usuario con este email."

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute('''
        INSERT INTO Users (name, email, password, role_id, branch_id)
        VALUES (?, ?, ?, ?, ?)
        ''', (name, email, hashed_password, role_id, branch_name))

        conn.commit()
        conn.close()

        return(f"Usuario {name} registrado.")
    else:
        print(f"La sucursal '{branch_name}' no existe.")
        
def get_user_id(email:str)->None:
    '''
    Obtiene el ID de un usuario a partir de su email.
    '''
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT id FROM Users WHERE email = ?
    ''', (email,))
    
    user_id = cursor.fetchone()
    conn.close()
    
    return user_id[0] if user_id else None

@log_database_action("Add product")
def add_product(product)->None:
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO Products (name, price, brand, size, category, description, branch_name, stock)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (product.name, product.price, product.brand, product.size, product.category, product.description, product.branch_name, product.stock))
    
    conn.commit()
    conn.close()

    print(f"Product {product.name} added successfully.")
    
def get_product_category(id_product:int)->str:
    '''
    Obtiene la categoría de un producto a partir de su ID.
    '''
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT category FROM Products WHERE id = ?
    ''', (id_product,))
    
    category = cursor.fetchone()
    conn.close()
    
    return category[0] if category else None

@log_database_action("Sale")
def record_sale(product_id:int, user_id:int, branch_name:str, quantity:int, price:int)->bool:
    '''
    Guarda una venta de un producto y reduce el stock del producto.
    '''
    if branch_exists(branch_name):
        conn = sqlite3.connect(dataBasePath)
        cursor = conn.cursor()

        # Verifica el stock actual
        cursor.execute('SELECT stock FROM Products WHERE id = ?', (product_id,))
        current_stock = cursor.fetchone()[0]

        print(quantity)
        print(current_stock)

        if current_stock >= quantity:
            # Registra la venta
            cursor.execute('''
            INSERT INTO Sales (product_id, user_id, branch_name, quantity, price, category)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (product_id, user_id, branch_name, quantity, price, get_product_category(product_id)))

            # Reduce el stock
            new_stock = current_stock - quantity
            cursor.execute('UPDATE Products SET stock = ? WHERE id = ?', (new_stock, product_id))

            conn.commit()
            conn.close()
            print(f"Venta guardada .Stock: {new_stock}")
            return True
        else:
            print("Error: No hay suficiente stock.")
            return False
    else:
        print(f"La sucursal '{branch_name}' no existe.")
        
def get_products_out_of_stock()->dict:
    """
    Recupera los productos que no tienen stock disponible.
    """
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT p.id, p.name, p.branch_name, p.stock FROM Products p
    WHERE p.stock = 0
    ''')
    
    products_out_of_stock = cursor.fetchall()
    conn.close()

    return products_out_of_stock

@log_database_action('Restock')
def record_restock(product_id:int, user_id:int, branch_name:str, quantity:int)->None:
    # sourcery skip: remove-unnecessary-cast
    '''
    Guarda el reestock de un producto
    '''
    if branch_exists(branch_name):
        conn = sqlite3.connect(dataBasePath)
        cursor = conn.cursor()

        cursor.execute('SELECT stock FROM Products WHERE id = ?', (product_id,))
        current_stock = cursor.fetchone()[0]
        new_stock = int(current_stock) + int(quantity)

        cursor.execute('UPDATE Products SET stock = ? WHERE id = ?', (new_stock, product_id))
        cursor.execute('''
        INSERT INTO Restocks (product_id, user_id, branch_name, quantity, date)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (product_id, user_id, branch_name, quantity))

        conn.commit()
        conn.close()
    else:
        print(f"La sucursal '{branch_name}' no existe.")
    
def get_products_in_stock() -> dict:
    """
    Recupera los productos en stock y los devuelve como una lista de Product.
    """
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT * FROM Products
    ''')

    rows = cursor.fetchall()
    conn.close()

    return [Product.from_row(row) for row in rows]

def get_user_details(user_id: int) -> tuple:
    '''
    Obtiene detalles de un usuario junto con su sucursal asociada
    '''
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT Users.email, Roles.name as role, Users.password, Branches.name as branch
    FROM Users
    LEFT JOIN Roles ON Users.role_id = Roles.id
    LEFT JOIN Branches ON Users.branch_id = Branches.name
    WHERE Users.id = ?
    ''', (user_id,))

    user_details = cursor.fetchone()
    conn.close()
    
    return user_details

def get_record_from_table(table_name, columns='*', **kwargs:str) -> any:
    """
    Recupera registros de una tabla específica basada en los filtros proporcionados.
    :param table_name: str, nombre de la tabla
    :param columns: str o list, columnas a seleccionar (por defecto todas)
    :param kwargs: dict, condiciones para filtrar los resultados
    :return: list, registros que coinciden con los filtros
    """
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    # Construye la parte de selección de columnas
    columns_str = ', '.join(columns) if isinstance(columns, list) else columns
    # Construye la parte de condiciones de la consulta
    conditions = []
    values = []
    for key, value in kwargs.items():
        conditions.append(f"{key} = ?")
        values.append(value)

    conditions_str = " AND ".join(conditions) if conditions else "1=1"

    # Query dinámica
    query = f"SELECT {columns_str} FROM {table_name} WHERE {conditions_str}"

    cursor.execute(query, values)
    records = cursor.fetchall()
    conn.close()

    return records

def get_name_product(id:int)->str:
    '''
    Obtiene el nombre del producto a traves de la id
    '''
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    cursor.execute('SELECT name FROM Products WHERE id = ?', (id,))

    name = cursor.fetchone()[0]
    conn.close()
    return name
    
def get_price_product(id:int)->str:
    '''
    Obtiene los precios de el producto mediante la id
    '''
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    cursor.execute('SELECT price FROM Products WHERE id = ?', (id,))

    price = cursor.fetchone()[0]
    conn.close()
    return price

def get_stock_product(id:int)->str:
    '''
    Obtiene todos los productos en stock
    '''
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    cursor.execute('SELECT stock FROM Products WHERE id = ?', (id,))

    stock = cursor.fetchone()[0]
    conn.close()
    return stock

def get_all_branch_names()->list:
    '''
    Obtiene todos los nombres de las sucursales de la tabla Branches
    '''
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT name
    FROM Branches
    ''')

    branch_names = cursor.fetchall()
    conn.close()
    
    # Extrae solo los nombres de las sucursales de las tuplas
    branch_names = [name[0] for name in branch_names]
    
    return branch_names

def get_all_sales(target_timezone: str = 'America/Argentina/Buenos_Aires') -> list:
    '''
    Obtiene todos los registros de la tabla Sales y convierte la fecha de cada venta a la zona horaria deseada.
    id[0], product_id[1], user_id [2], branch_name[3], quantity[4], date[5], price[6], category[7]
    :param target_timezone: Zona horaria a la que se desea convertir la fecha (por defecto 'America/Argentina/Buenos_Aires')
    :return: Lista de ventas con las fechas convertidas en la zona horaria especificada
    '''
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT id, product_id, user_id, branch_name, quantity, date, price, category
    FROM Sales
    ''')

    sales = cursor.fetchall()
    conn.close()

    sales_converted = []
    for sale in sales:
        sale_id, product_id, user_id, branch_name, quantity, sale_date, price, category = sale

        # Convierte el string a objeto datetime asumiendo que la fecha está en UTC
        sale_datetime_utc = datetime.strptime(sale_date, '%Y-%m-%d %H:%M:%S').replace(tzinfo=ZoneInfo('UTC'))

        # Convierte a la zona horaria objetivo
        sale_datetime_local = sale_datetime_utc.astimezone(ZoneInfo(target_timezone))

        # Guarda los datos con la fecha convertida en la lista final
        sale_with_converted_date = (sale_id, product_id, user_id, branch_name, quantity, sale_datetime_local.strftime('%Y-%m-%d %H:%M:%S'), price, category)
        sales_converted.append(sale_with_converted_date)

    return sales_converted

def get_product_name(id:int)->str:
    '''
    Obtiene el nombre de un producto
    '''
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    cursor.execute('SELECT name FROM Products WHERE id = ?', (id,))

    name = cursor.fetchone()[0]
    conn.close()
    return name

def get_user_name(id:int)->str:
    '''
    Obtiene el nombre de un usuario
    '''
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    cursor.execute('SELECT name FROM Users WHERE id = ?', (id,))

    name = cursor.fetchone()[0]
    conn.close()
    return name

def get_restock_date(restock_id: int, target_timezone: str = 'America/Argentina/Buenos_Aires') -> str:
    '''
    Obtiene la fecha de un restock específico y la convierte a la zona horaria deseada.
    :param restock_id: ID del restock
    :param target_timezone: Zona horaria a la que se desea convertir la fecha (por defecto 'America/Argentina/Buenos_Aires')
    :return: Fecha del restock en la zona horaria especificada como string
    '''
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT MAX(date)
    FROM Restocks
    WHERE id = ?
    ''', (restock_id,))

    restock_date = cursor.fetchone()
    conn.close()
    if restock_date and restock_date[0]:
        # Convierte el string a objeto datetime asumiendo que esta en UTC
        restock_datetime_utc = datetime.strptime(restock_date[0], '%Y-%m-%d %H:%M:%S').replace(tzinfo=ZoneInfo('UTC'))

        # Convierte a la zona horaria objetivo
        restock_datetime_local = restock_datetime_utc.astimezone(ZoneInfo(target_timezone))

        # Devuelve la fecha convertida como string
        return restock_datetime_local.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return ("Fecha no disponible.")

def get_name_per_id(name:str):  # sourcery skip: avoid-builtin-shadow
    '''
    Obtiene el nombre de un usuario
    '''
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM Products WHERE name = ?', (name,))

    id = cursor.fetchone()[0]
    conn.close()
    return id

def branch_exists(branch_name: str) -> bool:
    """Comprueba si una sucursal con el nombre dado existe en la tabla Branches."""
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM Branches WHERE name = ?", (branch_name,))
    result = cursor.fetchone()
    return result is not None

def get_all_branches()->list:
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT name
    FROM Branches
    ''')

    branches = cursor.fetchall()
    conn.close()
    return branches

@log_database_action("New_Branch")
def create_new_branch(name, address)->None:
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO Branches (name, address) VALUES (?, ?)', (name, address))
    conn.close()

def get_products_in_branch(name)->list:
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Products WHERE branch_name =?", (name,))
    products = cursor.fetchall()
    conn.close()
    return products

def export_to_file(path_to_export='sales_export.csv') -> csv:
    conn = sqlite3.connect(dataBasePath);cursor = conn.cursor();cursor.execute("SELECT * FROM Sales")
    with open('sales_export.csv', 'w', newline='', encoding='utf-8') as f:  writer = csv.writer(f);writer.writerow([i[0] for i in cursor.description])  ;writer.writerows(cursor.fetchall()) ; conn.close()

if __name__ == "__main__":
    
    ''' Literalmente aca solo copie y pegue del archivo example.py por cuestion de que se utilizaria
        para ejecutar tests'''
    
    create_database()

    register_user('John Doe', 'john@example.com', 'password123', 1, "San miguel")
    register_user('Jane Smith', 'jane@example.com', 'admin456', 2, "Jose c paz")
    register_user('Carlos Torres', 'carlos@example.com', 'superadmin789', 3, "Retiro")

    product1 = Product('White T-shirt', 19.99, 'Brand X', 'M', "T-Shirt", 'White cotton t-shirt', "San Miguel" , stock=10)
    product2 = Product('Blue Jeans', 39.99, 'Brand Y', 'L', "Jeans", 'Blue denim jeans', "San Miguel", stock=10)

    add_product(product1)
    add_product(product2)

    user_id = get_user_id('john@example.com')
    record_sale(1, user_id, "San Miguel", 2, price=20)  
    user_id = get_user_id('jane@example.com')
    record_restock(2, user_id, 2, 10) 
    
    print(get_user_details(get_user_id('john@example.com')))

    products_in_stock = get_products_in_stock()
    for product in products_in_stock:
        print(f"Product: {product.name}, Price: {product.price}, Brand: {product.brand}, Size: {product.size}, Description: {product.description}")
