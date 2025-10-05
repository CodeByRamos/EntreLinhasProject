from flask import Blueprint, render_template, request, jsonify, current_app
import database as db

# Criação do Blueprint para as rotas de pesquisa
search = Blueprint('search', __name__)

@search.route('/pesquisar')
def pesquisar():
    """Rota para a página de pesquisa."""
    # Obter parâmetros de pesquisa e paginação
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Número de posts por página
    
    # Se não houver consulta, retornar página de pesquisa vazia
    if not query:
        return render_template('search.html', 
                              query='',
                              desabafos=[],
                              page=1,
                              total_pages=0)
    
    # Calcular o offset para paginação
    offset = (page - 1) * per_page
    
    # Obter resultados da pesquisa
    desabafos = db.search_posts(query, limit=per_page, offset=offset)
    total_posts = db.count_search_results(query)
    
    # Calcular número total de páginas
    total_pages = (total_posts + per_page - 1) // per_page  # Arredondamento para cima
    
    # Obter categorias e reações da configuração
    categorias = current_app.config['CATEGORIAS']
    reacoes = current_app.config['REACOES']
    
    # Preparar dados para cada post
    for post in desabafos:
        post_id = post['id']
        post['comments'] = db.get_comments(post_id)
        post['reaction_counts'] = db.get_reaction_counts(post_id)
    
    return render_template('search.html', 
                          query=query,
                          desabafos=desabafos,
                          categorias=categorias,
                          reacoes=reacoes,
                          page=page,
                          total_pages=total_pages,
                          total_results=total_posts)

@search.route('/api/pesquisar')
def api_pesquisar():
    """Rota para API de pesquisa (para uso com JavaScript)."""
    # Obter parâmetros de pesquisa e paginação
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Número de posts por página
    
    # Se não houver consulta, retornar resultados vazios
    if not query:
        return jsonify({
            'query': '',
            'results': [],
            'page': 1,
            'total_pages': 0,
            'total_results': 0
        })
    
    # Calcular o offset para paginação
    offset = (page - 1) * per_page
    
    # Obter resultados da pesquisa
    desabafos = db.search_posts(query, limit=per_page, offset=offset)
    total_posts = db.count_search_results(query)
    
    # Calcular número total de páginas
    total_pages = (total_posts + per_page - 1) // per_page  # Arredondamento para cima
    
    # Preparar dados para cada post
    for post in desabafos:
        post_id = post['id']
        post['comments'] = db.get_comments(post_id)
        post['reaction_counts'] = db.get_reaction_counts(post_id)
    
    return jsonify({
        'query': query,
        'results': desabafos,
        'page': page,
        'total_pages': total_pages,
        'total_results': total_posts
    })

