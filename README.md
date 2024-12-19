# Urbanlive Stock Management System

Urbanlive is a comprehensive Stock Management System implemented in Python, designed specifically for clothing stores. It provides a modern, user-friendly graphical interface for managing inventory, sales, and user roles efficiently across multiple store branches.

## Features

1. **User Authentication**: 
   - Secure login system with different access levels (General User and Admin)
   - Password hashing for enhanced security

2. **Stock Management**: 
   - Add and update products in inventory
   - Search functionality for quick product lookup
   - Restock products with logging

3. **Sales Management**:
   - Record sales transactions
   - Support for multiple payment methods (Cash, Credit, Debit, Transfer)
   - Apply discounts to sales

4. **Data Visualization**:
   - Charts for sales per category
   - Custom data visualizing widgets

5. **Multi-branch Support**: 
   - Manage stock and sales across different store branches

6. **Notifications System**:
   - Alert for out-of-stock products

7. **User-friendly Interface**:
   - Modern UI with customtkinter
   - Tooltips for enhanced user experience

## Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/urbanlive-stock-management.git
   cd urbanlive-stock-management
   ```

2. Install the required dependencies:
   ```
   pip install -r dependencias.txt
   ```

### Running the Application

Execute the main script to run the application:

```
python giu.py
```

## Dependencies

The project relies on several Python libraries:

- customtkinter
- PIL (Pillow)
- tkinter
- hashlib
- contextlib
- sqlite3 (included in Python standard library)

For a complete list of dependencies, refer to the `dependencias.txt` file in the project root.

## Project Structure

- `giu.py`: Main application file
- `Utils/`: Utility functions and database operations
- `CTkDataVisualizingWidgets/`: Custom widgets for data visualization
- `CTkToolTip/`: Custom tooltip implementation
- `Opacity/`: Window styling utilities
- `img/`: Image resources for the UI
- `Bd/clothing_store.db`: SQLite database file

## Usage

1. Launch the application
2. Log in with your credentials
3. Navigate through different sections:
   - Main Menu
   - Product Management
   - Sales Recording
   - Stock Updates

## Contributing

Contributions to Urbanlive are welcome! Please feel free to submit a Pull Request.

## License
MIT License
