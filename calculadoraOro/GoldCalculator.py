from PyQt5 import QtWidgets, QtCore
from datetime import datetime

class GoldCalculator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculadora de Oro")
        self.resize(950, 500)  # Ajusta el tamaño de la ventana a 800x400 píxeles

        # Crear las etiquetas y campos de entrada para la operación de compra
        self.buy_gold_price_label = QtWidgets.QLabel("Precio del oro por gramo:")
        self.buy_gold_price_entry = QtWidgets.QLineEdit()

        self.buy_gold_weight_label = QtWidgets.QLabel("Gramos de oro:")
        self.buy_gold_weight_entry = QtWidgets.QLineEdit()

        # Crear el botón para realizar la operación de compra
        self.buy_button = QtWidgets.QPushButton("Comprar")
        self.buy_button.clicked.connect(self.calculate_buy_price)

        # Crear las etiquetas y campos de entrada para la operación de venta
        self.sell_jewelry_price_label = QtWidgets.QLabel("Precio de la joya:")
        self.sell_jewelry_price_entry = QtWidgets.QLineEdit()

        self.sell_total_weight_label = QtWidgets.QLabel("Gramos totales:")
        self.sell_total_weight_entry = QtWidgets.QLineEdit()

        # Crear el botón para realizar la operación de venta
        self.sell_button = QtWidgets.QPushButton("Vender")
        self.sell_button.clicked.connect(self.calculate_sell_price)

        self.buy_button.setStyleSheet("background-color: green;")
        self.sell_button.setStyleSheet("background-color: red;")

        self.setStyleSheet("background-color: #FFDAB2;")

        # Crear la tabla para mostrar los cálculos
        self.table = QtWidgets.QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(
            ["Fecha y hora", "Precio del oro por gramo", "Gramos de oro", "Total en euros"])

        # Ajustar el tamaño de la columna
        self.table.setColumnWidth(1, 300)  # Ajusta el ancho de la segunda columna (índice 1) a 200 píxeles
        self.table.setColumnWidth(0, 300)

        # Organizar los widgets en la ventana
        layout = QtWidgets.QVBoxLayout()

        # Operación de compra
        buy_layout = QtWidgets.QHBoxLayout()
        buy_layout.addWidget(self.buy_gold_price_label)
        buy_layout.addWidget(self.buy_gold_price_entry)
        buy_layout.addWidget(self.buy_gold_weight_label)
        buy_layout.addWidget(self.buy_gold_weight_entry)
        buy_layout.addWidget(self.buy_button)
        layout.addLayout(buy_layout)

        # Operación de venta
        sell_layout = QtWidgets.QHBoxLayout()
        sell_layout.addWidget(self.sell_jewelry_price_label)
        sell_layout.addWidget(self.sell_jewelry_price_entry)
        sell_layout.addWidget(self.sell_total_weight_label)
        sell_layout.addWidget(self.sell_total_weight_entry)
        sell_layout.addWidget(self.sell_button)
        layout.addLayout(sell_layout)

        layout.addWidget(self.table)
        self.setLayout(layout)

    # Función para calcular el valor del oro y actualizar la tabla y el archivo de texto
    def calculate_buy_price(self):
        try:
            gold_price = float(self.buy_gold_price_entry.text().replace(',', '.'))
            gold_weight = float(self.buy_gold_weight_entry.text().replace(',', '.'))
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, introduce números válidos.")
            # Limpiar los campos de entrada
            self.buy_gold_price_entry.clear()
            self.buy_gold_weight_entry.clear()
            return

        total = gold_price * gold_weight
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(timestamp))
        self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(gold_price)))
        self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(gold_weight)))
        self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(total)))

        with open("gold_calculations.txt", "a") as file:
            file.write(f"{timestamp}\t{gold_price}\t{gold_weight}\t{total}\n")

        # Limpiar los campos de entrada
        self.buy_gold_price_entry.clear()
        self.buy_gold_weight_entry.clear()

    # Función para calcular el precio del gramo al que se está vendiendo
    def calculate_sell_price(self):
        try:
            jewelry_price = float(self.sell_jewelry_price_entry.text().replace(',', '.'))
            total_weight = float(self.sell_total_weight_entry.text().replace(',', '.'))
        except ValueError:
            QtWidgets.QMessageBox.warning(self, "Error", "Por favor, introduce números válidos.")
            # Limpiar los campos de entrada
            self.sell_jewelry_price_entry.clear()
            self.sell_total_weight_entry.clear()
            return

        sell_price = jewelry_price / total_weight

        QtWidgets.QMessageBox.information(self, "Precio de venta", f"El precio de venta por gramo es: {sell_price}")

        # Limpiar los campos de entrada
        self.sell_jewelry_price_entry.clear()
        self.sell_total_weight_entry.clear()


# Crear la aplicación y la ventana
app = QtWidgets.QApplication([])

# Define los estilos como una cadena de texto
qss_content = """
/* Aquí irían los estilos que antes estaban en tu archivo .qss */
"""

app.setStyleSheet(qss_content)
window = GoldCalculator()
window.show()

# Iniciar la aplicación
app.exec_()
