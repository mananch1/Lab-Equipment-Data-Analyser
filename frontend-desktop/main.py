import sys
import requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                             QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# PROD URL
API_URL = "https://lab-equipment-data-analyser-backend.onrender.com/api"
# API_URL = "http://127.0.0.1:8000/api" # LOCAL DEV

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes_bar = fig.add_subplot(121)
        self.axes_pie = fig.add_subplot(122)
        super(MplCanvas, self).__init__(fig)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setGeometry(100, 100, 1200, 700)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_upload_tab()
        self.create_history_tab()

    def create_upload_tab(self):
        self.upload_tab = QWidget()
        layout = QVBoxLayout()
        
        # File Selection Area
        file_layout = QHBoxLayout()
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("border: 1px solid #ccc; padding: 5px; background-color: #fff;")
        self.select_btn = QPushButton("Select CSV")
        self.select_btn.clicked.connect(self.select_file)
        self.upload_btn = QPushButton("Upload & Analyze")
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setEnabled(False)
        
        file_layout.addWidget(self.select_btn)
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.upload_btn)
        layout.addLayout(file_layout)

        # Matplotlib Area
        self.canvas = MplCanvas(self, width=10, height=4, dpi=100)
        layout.addWidget(self.canvas)

        self.upload_tab.setLayout(layout)
        self.tabs.addTab(self.upload_tab, "Upload & Analysis")

    def create_history_tab(self):
        self.history_tab = QWidget()
        layout = QVBoxLayout()
        
        self.refresh_btn = QPushButton("Refresh History")
        self.refresh_btn.clicked.connect(self.load_history)
        layout.addWidget(self.refresh_btn)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Uploaded At", "Records"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellDoubleClicked.connect(self.on_history_double_click)
        layout.addWidget(self.table)

        self.history_tab.setLayout(layout)
        self.tabs.addTab(self.history_tab, "History")
        
        self.load_history()

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if file_path:
            self.file_path = file_path
            self.file_label.setText(file_path)
            self.upload_btn.setEnabled(True)

    def upload_file(self):
        if not hasattr(self, 'file_path'):
            return
            
        try:
            files = {'file': open(self.file_path, 'rb')}
            response = requests.post(f"{API_URL}/upload/", files=files)
            if response.status_code == 201:
                data = response.json()
                self.plot_data(data['summary'])
                QMessageBox.information(self, "Success", "File uploaded and analyzed.")
                self.load_history()
            else:
                QMessageBox.critical(self, "Error", f"Upload failed: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Connection error: {e}")

    def plot_data(self, summary):
        self.canvas.axes_bar.clear()
        self.canvas.axes_pie.clear()

        # Bar Chart
        averages = summary.get('averages', {})
        if averages:
            self.canvas.axes_bar.bar(averages.keys(), averages.values(), color='skyblue')
            self.canvas.axes_bar.set_title("Average Parameters")

        # Pie Chart
        dist = summary.get('type_distribution', {})
        if dist:
            self.canvas.axes_pie.pie(dist.values(), labels=dist.keys(), autopct='%1.1f%%')
            self.canvas.axes_pie.set_title("Equipment Distribution")

        self.canvas.draw()
        # Switch to first tab to show results
        self.tabs.setCurrentIndex(0)

    def load_history(self):
        try:
            response = requests.get(f"{API_URL}/history/")
            if response.status_code == 200:
                self.history_data = response.json()
                self.table.setRowCount(len(self.history_data))
                for i, row in enumerate(self.history_data):
                    self.table.setItem(i, 0, QTableWidgetItem(str(row['id'])))
                    self.table.setItem(i, 1, QTableWidgetItem(row['uploaded_at']))
                    count = row['summary'].get('total_count', 'N/A') if row['summary'] else 'N/A'
                    self.table.setItem(i, 2, QTableWidgetItem(str(count)))
        except Exception as e:
            print(f"Error loading history: {e}")

    def on_history_double_click(self, row, column):
        if hasattr(self, 'history_data') and row < len(self.history_data):
            item = self.history_data[row]
            summary = item.get('summary')
            if summary:
                self.plot_data(summary)
            else:
                QMessageBox.warning(self, "Info", "No summary data available for this item.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
