import flet as ft
import sqlite3 as sql

class TelaCadastroM(ft.Container):
    def __init__(self):
        super().__init__()

        self.nome_m = ft.TextField(
            label="Digite o nome da música",
            width=300,
            height=50
        )

        self.autor = ft.TextField(
            label="Digite o nome do autor da música",
            width=300,
            height=50
        )

        self.genero = ft.TextField(
            label="Digite gênero da música",
            width=300,
            height=50
        )

        self.confirmar = ft.ElevatedButton(
            text="confirmar",
            on_click=self.salvar
        )

        self.content = (
            ft.Column(
                controls=[self.nome_m,self.autor,self.genero,self.confirmar]
            )
        )
    
    def salvar(self, e):
        try:
            conn = sql.connect('urna.db')
            cursor = conn.cursor()

            cursor.execute('''
                SELECT * FROM dimMusicas WHERE nome_musica = ?
            ''', (self.nome_m.value.lower(),))
            existe_m = cursor.fetchone()

            if not existe_m:

                cursor.execute('''
                    SELECT * FROM dimGeneros WHERE nome_genero = ?
                ''', (self.genero.value.lower(),))
                existe_g = cursor.fetchone()

                if not existe_g:
                    cursor.execute('''
                        INSERT INTO dimGeneros(nome_genero)
                        VALUES(?)
                    ''', (self.genero.value.lower(),))
                    conn.commit()

                cursor.execute('''
                    SELECT id_genero FROM dimGeneros WHERE nome_genero = ?
                ''', (self.genero.value.lower(),))
                resultado = cursor.fetchone()[0]

                cursor.execute('''
                    INSERT INTO dimMusicas(nome_musica, id_genero)
                    VALUES(?,?)
                ''', (self.nome_m.value.lower(),resultado))

                conn.commit()

                cursor.execute('''
                    INSERT INTO dimAutores(nome_autor)
                    VALUES(?)
                ''', (self.autor.value.lower(),))

                conn.commit()
                conn.close()
                print("Musica cadastrada!")

            else:
                print("Música já cadastrada")

        except sql.IntegrityError:
            print("Erro: CPF ou e-mail já cadastrado.")