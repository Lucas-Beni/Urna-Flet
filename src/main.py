import flet as ft
import sqlite3 as sql
from screens.tela_cadastro import TelaCadastro
from screens.tela_login import TelaLogin

conn = sql.connect('urna.db')
cursor = conn.cursor()

# Cria a tabela se não existir
cursor.execute('''
    CREATE TABLE IF NOT EXISTS dimUsuarios(
        id_user INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_user TEXT NOT NULL,
        cpf_user TEXT UNIQUE NOT NULL,
        email_user TEXT UNIQUE NOT NULL,
        senha_user TEXT NOT NULL,
        cargo TEXT NOT NULL CHECK(cargo IN ('adm', 'user'))
    )
''')

# Verifica se já existe um usuário com cargo 'adm'
cursor.execute('''
    SELECT COUNT(*) FROM dimUsuarios WHERE cargo = 'adm'
''')
existe_adm = cursor.fetchone()[0]

# Se não existir, insere o usuário adm padrão
if existe_adm == 0:
    cursor.execute('''
        INSERT INTO dimUsuarios (nome_user, cpf_user, email_user, senha_user, cargo)
        VALUES (?, ?, ?, ?, ?)
    ''', ('Administrador', '00000000000', 'adm@admin.com', 'admin', 'adm'))

conn.commit()
conn.close()

def main(page: ft.Page):
    page.title = "Sistema de Votação"

    def abrir_login():
        page.controls.clear()
        page.add(
            TelaLogin(
                abrir_voto,
                abrir_adm,
                abrir_cadastro
            )
        )

    def abrir_cadastro():
        page.controls.clear()
        page.add(TelaCadastro(abrir_login))

    def abrir_voto():
        page.controls.clear()
        page.add(ft.Text("Tela de Votação"))

    def abrir_adm():
        page.controls.clear()
        page.add(ft.Text("Tela de Administração"))

    # Inicia na tela de login
    abrir_login()

ft.app(target=main, view=ft.WEB_BROWSER)
