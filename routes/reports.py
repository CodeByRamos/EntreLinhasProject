from flask import Blueprint, request, jsonify, session
import database as db

# Criação do Blueprint para as rotas de reports
reports = Blueprint('reports', __name__)

@reports.route('/api/report', methods=['POST'])
def reportar_post():
    """Rota para reportar um post."""
    try:
        data = request.get_json()
        post_id = data.get('post_id')
        reason = data.get('reason', 'Conteúdo inadequado')
        
        if not post_id:
            return jsonify({'success': False, 'message': 'ID do post é obrigatório.'}), 400
        
        # Verificar se o post existe
        post = db.get_post(post_id)
        if not post:
            return jsonify({'success': False, 'message': 'Post não encontrado.'}), 404
        
        # Criar o report
        success = db.report_post(post_id, reason)
        
        if success:
            return jsonify({
                'success': True, 
                'message': 'Post reportado com sucesso.'
            })
        else:
            return jsonify({'success': False, 'message': 'Erro ao reportar post.'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'message': 'Erro interno do servidor.'}), 500

@reports.route('/api/report_comment/<int:comment_id>', methods=['POST'])
def reportar_comentario(comment_id):
    """Rota para reportar um comentário."""
    try:
        data = request.get_json()
        reason = data.get('reason', 'Conteúdo inadequado')
        
        # Verificar se o comentário existe
        comment = db.get_comment_by_id(comment_id)
        if not comment:
            return jsonify({'success': False, 'message': 'Comentário não encontrado.'}), 404
        
        # Criar o report do comentário
        success = db.report_comment(comment_id, reason)
        
        if success:
            return jsonify({
                'success': True, 
                'message': 'Comentário reportado com sucesso.'
            })
        else:
            return jsonify({'success': False, 'message': 'Erro ao reportar comentário.'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'message': 'Erro interno do servidor.'}), 500

@reports.route('/admin/reports', methods=['GET'])
def listar_reports():
    """Rota para listar todos os reports de posts (admin)."""
    try:
        reports_list = db.get_reports()
        
        return jsonify({
            'success': True,
            'reports': [dict(report) for report in reports_list]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': 'Erro interno do servidor.'}), 500

@reports.route('/admin/comment-reports', methods=['GET'])
def listar_reports_comentarios():
    """Rota para listar todos os reports de comentários (admin)."""
    try:
        reports_list = db.get_comment_reports()
        
        return jsonify({
            'success': True,
            'reports': [dict(report) for report in reports_list]
        })
    except Exception as e:
        return jsonify({'success': False, 'message': 'Erro interno do servidor.'}), 500

@reports.route('/admin/reports/<int:report_id>/resolve', methods=['POST'])
def resolver_report(report_id):
    """Rota para resolver um report de post (admin)."""
    try:
        success = db.resolve_report(report_id)
        
        if success:
            return jsonify({
                'success': True, 
                'message': 'Report resolvido com sucesso.'
            })
        else:
            return jsonify({'success': False, 'message': 'Erro ao resolver report.'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'message': 'Erro interno do servidor.'}), 500

@reports.route('/admin/comment-reports/<int:report_id>/resolve', methods=['POST'])
def resolver_report_comentario(report_id):
    """Rota para resolver um report de comentário (admin)."""
    try:
        success = db.resolve_comment_report(report_id)
        
        if success:
            return jsonify({
                'success': True, 
                'message': 'Report de comentário resolvido com sucesso.'
            })
        else:
            return jsonify({'success': False, 'message': 'Erro ao resolver report de comentário.'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'message': 'Erro interno do servidor.'}), 500

@reports.route('/admin/reports/<int:report_id>/remove', methods=['DELETE'])
def remover_report(report_id):
    """Rota para remover um report de post (admin)."""
    try:
        success = db.remove_report(report_id)
        
        if success:
            return jsonify({
                'success': True, 
                'message': 'Report removido com sucesso.'
            })
        else:
            return jsonify({'success': False, 'message': 'Erro ao remover report.'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'message': 'Erro interno do servidor.'}), 500

@reports.route('/admin/comment-reports/<int:report_id>/remove', methods=['DELETE'])
def remover_report_comentario(report_id):
    """Rota para remover um report de comentário (admin)."""
    try:
        success = db.remove_comment_report(report_id)
        
        if success:
            return jsonify({
                'success': True, 
                'message': 'Report de comentário removido com sucesso.'
            })
        else:
            return jsonify({'success': False, 'message': 'Erro ao remover report de comentário.'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'message': 'Erro interno do servidor.'}), 500

