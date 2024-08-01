import sqlite3


class DbConnection:
    def __init__(self):
      self.connectionString = f'./data/scores.db'
    
    def CreateTable(self):
       with sqlite3.connect(self.connectionString) as connection:
          try:
            query = '''CREATE TABLE IF NOT EXISTS Scores(id integer primary key autoincrement,player text,score integer)'''
            connection.execute(query)
            print('Se creo correctamente la tabla') 
          except sqlite3.OperationalError:
            print('La tabla Scores ya existe') 

    def Add_Register(self, player,score):
       with sqlite3.connect(self.connectionString) as connection:
          try:
            query = 'insert into Scores(player,score) values(?,?)'
            values = (player,score)
            connection.execute(query,values)
            connection.commit()
            print('Se inserto el registro correctamente') 
          except sqlite3.OperationalError:
            print('Hubo un error en la ejecucion')
    
    def Get_top_five_scores(self) -> list[tuple]:
       previous_scores = []
       with sqlite3.connect(self.connectionString) as conn:
            c = conn.cursor()
            c.execute("SELECT player, score FROM Scores ORDER BY score DESC LIMIT 5")
            previous_scores = c.fetchall()
        
       return previous_scores