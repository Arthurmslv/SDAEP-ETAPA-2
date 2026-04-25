from PyQt5 import QtCore, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 450)

        self.verticalLayout = QtWidgets.QVBoxLayout(Form)

        self.formLayout = QtWidgets.QFormLayout()

        self.descricao = QtWidgets.QLineEdit(Form)
        self.formLayout.addRow("Descrição:", self.descricao)

        self.ondeEstava = QtWidgets.QLineEdit(Form)
        self.formLayout.addRow("Onde estava:", self.ondeEstava)

        self.observacoes = QtWidgets.QLineEdit(Form)
        self.formLayout.addRow("Observações:", self.observacoes)

        self.localEncontrado = QtWidgets.QLineEdit(Form)
        self.formLayout.addRow("Local onde se encontra:", self.localEncontrado)

        self.verticalLayout.addLayout(self.formLayout)

        self.checkboxDevolvido = QtWidgets.QCheckBox("Devolvido")
        self.verticalLayout.addWidget(self.checkboxDevolvido)

        self.grupoDevolucao = QtWidgets.QGroupBox("Informações da devolução")
        self.formLayout2 = QtWidgets.QFormLayout(self.grupoDevolucao)

        self.nome = QtWidgets.QLineEdit()
        self.formLayout2.addRow("Nome:", self.nome)

        self.cpf = QtWidgets.QLineEdit()
        self.formLayout2.addRow("CPF:", self.cpf)

        self.telefone = QtWidgets.QLineEdit()
        self.formLayout2.addRow("Telefone:", self.telefone)

        self.endereco = QtWidgets.QLineEdit()
        self.formLayout2.addRow("Endereço:", self.endereco)

        self.obsAdicionais = QtWidgets.QTextEdit()
        self.formLayout2.addRow("Observações adicionais:", self.obsAdicionais)

        self.verticalLayout.addWidget(self.grupoDevolucao)

        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.botaoVoltar = QtWidgets.QPushButton("Voltar")
        self.horizontalLayout.addWidget(self.botaoVoltar)

        self.botaoSalvar = QtWidgets.QPushButton("Salvar")
        self.horizontalLayout.addWidget(self.botaoSalvar)

        self.verticalLayout.addLayout(self.horizontalLayout)

        QtCore.QMetaObject.connectSlotsByName(Form)