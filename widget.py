# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QPushButton
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo


class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        # Находим кнопку по имени
        self.pushButton = self.findChild(QPushButton, "pushButton")
        # Подключаем обработчик события нажатия кнопки
        self.pushButton.clicked.connect(self.show_message_box)
        # Находим другую кнопку по имени
        self.pushButton2 = self.findChild(QPushButton, "pushButton_2")
        # Подключаем обработчик события нажатия кнопки
        self.pushButton2.clicked.connect(self.onButton2Clicked)


    def show_message_box(self):
        # Создаем и отображаем MessageBox
        QMessageBox.information(self, 'Заголовок MessageBox', 'Текст сообщения', QMessageBox.Ok)

    def onButton2Clicked(self):
        self.serial_port = QSerialPort(self)
        available_ports = QSerialPortInfo.availablePorts()

        if not available_ports:
            QMessageBox.warning(self, 'Предупреждение', 'Не найдено доступных COM-портов.', QMessageBox.Ok)
            return

        # Пример: выбор первого доступного порта
        port_info = available_ports[0]
        self.serial_port.setPort(port_info)

        # Настройка параметров порта (скорость передачи, бит данных и так далее)
        self.serial_port.setBaudRate(QSerialPort.Baud9600)
        self.serial_port.setDataBits(QSerialPort.Data8)
        self.serial_port.setParity(QSerialPort.NoParity)
        self.serial_port.setStopBits(QSerialPort.OneStop)

        # Пример: открытие порта
        if not self.serial_port.open(QSerialPort.ReadOnly):
            QMessageBox.warning(self, 'Предупреждение', f'Не удалось открыть порт {port_info.portName()}')

        # Пример: подключение слота к событи приема данных
        self.serial_port.readyRead.connect(self.read_data)

    def read_data(self):
        # Пример: чтение данных из порта
        data = self.serial_port.readAll()
        # Обработка полученных данных
        print(data.decode('utf-8'))


if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())
