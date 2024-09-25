import sqlite3
import hashlib

class Product:
    def __init__(self, name:str, price:int, brand:str, size:any, image:any, description:str, branch_name:str, stock:int, image_path=None, id:int=None):
        self.id = id
        self.name = name
        self.price = price
        self.brand = brand
        self.size = size
        self.stock = stock
        if image_path:
            self.image = self.convert_image_to_binary(image_path)
        else:
            self.image = image  # Asume que image es un binario si image_path no está presente
        self.description = description
        self.branch_name = branch_name

    def convert_image_to_binary(self, image_path)->bytearray:
        with open(image_path, 'rb') as file:
            return file.read()

    @classmethod
    def from_row(cls, row)->tuple:
        # Crea una instancia de Product a partir de una fila de la base de datos
        return cls(
            id=row[0],
            name=row[1],
            price=row[2],
            brand=row[3],
            size=row[4],
            image=row[5],  
            description=row[6],
            branch_name=row[7],
            stock=row[8]
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
        image BLOB,
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

    conn.commit()
    conn.close()

    print("Database creada.")

def register_user(name, email, password, role_id, branch_id)->None:
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM Users WHERE email = ?', (email,))
    if cursor.fetchone() is not None:
        print(f"Error: ya existe un usuario con este email.")
        conn.close()
        return
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute('''
    INSERT INTO Users (name, email, password, role_id, branch_id)
    VALUES (?, ?, ?, ?, ?)
    ''', (name, email, hashed_password, role_id, branch_id))
    
    conn.commit()
    conn.close()

    print(f"User {name} registrado.")

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

def add_product(product)->None:
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO Products (name, price, brand, size, image, description, branch_name, stock)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (product.name, product.price, product.brand, product.size, product.image, product.description, product.branch_name, product.stock))
    
    conn.commit()
    conn.close()

    print(f"Product {product.name} added successfully.")

def record_sale(product_id:int, user_id:int, branch_name:str, quantity:int, price:int)->None:
    '''
    Guarda una venta de un producto y reduce el stock del producto.
    '''
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
        INSERT INTO Sales (product_id, user_id, branch_name, quantity, price)
        VALUES (?, ?, ?, ?, ?)
        ''', (product_id, user_id, branch_name, quantity, price))

        # Reduce el stock
        new_stock = current_stock - quantity
        cursor.execute('UPDATE Products SET stock = ? WHERE id = ?', (new_stock, product_id))

        # Registra la acción en los logs
        cursor.execute('''
        INSERT INTO Logs (action, user_id, product_id, branch_name, quantity, price)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', ('Sale', user_id, product_id, branch_name, quantity, price))

        conn.commit()
        print(f"Venta guardada .Stock: {new_stock}")
    else:
        print("Error: No hay suficiente stock.")

    conn.close()
    
def get_products_out_of_stock()->dict:
    """
    Recupera los productos que no tienen stock disponible.
    """
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT p.id, p.name, b.name, p.price, p.stock FROM Products p
    JOIN Brands b ON p.brand_id = b.id
    WHERE p.stock = 0
    ''')
    
    products_out_of_stock = cursor.fetchall()
    conn.close()

    return products_out_of_stock

def record_restock(product_id:int, user_id:int, branch_name:str, quantity:int)->None:
    '''
    Guarda el reestock de un producto
    '''
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    cursor.execute('SELECT stock FROM Products WHERE id = ?', (product_id,))
    current_stock = cursor.fetchone()[0]
    new_stock = current_stock + quantity

    cursor.execute('UPDATE Products SET stock = ? WHERE id = ?', (new_stock, product_id))
    cursor.execute('''
    INSERT INTO Restocks (product_id, user_id, branch_name, quantity)
    VALUES (?, ?, ?, ?)
    ''', (product_id, user_id, branch_name, quantity))

    cursor.execute('''
    INSERT INTO Logs (action, user_id, product_id, branch_name, quantity)
    VALUES (?, ?, ?, ?, ?)
    ''', ('Restock', user_id, product_id, branch_name, quantity))

    conn.commit()
    conn.close()

def get_products_in_stock()->dict:
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
    
    products = [Product.from_row(row) for row in rows]
    return products

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
    LEFT JOIN Branches ON Users.branch_id = Branches.id
    WHERE Users.id = ?
    ''', (user_id,))

    user_details = cursor.fetchone()
    conn.close()
    
    return user_details

def get_record_from_table(table_name, columns='*', **kwargs:str)->any:
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
    if isinstance(columns, list):
        columns_str = ', '.join(columns)
    else:
        columns_str = columns

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

def get_all_sales()->list:
    '''
    Obtiene todos los registros de la tabla Sales
    '''
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT id, product_id, user_id, branch_name, quantity, date, price
    FROM Sales
    ''')

    sales = cursor.fetchall()
    conn.close()
    
    return sales

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

def get_restock_date(restock_id: int) -> str:
    '''
    Obtiene la fecha de un restock específico
    '''
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT date
    FROM Restocks
    WHERE id = ?
    ''', (restock_id,))

    restock_date = cursor.fetchone()
    conn.close()
    
    # Si se encuentra el restock, devuelve la fecha, sino, devuelve None
    return restock_date[0] if restock_date else None

def get_name_per_id(name:str):
    '''
    Obtiene el nombre de un usuario
    '''
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM Products WHERE name = ?', (name,))

    id = cursor.fetchone()[0]
    conn.close()
    return id

def branch_exists(connection, branch_name: str) -> bool:
    """Comprueba si una sucursal con el nombre dado existe en la tabla Branches."""
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM Branches WHERE name = ?", (branch_name,))
    result = cursor.fetchone()
    return result is not None

if __name__ == "__main__":
    
    ''' Literalmente aca solo copie y pegue del archivo example.py por cuestion de que se utilizaria
        para ejecutar tests'''
    
    create_database()

    register_user('John Doe', 'john@example.com', 'password123', 1, 1)
    register_user('Jane Smith', 'jane@example.com', 'admin456', 2, 2)
    register_user('Carlos Torres', 'carlos@example.com', 'superadmin789', 3, 3)

    product1 = Product('White T-shirt', 19.99, 'Brand X', 'M', None, 'White cotton t-shirt', "San Miguel", image_path='image1.jpg', stock=10)
    product2 = Product('Blue Jeans', 39.99, 'Brand Y', 'L', None, 'Blue denim jeans', "San Miguel", image_path='image1.jpg', stock=10)

    add_product(product1)
    add_product(product2)

    user_id = get_user_id('john@example.com')
    record_sale(1, user_id, 1, 2, price=20)  
    user_id = get_user_id('jane@example.com')
    record_restock(2, user_id, 2, 10) 
    
    print(get_user_details(get_user_id('john@example.com')))

    products_in_stock = get_products_in_stock()
    for product in products_in_stock:
        print(f"Product: {product.name}, Price: {product.price}, Brand: {product.brand}, Size: {product.size}, Description: {product.description}")
