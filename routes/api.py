from flask import Blueprint, request, jsonify, render_template_string, render_template
from flask_login import login_required
from models.credores import Title, Credor
from app import db, csrf

bp = Blueprint('api', __name__)

@bp.route('/api/credores/<int:id>/<status>/', methods=['GET'])
def get_titles_by_creditor(id, status):
    valid_statuses = ['paga', 'atrazo', 'devendo']
    if status not in valid_statuses:
        return jsonify({'error': 'Status inválido'}), 400

    titles = Title.query.filter_by(creditor_id=id, status=status).all()
    result = [{
        'id': title.id,
        'description': title.description,
        'amount': title.amount,
        'status': title.status
    } for title in titles]

    return jsonify(result)

@bp.route('/api/csrf-token', methods=['GET'])
@login_required
def get_csrf_token():
    csrf_token = request.cookies.get('csrf_token')
    if not csrf_token:
        # NOTE: parte da API responsável por gerar um token CSRF atualizado para os formulários
        csrf_token_html = render_template_string('{{ csrf_token() }}')
        response = jsonify({'csrf_token': csrf_token_html})
        response.set_cookie('csrf_token', csrf_token_html)
    else:
        response = jsonify({'csrf_token': csrf_token})
    return response

# NOTE: parte que recebe posts da tabela credores
@bp.route('/api/credor/', methods=['POST'])
@login_required
@csrf.exempt
def handle_credor_action():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400

    tipo = data.get('tipo')
    title_id = data.get('id')
    csrf_token = data.get('csrf_token')

    # INFO: Verificação do token CSRF
    if not csrf_token or csrf_token != request.cookies.get('csrf_token'):
        return jsonify({'error': 'Token CSRF inválido'}), 403

    if tipo == 'edit':
        # INFO: Processa a edição
        credor = Credor.query.get(title_id)
        if not credor:
            return jsonify({'error': 'Credor não encontrado'}), 404
        credor.nome = data.get('nome')
        credor.cidade = data.get('cidade')
        credor.estado = data.get('estado')
        db.session.commit()
        return jsonify({'success': 'Credor atualizado com sucesso'}), 200

    elif tipo == 'novo':
        # INFO: Processa a adição de credor
        credor = Credor(nome=data.get('nome'), cidade=data.get('cidade'), estado=data.get('estado'))
        db.session.add(credor)
        db.session.commit()
        return jsonify({'success': 'Credor adicionado com sucesso'}), 200
    elif tipo == 'delete':
        # INFO: Processa a deleção
        credor = Credor.query.get(title_id)
        if not credor:
            return jsonify({'error': 'Credor não encontrado'}), 404
        db.session.delete(credor)
        db.session.commit()
        return jsonify({'success': 'Credor deletado com sucesso'}), 200

    return jsonify({'error': 'Ação inválida'}), 400

# NOTE: parte que recebe posts da tabela contas
@bp.route('/api/titles/', methods=['POST'])
@login_required
@csrf.exempt
def handle_title_action():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Dados não fornecidos'}), 400

    tipo = data.get('tipo')
    title_id = data.get('id')
    csrf_token = data.get('csrf_token')

    # INFO: Verificação do token CSRF
    if not csrf_token or csrf_token != request.cookies.get('csrf_token'):
        return jsonify({'error': 'Token CSRF inválido'}), 403

    if tipo == 'edit':
        # INFO: Processa a edição
        title = Title.query.get(title_id)
        if not title:
            return jsonify({'error': 'Título não encontrado'}), 404

        title.creditor_id = data.get('credor_id')
        title.description = data.get('descricao')
        title.amount = data.get('valor')
        title.month = data.get('mes')
        title.year = data.get('ano')
        title.status = data.get('status')
        db.session.commit()
        return jsonify({'success': 'Título atualizado com sucesso'}), 200

    elif tipo == 'novo':
        # INFO: Processa a adição
        title = Title(creditor_id=data.get('Credor_Id'), description=data.get('Descricao'), amount=data.get('Valor'),
                      month=data.get('Mes'), year=data.get('Ano'), status=data.get('Status'))
        db.session.add(title)
        db.session.commit()
        return jsonify({'success': 'Título adicionado com sucesso'}), 200
    elif tipo == 'delete':
        # INFO: Processa a deleção
        title = Title.query.get(title_id)
        if not title:
            return jsonify({'error': 'Título não encontrado'}), 404
        db.session.delete(title)
        db.session.commit()
        return jsonify({'success': 'Título deletado com sucesso'}), 200

    return jsonify({'error': 'Ação inválida'}), 400

@bp.route('/report')
def report():
    return render_template('relatorio.html')

@bp.route('/api/creditor_accounts')
def creditor_accounts():
    creditor_id = request.args.get('creditor_id')
    status = request.args.get('status')
    valid_statuses = ['paga', 'atrazo', 'devendo']
    if status not in valid_statuses:
        return jsonify({'error': 'Status inválido'}), 400
    accounts = Title.query.filter(Title.creditor_id == creditor_id, Title.status == status).all()
    return jsonify([t.serialize() for t in accounts])

@bp.route('/api/creditors')
def creditors():
    creditors = Credor.query.all()
    return jsonify([c.serialize() for c in creditors])


@bp.route('/api/accounts_to_pay')
def accounts_to_pay():
    start_year = int(request.args.get('start_year'))
    start_month = int(request.args.get('start_month'))
    end_year = int(request.args.get('end_year'))
    end_month = int(request.args.get('end_month'))
    

    accounts = Title.query.filter(
        Title.status == 'devendo',
        ((Title.year > start_year) | 
         ((Title.year == start_year) & (Title.month >= start_month))),
        ((Title.year < end_year) | 
         ((Title.year == end_year) & (Title.month <= end_month)))
    ).all()
    
    return jsonify([t.serialize() for t in accounts])

@bp.route('/api/paid_accounts')
def paid_accounts():
    start_year = int(request.args.get('start_year'))
    start_month = int(request.args.get('start_month'))
    end_year = int(request.args.get('end_year'))
    end_month = int(request.args.get('end_month'))
    
    accounts = Title.query.filter(
        Title.status == 'paga',
        (Title.year > start_year) | 
        ((Title.year == start_year) & (Title.month >= start_month)),
        (Title.year < end_year) | 
        ((Title.year == end_year) & (Title.month <= end_month))
    ).all()
    
    return jsonify([t.serialize() for t in accounts])
