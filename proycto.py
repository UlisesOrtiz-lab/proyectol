import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QWidget, QDateEdit, QTabWidget
)
from PyQt5.QtCore import Qt, QDate
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt  
import pandas as pd
from PyQt5.QtWidgets import QMessageBox




class BudgetApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicación de Gestión de Presupuestos")
        self.setGeometry(100, 100, 1000, 700)

        # Bandera para el modo oscuro
        self.dark_mode_enabled = False

        # Configuración inicial (Modo claro por defecto)
        self.apply_light_mode()

        # Layout principal
        self.layout = QVBoxLayout()

        # Botón para alternar el modo oscuro
        self.toggle_mode_button = QPushButton("Activar Modo Oscuro")
        self.toggle_mode_button.clicked.connect(self.toggle_mode)
        self.layout.addWidget(self.toggle_mode_button)

        # Resto del código existente para inicializar la interfaz...
        self.income_input = QLineEdit()
        self.income_input.setPlaceholderText("Monto Total de Ingreso")
        self.layout.addWidget(QLabel("Total de Ingresos"))
        self.layout.addWidget(self.income_input)

        # Contenedor principal
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Inicialización de datos y funcionalidad
        self.data = pd.DataFrame(columns=["Tipo", "Monto", "Categoría", "Fecha"])
        self.total_income = 0
        self.total_expenses = 0
        self.balance = 0

    def apply_light_mode(self):
        """Aplica el estilo para el modo claro."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F5F5F5;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #000000;
            }
            QLineEdit, QDateEdit, QComboBox {
                background-color: white;
                color: black;
                border: 2px solid #4CAF50;
                border-radius: 5px;
                padding: 5px;
            }
        """)

    def apply_dark_mode(self):
        """Aplica el estilo para el modo oscuro."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QPushButton {
                background-color: #BB86FC;
                color: white;
                font-size: 14px;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #985EFF;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #FFFFFF;
            }
            QLineEdit, QDateEdit, QComboBox {
                background-color: #1E1E1E;
                color: white;
                border: 2px solid #BB86FC;
                border-radius: 5px;
                padding: 5px;
            }
        """)

    def toggle_mode(self):
        """Alterna entre modo claro y modo oscuro."""
        if self.dark_mode_enabled:
            self.apply_light_mode()
            self.toggle_mode_button.setText("Activar Modo Oscuro")
        else:
            self.apply_dark_mode()
            self.toggle_mode_button.setText("Activar Modo Claro")
        self.dark_mode_enabled = not self.dark_mode_enabled


    def toggle_mode(self):
        """Alterna entre modo claro y modo oscuro."""
        if self.dark_mode_enabled:
            self.apply_light_mode()
            self.toggle_mode_button.setText("Activar Modo Oscuro")
        else:
            self.apply_dark_mode()
            self.toggle_mode_button.setText("Activar Modo Claro")
        self.dark_mode_enabled = not self.dark_mode_enabled

        self.layout = QVBoxLayout()

        self.income_input = QLineEdit()
        self.income_input.setPlaceholderText("Monto Total de Ingreso")
        self.layout.addWidget(QLabel("Total de Ingresos"))
        self.layout.addWidget(self.income_input)

        self.add_income_button = QPushButton("Añadir Ingreso")
        self.add_income_button.clicked.connect(self.add_income)
        self.layout.addWidget(self.add_income_button)

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

        self.expense_date_input = QDateEdit()
        self.expense_date_input.setCalendarPopup(True)
        self.expense_date_input.setDate(QDate.currentDate())
        self.layout.addWidget(QLabel("Fecha del Gasto"))
        self.layout.addWidget(self.expense_date_input)

        self.add_expense_button = QPushButton("Añadir Gasto")
        self.add_expense_button.clicked.connect(self.add_expense)
        self.layout.addWidget(self.add_expense_button)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Tipo", "Monto", "Categoría", "Porcentaje", "Fecha"])
        self.layout.addWidget(self.table)

        self.balance_label = QLabel("Balance Total: 0")
        self.layout.addWidget(self.balance_label)

        self.daily_balance_table = QTableWidget(0, 5)
        self.daily_balance_table.setHorizontalHeaderLabels(
            ["Fecha", "Ingresos", "Gastos", "Balance Diario", "Porcentaje de Gasto"]
        )
        self.layout.addWidget(QLabel("Balance Diario"))
        self.layout.addWidget(self.daily_balance_table)

        self.monthly_balance_table = QTableWidget(0, 2)
        self.monthly_balance_table.setHorizontalHeaderLabels(["Mes", "Balance Mensual"])
        self.layout.addWidget(QLabel("Balance Mensual"))
        self.layout.addWidget(self.monthly_balance_table)

        self.show_daily_graph_button = QPushButton("Ver Gráfica de Gastos Diarios")
        self.show_daily_graph_button.clicked.connect(self.show_daily_graph)
        self.layout.addWidget(self.show_daily_graph_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        
        self.data = pd.DataFrame(columns=["Tipo", "Monto", "Categoría", "Fecha"])
        self.total_income = 0
        self.total_expenses = 0
        self.balance = 0

    def add_income(self):
        """Añade ingresos adicionales y actualiza el balance."""
        try:
            amount = float(self.income_input.text())
            date = QDate.currentDate().toString("yyyy-MM-dd")
            self.update_data("Ingreso", amount, "Ingreso", date)
            self.income_input.clear()
        except ValueError:
            print("Error: El monto del ingreso debe ser un número.")

    def add_category(self):
        """Añade una nueva categoría al ComboBox de categorías."""
        category_name = self.new_category_input.text().strip()
        if category_name and category_name not in [self.category_input.itemText(i) for i in range(self.category_input.count())]:
            self.category_input.addItem(category_name)
            self.new_category_input.clear()
        else:
            print("Error: La categoría ya existe o está vacía.")

    def add_expense(self):
        """Añade un gasto y actualiza el balance."""
        try:
            amount = float(self.expense_input.text())
            category = self.category_input.currentText()
            date = self.expense_date_input.date().toString("yyyy-MM-dd")
            self.update_data("Gasto", -amount, category, date)
            self.expense_input.clear()
        except ValueError:
            print("Error: El monto del gasto debe ser un número.")

    def update_data(self, tipo, monto, categoria, fecha):
        """Actualiza el DataFrame con la nueva transacción."""
        percentage = f"{abs(monto) / self.total_income * 100:.2f}%" if self.total_income > 0 else "0.00%"
        new_entry = pd.DataFrame([[tipo, monto, categoria, fecha]], columns=["Tipo", "Monto", "Categoría", "Fecha"])
        
        if not new_entry.empty:
            self.data = pd.concat([self.data, new_entry], ignore_index=True)
        else:
            print("Error: El nuevo registro está vacío y no se puede añadir.")

        if tipo == "Ingreso":
            self.total_income += monto
        elif tipo == "Gasto":
            self.total_expenses += -monto

        self.update_balance()

        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(tipo))
        self.table.setItem(row_position, 1, QTableWidgetItem(str(monto)))
        self.table.setItem(row_position, 2, QTableWidgetItem(categoria))
        self.table.setItem(row_position, 3, QTableWidgetItem(percentage))
        self.table.setItem(row_position, 4, QTableWidgetItem(fecha))

    def update_balance(self):
        """Actualiza el balance total y lo muestra en la interfaz."""
        self.balance = self.total_income - self.total_expenses
        self.balance_label.setText(f"Balance Total: {self.balance}")
        self.update_daily_balance()
        self.update_monthly_balance()

    def update_daily_balance(self):
        """Actualiza el balance diario en la tabla."""
        daily_totals = self.data.groupby("Fecha")["Monto"].agg(["sum", "count"]).reset_index()
        self.daily_balance_table.setRowCount(0)

        for _, row in daily_totals.iterrows():
            ingresos = self.data[(self.data["Fecha"] == row["Fecha"]) & (self.data["Monto"] > 0)]["Monto"].sum()
            gastos = abs(self.data[(self.data["Fecha"] == row["Fecha"]) & (self.data["Monto"] < 0)]["Monto"].sum())
            porcentaje_gasto = f"{(gastos / ingresos * 100):.2f}%" if ingresos > 0 else "0.00%"

            row_position = self.daily_balance_table.rowCount()
            self.daily_balance_table.insertRow(row_position)
            self.daily_balance_table.setItem(row_position, 0, QTableWidgetItem(row["Fecha"]))
            self.daily_balance_table.setItem(row_position, 1, QTableWidgetItem(str(ingresos)))
            self.daily_balance_table.setItem(row_position, 2, QTableWidgetItem(str(gastos)))
            self.daily_balance_table.setItem(row_position, 3, QTableWidgetItem(str(ingresos - gastos)))
            self.daily_balance_table.setItem(row_position, 4, QTableWidgetItem(porcentaje_gasto))

    def update_monthly_balance(self):
        """Actualiza el balance mensual en la tabla."""
        self.data["Mes"] = pd.to_datetime(self.data["Fecha"]).dt.to_period("M")
        monthly_totals = self.data.groupby("Mes")["Monto"].sum()

        self.monthly_balance_table.setRowCount(0)
        for month, balance in monthly_totals.items():
            row_position = self.monthly_balance_table.rowCount()
            self.monthly_balance_table.insertRow(row_position)
            self.monthly_balance_table.setItem(row_position, 0, QTableWidgetItem(str(month)))
            self.monthly_balance_table.setItem(row_position, 1, QTableWidgetItem(str(balance)))

    
    def show_daily_graph(self):
        """Muestra una gráfica con los gastos diarios por categoría."""
        selected_row = self.daily_balance_table.currentRow()
        if selected_row < 0:
            print("Seleccione un día en la tabla de balances diarios.")
            return

        selected_date = self.daily_balance_table.item(selected_row, 0).text()
        daily_data = self.data[self.data["Fecha"] == selected_date]

        if daily_data.empty:
            print("No hay datos para la fecha seleccionada.")
            return

        category_totals = daily_data.groupby("Categoría")["Monto"].sum()

        fig, ax = plt.subplots()
        ax.pie(
            abs(category_totals),
            labels=category_totals.index,
            autopct='%1.1f%%',
            startangle=140
        )
        ax.set_title(f"Distribución de Gastos para {selected_date}")
        plt.show()

    
