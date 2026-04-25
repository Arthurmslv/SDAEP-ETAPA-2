import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from form_ui import Ui_Form


class FormularioItem(QWidget):

    item_salvo = pyqtSignal()

    def __init__(self, id_item=None):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.id_item = id_item

        self.ui.grupoDevolucao.hide()

        self.ui.checkboxDevolvido.stateChanged.connect(self.toggle_devolucao)
        self.ui.botaoSalvar.clicked.connect(self.salvar)

        if self.id_item:
            self.carregar_item()

    def toggle_devolucao(self):

        if self.ui.checkboxDevolvido.isChecked():
            self.ui.grupoDevolucao.show()
        else:
            self.ui.grupoDevolucao.hide()

    def carregar_item(self):

        conn = sqlite3.connect("achados_perdidos.db")
        cursor = conn.cursor()

        cursor.execute("SELECT descricao, detalhes, status FROM itens WHERE id=?", (self.id_item,))
        item = cursor.fetchone()

        conn.close()

        self.ui.descricao.setText(item[0])
        self.ui.observacoes.setText(item[1])

        if item[2] == "DEVOLVIDO":
            self.ui.checkboxDevolvido.setChecked(True)

    def salvar(self):

        descricao = self.ui.descricao.text()
        detalhes = self.ui.observacoes.text()

        data = datetime.now().strftime("%d/%m/%Y %H:%M")

        status = "DEVOLVIDO" if self.ui.checkboxDevolvido.isChecked() else "NÃO DEVOLVIDO"

        conn = sqlite3.connect("achados_perdidos.db")
        cursor = conn.cursor()

        if self.id_item:

            cursor.execute("""
            UPDATE itens
            SET descricao=?, detalhes=?, status=?
            WHERE id=?
            """, (descricao, detalhes, status, self.id_item))

        else:

            cursor.execute("""
            INSERT INTO itens (descricao, data, detalhes, status)
            VALUES (?, ?, ?, ?)
            """, (descricao, data, detalhes, status))

        conn.commit()
        conn.close()

        self.item_salvo.emit()
        self.close()