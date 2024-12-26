from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import logging
from flask_migrate import Migrate

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')

# Configurações
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sua_chave_secreta_aqui')
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or \
    'sqlite:///' + os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

# Modelos
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    registros = db.relationship('Registro', backref='usuario', lazy=True)
    ganhos = db.relationship('Ganho', backref='usuario', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Registro(db.Model):
    __tablename__ = 'registro'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tipo = db.Column(db.String(50), nullable=False)
    km_anterior = db.Column(db.Float)
    km_atual = db.Column(db.Float)
    hodometro = db.Column(db.Float)
    litros_totais = db.Column(db.Float)
    custo_total = db.Column(db.Float)
    observacao = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

class Ganho(db.Model):
    __tablename__ = 'ganho'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tipo = db.Column(db.String(50), nullable=False)  # 'Uber' ou 'Ifood'
    valor = db.Column(db.Float, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Rotas
@app.route('/')
def index():
    logger.info('Página inicial acessada')
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Usuario.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        
        flash('Usuário ou senha inválidos')
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if Usuario.query.filter_by(username=username).first():
            flash('Nome de usuário já existe')
            return redirect(url_for('cadastro'))
        
        user = Usuario(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('login'))
    
    return render_template('cadastro.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Busca os últimos registros de abastecimento e troca de óleo
    registros = Registro.query.filter_by(usuario_id=current_user.id).order_by(Registro.data.desc()).limit(5).all()
    
    # Busca os últimos ganhos
    ganhos = Ganho.query.filter_by(usuario_id=current_user.id).order_by(Ganho.data.desc()).limit(5).all()
    
    # Combina os registros e ganhos em uma única lista e ordena por data
    ultimos_registros = sorted(
        registros + ganhos,
        key=lambda x: x.data,
        reverse=True
    )[:5]
    
    # Calcula os totais
    total_ganhos = db.session.query(func.sum(Ganho.valor)).filter_by(usuario_id=current_user.id).scalar() or 0
    total_gastos = db.session.query(func.sum(Registro.custo_total)).filter_by(usuario_id=current_user.id).scalar() or 0
    
    # Calcula a média de consumo
    abastecimentos = Registro.query.filter_by(
        usuario_id=current_user.id,
        tipo='abastecimento'
    ).order_by(Registro.data.desc()).all()
    
    media_consumo = 0
    if abastecimentos:
        total_km = 0
        total_litros = 0
        for abastecimento in abastecimentos:
            total_km += abastecimento.km_atual - abastecimento.km_anterior
            total_litros += abastecimento.litros_totais
        if total_litros > 0:
            media_consumo = total_km / total_litros
    
    # Calcula a próxima troca de óleo
    ultima_troca = Registro.query.filter_by(
        usuario_id=current_user.id,
        tipo='troca_oleo'
    ).order_by(Registro.data.desc()).first()
    
    proxima_troca_oleo = 'Não disponível'
    if ultima_troca:
        km_proxima_troca = ultima_troca.km_atual + 1000  
        proxima_troca_oleo = f'{km_proxima_troca:,.0f}'
    
    return render_template('dashboard.html',
                         ultimos_registros=ultimos_registros,
                         total_ganhos=total_ganhos,
                         total_gastos=total_gastos,
                         media_consumo=media_consumo,
                         proxima_troca_oleo=proxima_troca_oleo)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Rotas do Dashboard
@app.route('/registrar_abastecimento', methods=['GET', 'POST'])
@login_required
def registrar_abastecimento():
    if request.method == 'POST':
        km_anterior = float(request.form.get('km_anterior'))
        km_atual = float(request.form.get('km_atual'))
        litros_totais = float(request.form.get('litros_totais'))
        custo_total = float(request.form.get('custo_total'))
        observacao = request.form.get('observacao')
        
        registro = Registro(
            tipo='abastecimento',
            km_anterior=km_anterior,
            km_atual=km_atual,
            litros_totais=litros_totais,
            custo_total=custo_total,
            observacao=observacao,
            usuario_id=current_user.id
        )
        
        db.session.add(registro)
        db.session.commit()
        
        flash('Abastecimento registrado com sucesso!')
        return redirect(url_for('dashboard'))
    
    return render_template('registrar_abastecimento.html')

@app.route('/registrar_ganho', methods=['GET', 'POST'])
@login_required
def registrar_ganho():
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        valor = float(request.form.get('valor'))
        
        ganho = Ganho(
            tipo=tipo,
            valor=valor,
            usuario_id=current_user.id
        )
        
        db.session.add(ganho)
        db.session.commit()
        
        flash('Ganho registrado com sucesso!')
        return redirect(url_for('dashboard'))
    
    return render_template('registrar_ganho.html')

@app.route('/registrar_oleo', methods=['GET', 'POST'])
@login_required
def registrar_oleo():
    if request.method == 'POST':
        km_atual = float(request.form.get('km_atual'))
        custo_total = float(request.form.get('custo_total'))
        observacao = request.form.get('observacao')
        
        registro = Registro(
            tipo='troca_oleo',
            km_atual=km_atual,
            custo_total=custo_total,
            observacao=observacao,
            usuario_id=current_user.id
        )
        
        db.session.add(registro)
        db.session.commit()
        
        flash('Troca de óleo registrada com sucesso!')
        return redirect(url_for('dashboard'))
    
    return render_template('registrar_oleo.html')

@app.route('/relatorios')
@login_required
def relatorios():
    # Obtém o primeiro dia do mês atual
    hoje = datetime.now()
    primeiro_dia = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Calcula os ganhos do mês
    ganhos_uber = db.session.query(func.sum(Ganho.valor)).filter(
        Ganho.tipo == 'Uber',
        Ganho.usuario_id == current_user.id,
        Ganho.data >= primeiro_dia
    ).scalar() or 0.0
    
    ganhos_ifood = db.session.query(func.sum(Ganho.valor)).filter(
        Ganho.tipo == 'Ifood',
        Ganho.usuario_id == current_user.id,
        Ganho.data >= primeiro_dia
    ).scalar() or 0.0
    
    # Calcula os gastos do mês
    gastos_combustivel = db.session.query(func.sum(Registro.custo_total)).filter(
        Registro.tipo == 'abastecimento',
        Registro.usuario_id == current_user.id,
        Registro.data >= primeiro_dia
    ).scalar() or 0.0
    
    gastos_oleo = db.session.query(func.sum(Registro.custo_total)).filter(
        Registro.tipo == 'troca_oleo',
        Registro.usuario_id == current_user.id,
        Registro.data >= primeiro_dia
    ).scalar() or 0.0
    
    # Calcula o balanço total
    balanco_total = (ganhos_uber + ganhos_ifood) - (gastos_combustivel + gastos_oleo)
    
    # Obtém os últimos registros
    ultimos_registros = []
    
    # Últimos abastecimentos e trocas de óleo
    registros = Registro.query.filter_by(
        usuario_id=current_user.id
    ).order_by(Registro.data.desc()).limit(5).all()
    ultimos_registros.extend(registros)
    
    # Últimos ganhos
    ganhos = Ganho.query.filter_by(
        usuario_id=current_user.id
    ).order_by(Ganho.data.desc()).limit(5).all()
    ultimos_registros.extend(ganhos)
    
    # Ordena todos os registros por data
    ultimos_registros.sort(key=lambda x: x.data, reverse=True)
    ultimos_registros = ultimos_registros[:5]  # Mantém apenas os 5 mais recentes
    
    return render_template('relatorios.html',
                         ganhos_uber=ganhos_uber,
                         ganhos_ifood=ganhos_ifood,
                         gastos_combustivel=gastos_combustivel,
                         gastos_oleo=gastos_oleo,
                         balanco_total=balanco_total,
                         ultimos_registros=ultimos_registros)

# Rotas de Edição e Exclusão
@app.route('/editar_abastecimento/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_abastecimento(id):
    registro = Registro.query.filter_by(id=id, usuario_id=current_user.id, tipo='abastecimento').first_or_404()
    
    if request.method == 'POST':
        registro.km_anterior = float(request.form.get('km_anterior'))
        registro.km_atual = float(request.form.get('km_atual'))
        registro.litros_totais = float(request.form.get('litros_totais'))
        registro.custo_total = float(request.form.get('custo_total'))
        registro.observacao = request.form.get('observacao')
        
        db.session.commit()
        flash('Abastecimento atualizado com sucesso!')
        return redirect(url_for('dashboard'))
    
    return render_template('registrar_abastecimento.html', registro=registro)

@app.route('/editar_ganho/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_ganho(id):
    ganho = Ganho.query.filter_by(id=id, usuario_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        ganho.tipo = request.form.get('tipo')
        ganho.valor = float(request.form.get('valor'))
        
        db.session.commit()
        flash('Ganho atualizado com sucesso!')
        return redirect(url_for('dashboard'))
    
    return render_template('registrar_ganho.html', ganho=ganho)

@app.route('/editar_oleo/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_oleo(id):
    registro = Registro.query.filter_by(id=id, usuario_id=current_user.id, tipo='troca_oleo').first_or_404()
    
    if request.method == 'POST':
        registro.km_atual = float(request.form.get('km_atual'))
        registro.custo_total = float(request.form.get('custo_total'))
        registro.observacao = request.form.get('observacao')
        
        db.session.commit()
        flash('Troca de óleo atualizada com sucesso!')
        return redirect(url_for('dashboard'))
    
    return render_template('registrar_oleo.html', registro=registro)

@app.route('/excluir_abastecimento/<int:id>')
@login_required
def excluir_abastecimento(id):
    registro = Registro.query.filter_by(id=id, usuario_id=current_user.id, tipo='abastecimento').first_or_404()
    db.session.delete(registro)
    db.session.commit()
    flash('Abastecimento excluído com sucesso!')
    return redirect(url_for('dashboard'))

@app.route('/excluir_ganho/<int:id>')
@login_required
def excluir_ganho(id):
    ganho = Ganho.query.filter_by(id=id, usuario_id=current_user.id).first_or_404()
    db.session.delete(ganho)
    db.session.commit()
    flash('Ganho excluído com sucesso!')
    return redirect(url_for('dashboard'))

@app.route('/excluir_oleo/<int:id>')
@login_required
def excluir_oleo(id):
    registro = Registro.query.filter_by(id=id, usuario_id=current_user.id, tipo='troca_oleo').first_or_404()
    db.session.delete(registro)
    db.session.commit()
    flash('Troca de óleo excluída com sucesso!')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 