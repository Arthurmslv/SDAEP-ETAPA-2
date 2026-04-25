import sys
import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton,
    QTableWidgetItem, QWidget, QMessageBox
)
from PyQt5 import QtWidgets

from main_ui import Ui_MainWindow
from form_ui import Ui_Form
from details_ui import MaisDetalhesUI

def criar_banco():
    conn = sqlite3.connect("achados_perdidos.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT,
        data TEXT,
        onde_estava TEXT,
        local_encontrado TEXT,
        observacoes TEXT,
        status TEXT,
        nome_recebedor TEXT,
        cpf TEXT,
        telefone TEXT,
        endereco TEXT,
        obs_devolucao TEXT
    )
    """)

    conn.commit()
    conn.close()

class FormularioItem(QWidget):

    def __init__(self, atualizar_callback, id_item=None):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.id_item = id_item
        self.atualizar_callback = atualizar_callback

        self.ui.grupoDevolucao.hide()

        self.ui.checkboxDevolvido.stateChanged.connect(self.toggle_devolucao)
        self.ui.botaoSalvar.clicked.connect(self.salvar)
        self.ui.botaoVoltar.clicked.connect(self.close)

        if self.id_item:
            self.botaoExcluir = QtWidgets.QPushButton("Excluir")
            self.ui.horizontalLayout.addWidget(self.botaoExcluir)
            self.botaoExcluir.clicked.connect(self.excluir_item)

        if self.id_item:
            self.carregar_item()
        else:
            self.setWindowTitle("Novo item")

    def toggle_devolucao(self):
        self.ui.grupoDevolucao.setVisible(
            self.ui.checkboxDevolvido.isChecked()
        )

    def carregar_item(self):

        conn = sqlite3.connect("achados_perdidos.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM itens WHERE id=?", (self.id_item,))
        item = cursor.fetchone()

        conn.close()

        self.ui.descricao.setText(item[1])
        self.ui.ondeEstava.setText(item[3])
        self.ui.localEncontrado.setText(item[4])
        self.ui.observacoes.setText(item[5])

        # dados devolução
        self.ui.nome.setText(item[7] or "")
        self.ui.cpf.setText(item[8] or "")
        self.ui.telefone.setText(item[9] or "")
        self.ui.endereco.setText(item[10] or "")
        self.ui.obsAdicionais.setText(item[11] or "")

        if item[6] == "DEVOLVIDO":
            self.ui.checkboxDevolvido.setChecked(True)

        self.setWindowTitle(f"Alterando informações sobre {item[1]}")

    def salvar(self):

        dados = (
            self.ui.descricao.text(),
            datetime.now().strftime("%d/%m/%Y %H:%M"),
            self.ui.ondeEstava.text(),
            self.ui.localEncontrado.text(),
            self.ui.observacoes.text(),
            "DEVOLVIDO" if self.ui.checkboxDevolvido.isChecked() else "NÃO DEVOLVIDO",
            self.ui.nome.text(),
            self.ui.cpf.text(),
            self.ui.telefone.text(),
            self.ui.endereco.text(),
            self.ui.obsAdicionais.toPlainText()
        )

        conn = sqlite3.connect("achados_perdidos.db")
        cursor = conn.cursor()

        if self.id_item:
            cursor.execute("""
            UPDATE itens
            SET descricao=?, data=?, onde_estava=?, local_encontrado=?, observacoes=?, status=?,
                nome_recebedor=?, cpf=?, telefone=?, endereco=?, obs_devolucao=?
            WHERE id=?
            """, (*dados, self.id_item))
        else:
            cursor.execute("""
            INSERT INTO itens (
                descricao, data, onde_estava, local_encontrado,
                observacoes, status,
                nome_recebedor, cpf, telefone, endereco, obs_devolucao
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, dados)

        conn.commit()
        conn.close()

        self.atualizar_callback()
        self.close()

    def excluir_item(self):

        confirmacao = QMessageBox.question(
            self,
            "Confirmar exclusão",
            "Tem certeza que deseja excluir este item?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmacao == QMessageBox.Yes:

            conn = sqlite3.connect("achados_perdidos.db")
            cursor = conn.cursor()

            cursor.execute("DELETE FROM itens WHERE id=?", (self.id_item,))

            conn.commit()
            conn.close()

            self.atualizar_callback()
            self.close()

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )

        self.ui.botaoPesquisar.clicked.connect(self.pesquisar)
        self.ui.botaoAdcItem.clicked.connect(self.novo_item)
        self.ui.botaoAtualizar.clicked.connect(self.atualizar)

        self.atualizar()

    def buscar_dados(self, filtro=""):

        conn = sqlite3.connect("achados_perdidos.db")
        cursor = conn.cursor()

        if filtro:
            cursor.execute("""
            SELECT * FROM itens WHERE descricao LIKE ?
            """, ('%' + filtro + '%',))
        else:
            cursor.execute("SELECT * FROM itens")

        dados = cursor.fetchall()
        conn.close()

        return dados

    def atualizar(self):
        self.preencher_tabela(self.buscar_dados())

    def pesquisar(self):
        texto = self.ui.campoPesquisar.text()
        self.preencher_tabela(self.buscar_dados(texto))

    def preencher_tabela(self, dados):

        self.ui.tableWidget.setRowCount(len(dados))

        for row, item in enumerate(dados):

            id_item = item[0]

            self.ui.tableWidget.setItem(row, 0, QTableWidgetItem(item[1]))
            self.ui.tableWidget.setItem(row, 1, QTableWidgetItem(item[2]))
            self.ui.tableWidget.setItem(row, 3, QTableWidgetItem(item[6]))

            btn_detalhes = QPushButton("Abrir")
            btn_detalhes.clicked.connect(
                lambda _, id=id_item: self.abrir_detalhes(id)
            )
            self.ui.tableWidget.setCellWidget(row, 2, btn_detalhes)

            btn_editar = QPushButton("Alterar")
            btn_editar.clicked.connect(
                lambda _, id=id_item: self.editar_item(id)
            )
            self.ui.tableWidget.setCellWidget(row, 4, btn_editar)

    def abrir_detalhes(self, id_item):
        self.details = MaisDetalhesUI(id_item)
        self.details.show()

    def novo_item(self):
        self.form = FormularioItem(self.atualizar)
        self.form.show()

    def editar_item(self, id_item):
        self.form = FormularioItem(self.atualizar, id_item)
        self.form.show()

criar_banco()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())