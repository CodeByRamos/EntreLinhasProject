// Arquivo JavaScript para gerenciar comentários

document.addEventListener('DOMContentLoaded', function() {
    // Carrega os comentários para cada post
    const commentContainers = document.querySelectorAll('.comments-container');
    commentContainers.forEach(container => {
        const postId = container.dataset.postId;
        loadComments(postId);
    });
    
    // Configura os formulários de comentários
    const commentForms = document.querySelectorAll('.comment-form');
    commentForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const postId = this.dataset.postId;
            const textarea = this.querySelector('textarea');
            const commentText = textarea.value.trim();
            
            if (commentText) {
                submitComment(postId, commentText, textarea);
            }
        });
    });
});

/**
 * Carrega os comentários para um post específico
 * @param {string} postId - ID do post
 */
function loadComments(postId) {
    fetch(`/api/comments/${postId}`)
        .then(response => response.json())
        .then(data => {
            const container = document.querySelector(`.comments-container[data-post-id="${postId}"]`);
            
            if (data.comments && data.comments.length > 0) {
                container.innerHTML = '';
                
                data.comments.forEach(comment => {
                    container.appendChild(createCommentElement(comment));
                });
            } else {
                container.innerHTML = '<p class="text-gray-500 dark:text-gray-400 text-sm">Nenhum comentário ainda. Seja o primeiro a comentar!</p>';
            }
        })
        .catch(error => {
            console.error('Erro ao carregar comentários:', error);
            const container = document.querySelector(`.comments-container[data-post-id="${postId}"]`);
            container.innerHTML = '<p class="text-red-500 dark:text-red-400 text-sm">Erro ao carregar comentários. Tente novamente mais tarde.</p>';
        });
}

/**
 * Envia um novo comentário
 * @param {string} postId - ID do post
 * @param {string} commentText - Texto do comentário
 * @param {HTMLElement} textarea - Elemento textarea para limpar após envio
 */
function submitComment(postId, commentText, textarea) {
    // Desabilita o textarea durante o envio
    textarea.disabled = true;
    const originalPlaceholder = textarea.placeholder;
    textarea.placeholder = 'Enviando comentário...';
    
    fetch(`/api/comments/${postId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: commentText }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            
            if (data.comment) {
                const container = document.querySelector(`.comments-container[data-post-id="${postId}"]`);
                
                // Se for o primeiro comentário, limpa a mensagem "nenhum comentário"
                if (container.querySelector('p.text-gray-500')) {
                    container.innerHTML = '';
                }
                
                // Adiciona o novo comentário
                const commentElement = createCommentElement(data.comment);
                commentElement.classList.add('comentario-novo');
                container.appendChild(commentElement);
                
                // Limpa o textarea
                textarea.value = '';
                
                // Scroll para o novo comentário
                commentElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                
                // Feedback visual de sucesso
                commentElement.style.backgroundColor = '#dcfce7'; // verde claro
                setTimeout(() => {
                    commentElement.style.backgroundColor = '';
                }, 2000);
            }
        })
        .catch(error => {
            console.error('Erro ao enviar comentário:', error);
            alert(`Erro ao enviar comentário: ${error.message}`);
        })
        .finally(() => {
            // Reabilita o textarea
            textarea.disabled = false;
            textarea.placeholder = originalPlaceholder;
        });
}

/**
 * Cria um elemento HTML para um comentário
 * @param {Object} comment - Dados do comentário
 * @returns {HTMLElement} - Elemento div do comentário
 */
function createCommentElement(comment) {
    const div = document.createElement('div');
    div.className = 'comentario-container';
    div.dataset.commentId = comment.id;
    
    div.innerHTML = `
        <p class="text-gray-800 dark:text-gray-200 text-sm">${escapeHTML(comment.text)}</p>
        <div class="mt-2 text-xs text-gray-500 dark:text-gray-400">${comment.date}</div>
    `;
    
    return div;
}

/**
 * Escapa caracteres HTML para prevenir XSS
 * @param {string} unsafe - String não segura
 * @returns {string} - String escapada
 */
function escapeHTML(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

