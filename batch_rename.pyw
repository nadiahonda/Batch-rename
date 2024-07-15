import os
import sys
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLineEdit, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QIntValidator


class BatchRenameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Batch File Renamer')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.base_name_label = QLabel('Base Name:', self)
        layout.addWidget(self.base_name_label)

        self.base_name_input = QLineEdit(self)
        layout.addWidget(self.base_name_input)

        self.year_label = QLabel('Year:', self)
        layout.addWidget(self.year_label)

        self.year_input = QLineEdit(str(datetime.now().year), self)
        # Limita o input para anos entre 1000 e 9999
        year_validator = QIntValidator(1000, 9999, self)
        self.year_input.setValidator(year_validator)
        # Limita o tamanho do input para 4 dígitos
        self.year_input.setMaxLength(4)
        layout.addWidget(self.year_input)

        self.start_count_label = QLabel('Start Count:', self)
        layout.addWidget(self.start_count_label)

        self.start_count_input = QLineEdit('001', self)
        # Limita o tamanho do input para 3 dígitos
        self.start_count_input.setMaxLength(3)
        # Aceita apenas números de 1 a 999
        validator = QIntValidator(1, 999, self)
        self.start_count_input.setValidator(validator)
        layout.addWidget(self.start_count_input)

        self.rename_button = QPushButton('Select Files and Rename', self)
        self.rename_button.clicked.connect(self.selectFiles)
        layout.addWidget(self.rename_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def selectFiles(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select files to rename", "", "All Files (*);;Text Files (*.txt)", options=options)
        if files:
            self.batch_rename(files, self.base_name_input.text(
            ), self.year_input.text(), int(self.start_count_input.text()))

    def batch_rename(self, files, base_name, year, start_count):
        errors = False
        for index, file_path in enumerate(files, start=start_count):
            try:
                folder_path, file_name = os.path.split(file_path)
                new_name = f"{base_name}_{year}_{str(index).zfill(3)}{
                    os.path.splitext(file_name)[1]}"
                renamed = os.path.join(folder_path, new_name)
                os.rename(file_path, renamed)
                print(f"Renamed {file_name} to {new_name}")
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Error renaming {file_path}: {e}")
                errors = True
                break  # Stop renaming process after the first error

        if not errors:
            QMessageBox.information(
                self, "Complete", "All files have been renamed successfully.")


def main():
    app = QApplication(sys.argv)
    ex = BatchRenameWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
