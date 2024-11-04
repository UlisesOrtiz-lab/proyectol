import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QWidget
)
from PyQt5.QtCore import Qt
import pandas as pd

class BudgetApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        
        self.setWindowTitle("Aplicación de Gestión de Presupuestos")
        self.setGeometry(100, 100, 600, 600)
        
        self.layout = QVBoxLayout()
        
        self.income_input = QLineEdit()
        self.income_input.setPlaceholderText("Monto Total de Ingreso")
        self.layout.addWidget(QLabel("Total de Ingresos"))
        self.layout.addWidget(self.income_input)
        
        self.set_income_button = QPushButton("Establecer Ingreso Total")
        self.set_income_button.clicked.connect(self.set_income)
        self.layout.addWidget(self.set_income_button)
        
        self.new_category_input = QLineEdit()
        self.new_category_input.setPlaceholderText("Nombre de Nueva Categoría")
        self.layout.addWidget(QLabel("Añadir Nueva Categoría"))
        self.layout.addWidget(self.new_category_input)
        
        self.add_category_button = QPushButton("Añadir Categoría")
        self.add_category_button.clicked.connect(self.add_category)
        self.layout.addWidget(self.add_category_button)
        
        self.expense_input = QLineEdit()
        self.expense_input.setPlaceholderText("Monto de Gasto")
        self.layout.addWidget(QLabel("Gastos"))
        self.layout.addWidget(self.expense_input)
        
        self.category_input = QComboBox()
        self.layout.addWidget(QLabel("Categoría"))
        self.layout.addWidget(self.category_input)
        
        self.add_expense_button = QPushButton("Añadir Gasto")
        self.add_expense_button.clicked.connect(self.add_expense)
        self.layout.addWidget(self.add_expense_button)

        self.table = QTableWidget(0, 3)  
        self.table.setHorizontalHeaderLabels(["Tipo", "Monto", "Categoría"])
        self.layout.addWidget(self.table)

        self.balance_label = QLabel("Balance Total: 0")
        self.layout.addWidget(self.balance_label)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.data = pd.DataFrame(columns=["Tipo", "Monto", "Categoría"])
        self.total_income = 0
        self.total_expenses = 0
        self.balance = 0

    def set_income(self):
        """Establece el ingreso total y actualiza el balance."""
        try:
            self.total_income = float(self.income_input.text())
            self.update_balance()
            self.income_input.clear()
        except ValueError:
            print("Error: El monto de ingreso debe ser un número.")

    def add_category(self):
        """Añade una nueva categoría de gasto al ComboBox de categorías."""
        category_name = self.new_category_input.text().strip()
        if category_name and category_name not in [self.category_input.itemText(i) for i in range(self.category_input.count())]:
            self.category_input.addItem(category_name)
            self.new_category_input.clear()
        else:
            print("Error: La categoría ya existe o está vacía.")

    def add_expense(self):
        """Añade un gasto al registro y actualiza la tabla y el balance."""
        try:
            amount = float(self.expense_input.text())
            category = self.category_input.currentText()
            self.update_data("Gasto", -amount, category)
            self.expense_input.clear()
        except ValueError:
            print("Error: El monto del gasto debe ser un número.")

    def update_data(self, tipo, monto, categoria):
        """Actualiza el DataFrame y el balance, y refresca la tabla de la interfaz."""
        new_entry = pd.DataFrame([[tipo, monto, categoria]], columns=["Tipo", "Monto", "Categoría"])
        self.data = pd.concat([self.data, new_entry], ignore_index=True)
        
        if tipo == "Gasto":
            self.total_expenses += -monto  

        self.update_balance()

        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(tipo))
        self.table.setItem(row_position, 1, QTableWidgetItem(str(monto)))
        self.table.setItem(row_position, 2, QTableWidgetItem(categoria))

    def update_balance(self):
        """Actualiza el balance total y lo muestra en la interfaz."""
        self.balance = self.total_income - self.total_expenses
        self.balance_label.setText(f"Balance Total: {self.balance}")

def start_app():
    app = QApplication(sys.argv)
    window = BudgetApp()
    window.show()
    sys.exit(app.exec_())

start_app()
