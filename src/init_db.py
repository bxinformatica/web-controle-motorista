from app import app, db

def init_database():
    with app.app_context():
        # Cria todas as tabelas
        db.create_all()
        print("Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    init_database() 