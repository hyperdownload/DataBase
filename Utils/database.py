import sqlite3
import hashlib

class Product:
    def __init__(self, name:str, price:int, brand:str, size:any, image:any, description:str, branch_id:int, image_path=None):
        self.name = name
        self.price = price
        self.brand = brand
        self.size = size
        if image_path:
            self.image = self.convert_image_to_binary(image_path)
        else:
            self.image = image  # Asume que image es un binario si image_path no está presente
        self.description = description
        self.branch_id = branch_id

    def convert_image_to_binary(self, image_path)->bytearray:
        with open(image_path, 'rb') as file:
            return file.read()

    @classmethod
    def from_row(cls, row)->tuple:
        # Crea una instancia de Product a partir de una fila de la base de datos
        return cls(
            name=row[1],
            price=row[2],
            brand=row[3],
            size=row[4],
            image=row[5],  # Pasa la imagen directamente desde la fila
            description=row[6],
            branch_id=row[7]
        )

dataBasePath = './Bd/clothing_store.db'

def create_database()->None:
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()

    # Creación de tablas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Branches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
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
        branch_id INTEGER NOT NULL,
        FOREIGN KEY (branch_id) REFERENCES Branches(id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        branch_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES Products(id),
        FOREIGN KEY (user_id) REFERENCES Users(id),
        FOREIGN KEY (branch_id) REFERENCES Branches(id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Restocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        branch_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES Products(id),
        FOREIGN KEY (user_id) REFERENCES Users(id),
        FOREIGN KEY (branch_id) REFERENCES Branches(id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT NOT NULL,
        user_id INTEGER,
        product_id INTEGER,
        branch_id INTEGER,
        quantity INTEGER,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(id),
        FOREIGN KEY (product_id) REFERENCES Products(id),
        FOREIGN KEY (branch_id) REFERENCES Branches(id)
    )
    ''')

    # Inserta roles por default
    cursor.execute('INSERT OR IGNORE INTO Roles (name) VALUES (?)', ('Normal User',))
    cursor.execute('INSERT OR IGNORE INTO Roles (name) VALUES (?)', ('Admin',))
    cursor.execute('INSERT OR IGNORE INTO Roles (name) VALUES (?)', ('General Admin',))

    conn.commit()
    conn.close()

    print("Database created successfully.")

def register_user(name, email, password, role_id, branch_id)->None:
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM Users WHERE email = ?', (email,))
    if cursor.fetchone() is not None:
        print(f"Error: A user with the email '{email}' already exists.")
        conn.close()
        return
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute('''
    INSERT INTO Users (name, email, password, role_id, branch_id)
    VALUES (?, ?, ?, ?, ?)
    ''', (name, email, hashed_password, role_id, branch_id))
    
    conn.commit()
    conn.close()

    print(f"User {name} registered successfully.")

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
    INSERT INTO Products (name, price, brand, size, image, description, branch_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (product.name, product.price, product.brand, product.size, product.image, product.description, product.branch_id))
    
    conn.commit()
    conn.close()

    print(f"Product {product.name} added successfully.")

def record_sale(product_id:int, user_id:int, branch_id:int, quantity:int)->None:
    '''
    Guarda una venta de un producto
    '''
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO Sales (product_id, user_id, branch_id, quantity)
    VALUES (?, ?, ?, ?)
    ''', (product_id, user_id, branch_id, quantity))
    
    cursor.execute('''
    INSERT INTO Logs (action, user_id, product_id, branch_id, quantity)
    VALUES (?, ?, ?, ?, ?)
    ''', ('Sale', user_id, product_id, branch_id, quantity))

    conn.commit()
    conn.close()

    print("Sale recorded successfully.")

def record_restock(product_id:int, user_id:int, branch_id:int, quantity:int)->None:
    """Guarda el reestock de un producto

        :param product_id: int, 
        user_id (_type_): _description_
        branch_id (_type_): _description_
        quantity (_type_): _description_
    """
    
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO Restocks (product_id, user_id, branch_id, quantity)
    VALUES (?, ?, ?, ?)
    ''', (product_id, user_id, branch_id, quantity))
    
    cursor.execute('''
    INSERT INTO Logs (action, user_id, product_id, branch_id, quantity)
    VALUES (?, ?, ?, ?, ?)
    ''', ('Restock', user_id, product_id, branch_id, quantity))

    conn.commit()
    conn.close()

    print("Restock recorded successfully.")

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

def get_user_details(user_id:int)->tuple:
    """
    Recupera el email, rol y contraseña de un usuario basado en su ID.
    """
    conn = sqlite3.connect(dataBasePath)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT Users.email, Roles.name as role, Users.password
    FROM Users
    JOIN Roles ON Users.role_id = Roles.id
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

if __name__ == "__main__":
    create_database()

    register_user('John Doe', 'john@example.com', 'password123', 1, 1)
    register_user('Jane Smith', 'jane@example.com', 'admin456', 2, 2)
    register_user('Carlos Torres', 'carlos@example.com', 'superadmin789', 3, 3)

    product1 = Product('White T-shirt', 19.99, 'Brand X', 'M', None, 'White cotton t-shirt', 1, image_path='image1.jpg')
    product2 = Product('Blue Jeans', 39.99, 'Brand Y', 'L', None, 'Blue denim jeans', 2, image_path='image1.jpg')

    add_product(product1)
    add_product(product2)

    user_id = get_user_id('john@example.com')
    record_sale(1, user_id, 1, 2)  
    user_id = get_user_id('jane@example.com')
    record_restock(2, user_id, 2, 10) 
    
    print(get_user_details(get_user_id('john@example.com')))

    products_in_stock = get_products_in_stock()
    for product in products_in_stock:
        print(f"Product: {product.name}, Price: {product.price}, Brand: {product.brand}, Size: {product.size}, Description: {product.description}")
