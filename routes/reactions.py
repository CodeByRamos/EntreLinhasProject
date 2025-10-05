from flask import Blueprint, request, jsonify, current_app
import database as db

# Criação do Blueprint para as rotas de reações
reactions = Blueprint('reactions', __name__)

@reactions.route('/api/reactions/<int:post_id>', methods=['GET'])
def get_reactions(post_id):
    """API para obter contagem de reações de um post específico."""
    # Verifica se o post existe
    post = db.get_post(post_id)
    if not post:
        return jsonify({'error': 'Post não encontrado'}), 404
    
    reaction_counts = db.get_reaction_counts(post_id)
    
    # Adiciona tipos de reação que ainda não têm contagem
    all_reactions = {}
    for reaction in current_app.config['REACOES']:
        reaction_type = reaction['valor']
        all_reactions[reaction_type] = reaction_counts.get(reaction_type, 0)
    
    return jsonify({'reactions': all_reactions})

@reactions.route('/api/reactions/<int:post_id>', methods=['POST'])
def add_reaction(post_id):
    """API para adicionar uma reação a um post."""
    data = request.json
    
    if not data or 'type' not in data:
        return jsonify({'error': 'Tipo de reação não especificado'}), 400
    
    reaction_type = data['type']
    
    # Verifica se o post existe
    post = db.get_post(post_id)
    if not post:
        return jsonify({'error': 'Post não encontrado'}), 404
    
    # Verifica se o tipo de reação é válido
    valid_reaction = False
    for reaction in current_app.config['REACOES']:
        if reaction['valor'] == reaction_type:
            valid_reaction = True
            break
    
    if not valid_reaction:
        return jsonify({'error': 'Tipo de reação inválido'}), 400
    
    # Adiciona a reação no banco de dados
    db.add_reaction(post_id, reaction_type)
    
    # Obtém a contagem atualizada de reações
    reaction_counts = db.get_reaction_counts(post_id)
    
    # Adiciona tipos de reação que ainda não têm contagem
    all_reactions = {}
    for reaction in current_app.config['REACOES']:
        reaction_type = reaction['valor']
        all_reactions[reaction_type] = reaction_counts.get(reaction_type, 0)
    
    return jsonify({'reactions': all_reactions})