def show_error_message(self, title, message):
    """Muestra un mensaje emergente de error."""
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.exec_()

def add_income(self):
    """Añade ingresos adicionales y actualiza el balance."""
    try:
        amount = float(self.income_input.text())
        date = QDate.currentDate().toString("yyyy-MM-dd")
        self.update_data("Ingreso", amount, "Ingreso", date)
        self.income_input.clear()
    except ValueError:
        self.show_error_message("Error de Ingreso", "El monto del ingreso debe ser un número válido.")

def add_category(self):
    """Añade una nueva categoría al ComboBox de categorías."""
    category_name = self.new_category_input.text().strip()
    if category_name:
        if category_name not in [self.category_input.itemText(i) for i in range(self.category_input.count())]:
            self.category_input.addItem(category_name)
            self.new_category_input.clear()
        else:
            self.show_error_message("Error de Categoría", "La categoría ya existe.")
    else:
        self.show_error_message("Error de Categoría", "El nombre de la categoría no puede estar vacío.")

def add_expense(self):
    """Añade un gasto y actualiza el balance."""
    try:
        amount = float(self.expense_input.text())
        if amount <= 0:
            raise ValueError("El monto del gasto debe ser positivo.")
        category = self.category_input.currentText()
        date = self.expense_date_input.date().toString("yyyy-MM-dd")
        self.update_data("Gasto", -amount, category, date)
        self.expense_input.clear()
    except ValueError:
        self.show_error_message("Error de Gasto", "El monto del gasto debe ser un número positivo.")
    except Exception as e:
        self.show_error_message("Error", str(e))
