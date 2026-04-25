import sqlite3
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton


class MaisDetalhesUI(QWidget):

    def __init__(self, id_item):
        super().__init__()

        self.setWindowTitle("Mais detalhes")
        self.setFixedSize(400, 400)

        layout = QVBoxLayout()

        conn = sqlite3.connect("achados_perdidos.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM itens WHERE id=?", (id_item,))
        item = cursor.fetchone()

        conn.close()

        def valor(v):
            return v if v and str(v).strip() != "" else "-"

        textos = [
            f"ID: {item[0]}",
            f"Descrição: {valor(item[1])}",
            f"Data: {valor(item[2])}",
            f"Onde estava: {valor(item[3])}",
            f"Local encontrado: {valor(item[4])}",
            f"Observações: {valor(item[5])}",
            f"Status: {valor(item[6])}"
        ]

        if item[6] == "DEVOLVIDO":
            textos.extend([
                "",
                "=== INFORMAÇÕES DA DEVOLUÇÃO ===",
                f"Nome: {valor(item[7])}",
                f"CPF: {valor(item[8])}",
                f"Telefone: {valor(item[9])}",
                f"Endereço: {valor(item[10])}",
                f"Obs adicionais: {valor(item[11])}"
            ])

        for t in textos:
            layout.addWidget(QLabel(t))

        btn = QPushButton("Fechar")
        btn.clicked.connect(self.close)
        layout.addWidget(btn)

        self.setLayout(layout)