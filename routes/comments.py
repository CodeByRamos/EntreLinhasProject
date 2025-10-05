from flask import Blueprint, request, jsonify
import database as db

# Criação do Blueprint para as rotas de comentários
comments = Blueprint('comments', __name__)

@comments.route('/api/comments/<int:post_id>', methods=['GET'])
def get_comments(post_id):
    """API para obter comentários de um post específico."""
    comments_list = db.get_comments(post_id)
    
    # Converte os objetos Row para dicionários
    comments_data = []
    for comment in comments_list:
        comments_data.append({
            'id': comment['id'],
            'text': comment['comment_text'],
            'date': comment['data_comentario']
        })
    
    return jsonify({'comments': comments_data})

@comments.route('/api/comments/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    """API para adicionar um comentário a um post."""
    data = request.json
    
    if not data or 'text' not in data or not data['text'].strip():
        return jsonify({'error': 'O comentário não pode estar vazio'}), 400
    
    comment_text = data['text'].strip()
    
    # Verifica se o post existe
    post = db.get_post(post_id)
    if not post:
        return jsonify({'error': 'Post não encontrado'}), 404
    
    # Cria o comentário no banco de dados
    comment_id = db.create_comment(post_id, comment_text)
    
    # Obtém o comentário recém-criado para retornar
    comments_list = db.get_comments(post_id)
    new_comment = None
    
    for comment in comments_list:
        if comment['id'] == comment_id:
            new_comment = {
                'id': comment['id'],
                'text': comment['comment_text'],
                'date': comment['data_comentario']
            }
            break
    
    return jsonify({'comment': new_comment})

