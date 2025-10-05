// Arquivo JavaScript para gerenciar reações

document.addEventListener('DOMContentLoaded', function() {
    // Carrega as reações para cada post
    const reactionContainers = document.querySelectorAll('[data-post-id]');
    reactionContainers.forEach(container => {
        if (container.classList.contains('reaction-buttons-container') || 
            container.querySelector('.reaction-buttons-container')) {
            const postId = container.dataset.postId;
            loadReactions(postId);
        }
    });
});

/**
 * Carrega as reações para um post específico
 * @param {string} postId - ID do post
 */
function loadReactions(postId) {
    fetch(`/api/reactions/${postId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const container = document.querySelector(`[data-post-id="${postId}"] .reaction-buttons-container`);
            if (!container) return;
            
            container.innerHTML = '';
            
            // Obtém as configurações de reações do servidor
            const reacoes = [
                { valor: 'te_entendo', nome: 'Te entendo', emoji: '🤝' },
                { valor: 'forca', nome: 'Força!', emoji: '💪' },
                { valor: 'abraco', nome: 'Abraço virtual', emoji: '🫂' },
                { valor: 'coracao', nome: 'Coração', emoji: '❤️' },
                { valor: 'inspirador', nome: 'Inspirador', emoji: '✨' }
            ];
            
            // Cria os botões de reação
            reacoes.forEach(reacao => {
                const count = data.reactions[reacao.valor] || 0;
                const button = createReactionButton(reacao, count, postId);
                container.appendChild(button);
            });
        })
        .catch(error => {
            console.error('Erro ao carregar reações:', error);
            const container = document.querySelector(`[data-post-id="${postId}"] .reaction-buttons-container`);
            if (container) {
                container.innerHTML = '<span class="text-sm text-red-500 dark:text-red-400">Erro ao carregar reações</span>';
            }
        });
}

/**
 * Cria um botão de reação
 * @param {Object} reacao - Dados da reação
 * @param {number} count - Contagem atual da reação
 * @param {string} postId - ID do post
 * @returns {HTMLElement} - Elemento button da reação
 */
function createReactionButton(reacao, count, postId) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'reacao-botao flex items-center space-x-1 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-full px-3 py-1 transition-all duration-300';
    button.dataset.reacao = reacao.valor;
    button.dataset.postId = postId;
    button.title = reacao.nome;
    
    button.innerHTML = `
        <span class="text-lg">${reacao.emoji}</span>
        <span class="text-xs font-medium text-gray-700 dark:text-gray-300">${count}</span>
    `;
    
    // Adiciona evento de clique
    button.addEventListener('click', function() {
        addReaction(postId, reacao.valor);
        
        // Efeito visual de clique
        this.classList.add('ativo');
        setTimeout(() => {
            this.classList.remove('ativo');
        }, 1000);
    });
    
    return button;
}

/**
 * Adiciona uma reação a um post
 * @param {string} postId - ID do post
 * @param {string} reactionType - Tipo de reação
 */
function addReaction(postId, reactionType) {
    fetch(`/api/reactions/${postId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ type: reactionType }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.reactions) {
                // Atualiza a contagem de reações nos botões
                Object.entries(data.reactions).forEach(([tipo, contagem]) => {
                    const button = document.querySelector(`button[data-reacao="${tipo}"][data-post-id="${postId}"]`);
                    if (button) {
                        const countSpan = button.querySelector('span:last-child');
                        if (countSpan) {
                            // Animação de incremento
                            const oldCount = parseInt(countSpan.textContent);
                            const newCount = contagem;
                            
                            if (newCount > oldCount) {
                                // Efeito visual de incremento
                                countSpan.classList.add('text-primary-600', 'dark:text-primary-400', 'font-bold');
                                setTimeout(() => {
                                    countSpan.classList.remove('text-primary-600', 'dark:text-primary-400', 'font-bold');
                                }, 1500);
                            }
                            
                            countSpan.textContent = newCount;
                        }
                    }
                });
            }
        })
        .catch(error => {
            console.error('Erro ao adicionar reação:', error);
            alert('Não foi possível adicionar sua reação. Tente novamente mais tarde.');
        });
}