def __init__(self):
        super().__init__()
        # Código existente...
        
        # Inicializamos la clase DataUpdater
        self.updater = DataUpdater(self)

def add_income(self):
        """Añade ingresos adicionales y actualiza el balance."""
        try:
            amount = float(self.income_input.text())
            date = QDate.currentDate().toString("yyyy-MM-dd")
            self.update_data("Ingreso", amount, "Ingreso", date)
            self.income_input.clear()
            # Dispara actualización automática
            self.updater.trigger_update()
        except ValueError:
            self.show_error_message("Error de Ingreso", "El monto del ingreso debe ser un número válido.")
def add_expense(self):
        """Añade un gasto y actualiza el balance."""
        try:
            amount = float(self.expense_input.text())
            if amount <= 0:
                raise ValueError("El monto del gasto debe ser positivo.")
            category = self.category_input.currentText()
            date = self.expense_date_input.date().toString("yyyy-MM-dd")
            self.update_data("Gasto", -amount, category, date)
            self.expense_input.clear()
            # Dispara actualización automática
            self.updater.trigger_update()
        except ValueError:
            self.show_error_message("Error de Gasto", "El monto del gasto debe ser un número positivo.")

def add_category(self):
        """Añade una nueva categoría al ComboBox de categorías."""
        category_name = self.new_category_input.text().strip()
        if category_name:
            if category_name not in [self.category_input.itemText(i) for i in range(self.category_input.count())]:
                self.category_input.addItem(category_name)
                self.new_category_input.clear()
                # Dispara actualización automática (opcional, si la categoría afecta balances)
                self.updater.trigger_update()
            else:
                self.show_error_message("Error de Categoría", "La categoría ya existe.")
        else:
            self.show_error_message("Error de Categoría", "El nombre de la categoría no puede estar vacío.")

def __init__(self):
        super().__init__()
        # Código existente...

        # Inicializamos el administrador de categorías
        self.category_manager = CategoryManager(self.category_input)

def add_category(self):
        """Añade una nueva categoría al ComboBox de categorías usando CategoryManager."""
        category_name = self.new_category_input.text().strip()
        if category_name:
            if self.category_manager.add_category(category_name):
                self.new_category_input.clear()
                self.show_error_message("Éxito", f"Categoría '{category_name}' añadida correctamente.")
            else:
                self.show_error_message("Error de Categoría", "La categoría ya existe.")
        else:
            self.show_error_message("Error de Categoría", "El nombre de la categoría no puede estar vacío.")

def start_app():
    app = QApplication(sys.argv)
    window = BudgetApp()
    window.show()
    sys.exit(app.exec_())


start_app()

