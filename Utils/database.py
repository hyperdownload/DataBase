import sqlite3
import hashlib

# Define the Product class with image as binary data
class Product:
    def __init__(self, name, price, brand, size, image_path, description, branch_id):
        self.name = name
        self.price = price
        self.brand = brand
        self.size = size
        self.image = self.convert_image_to_binary(image_path)
        self.description = description
        self.branch_id = branch_id

    # Convert image file to binary data
    def convert_image_to_binary(self, image_path):
        with open(image_path, 'rb') as file:
            return file.read()

# Create the database and necessary tables
def create_database():
    conn = sqlite3.connect('./Bd/clothing_store.db')
    cursor = conn.cursor()

    # Create Branches table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Branches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT NOT NULL
    )
    ''')

    # Create Roles table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Roles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')

    # Create Users table
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

    # Create Products table with image as BLOB
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

    # Create Sales table
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

    # Create Restocks table
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

    # Create Logs table
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

    # Insert default roles
    cursor.execute('INSERT OR IGNORE INTO Roles (name) VALUES (?)', ('Normal User',))
    cursor.execute('INSERT OR IGNORE INTO Roles (name) VALUES (?)', ('Admin',))
    cursor.execute('INSERT OR IGNORE INTO Roles (name) VALUES (?)', ('General Admin',))

    # Save changes and close the connection
    conn.commit()
    conn.close()

    print("Database created successfully.")

# Function to register a new user
def register_user(name, email, password, role_id, branch_id):
    conn = sqlite3.connect('clothing_store.db')
    cursor = conn.cursor()
    
    # Check if the email already exists
    cursor.execute('SELECT id FROM Users WHERE email = ?', (email,))
    if cursor.fetchone() is not None:
        print(f"Error: A user with the email '{email}' already exists.")
        conn.close()
        return
    
    # Encrypt the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute('''
    INSERT INTO Users (name, email, password, role_id, branch_id)
    VALUES (?, ?, ?, ?, ?)
    ''', (name, email, hashed_password, role_id, branch_id))
    
    conn.commit()
    conn.close()

    print(f"User {name} registered successfully.")

# Function to get user ID by email
def get_user_id(email):
    conn = sqlite3.connect('clothing_store.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT id FROM Users WHERE email = ?
    ''', (email,))
    
    user_id = cursor.fetchone()
    conn.close()
    
    return user_id[0] if user_id else None

# Function to add a product
def add_product(product):
    conn = sqlite3.connect('clothing_store.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO Products (name, price, brand, size, image, description, branch_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (product.name, product.price, product.brand, product.size, product.image, product.description, product.branch_id))
    
    conn.commit()
    conn.close()

    print(f"Product {product.name} added successfully.")

# Function to record a sale
def record_sale(product_id, user_id, branch_id, quantity):
    conn = sqlite3.connect('clothing_store.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO Sales (product_id, user_id, branch_id, quantity)
    VALUES (?, ?, ?, ?)
    ''', (product_id, user_id, branch_id, quantity))
    
    # Log the action
    cursor.execute('''
    INSERT INTO Logs (action, user_id, product_id, branch_id, quantity)
    VALUES (?, ?, ?, ?, ?)
    ''', ('Sale', user_id, product_id, branch_id, quantity))

    conn.commit()
    conn.close()

    print("Sale recorded successfully.")

# Function to record a restock
def record_restock(product_id, user_id, branch_id, quantity):
    conn = sqlite3.connect('clothing_store.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO Restocks (product_id, user_id, branch_id, quantity)
    VALUES (?, ?, ?, ?)
    ''', (product_id, user_id, branch_id, quantity))
    
    # Log the action
    cursor.execute('''
    INSERT INTO Logs (action, user_id, product_id, branch_id, quantity)
    VALUES (?, ?, ?, ?, ?)
    ''', ('Restock', user_id, product_id, branch_id, quantity))

    conn.commit()
    conn.close()

    print("Restock recorded successfully.")

# Main code
if __name__ == "__main__":
    # Create the database and tables
    create_database()

    # Register example users
    register_user('John Doe', 'john@example.com', 'password123', 1, 1)
    register_user('Jane Smith', 'jane@example.com', 'admin456', 2, 2)
    register_user('Carlos Torres', 'carlos@example.com', 'superadmin789', 3, 3)

    # Add example products
    product1 = Product('White T-shirt', 19.99, 'Brand X', 'M', 'path_to_image1.jpg', 'White cotton t-shirt', 1)
    product2 = Product('Blue Jeans', 39.99, 'Brand Y', 'L', 'path_to_image2.jpg', 'Blue denim jeans', 2)

    add_product(product1)
    add_product(product2)

    # Record example sales and restocks
    user_id = get_user_id('john@example.com')
    record_sale(1, user_id, 1, 2)  # Sale of 2 White T-shirts by John Doe in Branch 1
    user_id = get_user_id('jane@example.com')
    record_restock(2, user_id, 2, 10)  # Restock of 10 Blue Jeans by Jane Smith in Branch 2
