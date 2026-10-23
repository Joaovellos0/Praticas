/**
 * MÙSIC Shop - JavaScript Global
 * Gerenciamento de Modal de Login, Toasts de Notificação, Integração AJAX do Carrinho
 * e Barra de Pesquisa com Autocomplete em Tempo Real (JS Vanilla)
 */

document.addEventListener('DOMContentLoaded', function () {
    initUserModal();
    initCartAjax();
    initAutoDismissDjangoToasts();
    initSearchAutocomplete();
    initBackToTop();
    initSmoothScrollVitrine();
});

/* ==========================================================================
   1. Barra de Pesquisa Funcional com Autocomplete em Tempo Real (JS Vanilla)
   ========================================================================== */
function initSearchAutocomplete() {
    const searchInput = document.getElementById('search');
    const searchDropdown = document.getElementById('search_dropdown');
    const searchClearBtn = document.getElementById('search_clear');

    if (!searchInput || !searchDropdown) return;

    let debounceTimer = null;
    let currentResults = [];
    let selectedIndex = -1;

    // Escuta evento de digitação com debounce
    searchInput.addEventListener('input', function () {
        const query = this.value.trim();

        // Controla botão de limpar
        if (searchClearBtn) {
            searchClearBtn.style.display = query.length > 0 ? 'inline-block' : 'none';
        }

        clearTimeout(debounceTimer);

        if (query.length < 2) {
            closeDropdown();
            return;
        }

        // Exibe loading sutil no dropdown
        showLoading(query);

        debounceTimer = setTimeout(() => {
            fetchResults(query);
        }, 220);
    });

    // Botão de limpar busca
    if (searchClearBtn) {
        searchClearBtn.addEventListener('click', function () {
            searchInput.value = '';
            this.style.display = 'none';
            closeDropdown();
            searchInput.focus();
        });
    }

    // Navegação via Teclado (ArrowDown, ArrowUp, Enter, Escape)
    searchInput.addEventListener('keydown', function (e) {
        if (!searchDropdown.classList.contains('active')) {
            if (e.key === 'Enter' && searchInput.value.trim().length >= 2) {
                e.preventDefault();
                // Tenta buscar e ir ao primeiro resultado
                fetchDirectMatch(searchInput.value.trim());
            }
            return;
        }

        const items = searchDropdown.querySelectorAll('.search_dropdown_item');
        if (!items.length) return;

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            selectedIndex = (selectedIndex + 1) % items.length;
            updateHighlight(items);
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            selectedIndex = (selectedIndex - 1 + items.length) % items.length;
            updateHighlight(items);
        } else if (e.key === 'Enter') {
            e.preventDefault();
            if (selectedIndex >= 0 && selectedIndex < currentResults.length) {
                window.location.href = currentResults[selectedIndex].url;
            } else if (currentResults.length > 0) {
                // Direciona para o primeiro produto correspondente
                window.location.href = currentResults[0].url;
            }
        } else if (e.key === 'Escape') {
            closeDropdown();
        }
    });

    // Reabre ao focar se já houver texto válido
    searchInput.addEventListener('focus', function () {
        if (this.value.trim().length >= 2 && currentResults.length > 0) {
            searchDropdown.classList.add('active');
        }
    });

    // Fecha ao clicar fora do componente de busca
    document.addEventListener('click', function (e) {
        if (!e.target.closest('.searchbar_wrapper')) {
            closeDropdown();
        }
    });

    function showLoading(query) {
        selectedIndex = -1;
        searchDropdown.innerHTML = `
            <div class="search_dropdown_loading">
                <i class="fa-solid fa-spinner fa-spin"></i>
                <span>Buscando "${escapeHTML(query)}"...</span>
            </div>
        `;
        searchDropdown.classList.add('active');
    }

    function fetchResults(query) {
        fetch(`/api/busca-guitarras/?q=${encodeURIComponent(query)}`)
            .then((res) => {
                if (!res.ok) throw new Error('Erro na requisição');
                return res.json();
            })
            .then((data) => {
                currentResults = data.resultados || [];
                renderResults(currentResults, query);
            })
            .catch((err) => {
                console.error('Erro no autocomplete:', err);
                searchDropdown.innerHTML = `
                    <div class="search_dropdown_empty">
                        <i class="fa-solid fa-triangle-exclamation"></i>
                        <span>Não foi possível carregar as sugestões.</span>
                    </div>
                `;
            });
    }

    function fetchDirectMatch(query) {
        fetch(`/api/busca-guitarras/?q=${encodeURIComponent(query)}`)
            .then((res) => res.json())
            .then((data) => {
                if (data.resultados && data.resultados.length > 0) {
                    window.location.href = data.resultados[0].url;
                } else {
                    window.showToast(`Nenhuma guitarra encontrada para "${query}".`, 'info');
                }
            })
            .catch(() => {
                window.location.href = `/#vitrine`;
            });
    }

    function renderResults(results, query) {
        selectedIndex = -1;

        if (!results.length) {
            searchDropdown.innerHTML = `
                <div class="search_dropdown_empty">
                    <i class="fa-solid fa-magnifying-glass"></i>
                    <span>Nenhuma guitarra encontrada para "<strong>${escapeHTML(query)}</strong>"</span>
                </div>
            `;
            searchDropdown.classList.add('active');
            return;
        }

        let html = `
            <div class="search_dropdown_header">
                <span>Guitarras Encontradas (${results.length})</span>
            </div>
            <ul class="search_dropdown_list" role="listbox">
        `;

        results.forEach((item, index) => {
            const thumbHtml = item.imagem_url
                ? `<img src="${item.imagem_url}" alt="${escapeHTML(item.nome_completo)}">`
                : `<i class="fa-solid fa-guitar"></i>`;

            html += `
                <li class="search_dropdown_item" data-index="${index}" role="option" tabindex="-1">
                    <div class="search_item_thumb">
                        ${thumbHtml}
                    </div>
                    <div class="search_item_details">
                        <span class="search_item_brand">${escapeHTML(item.marca)}</span>
                        <span class="search_item_title">${escapeHTML(item.modelo)}</span>
                    </div>
                    <div class="search_item_price">
                        ${escapeHTML(item.preco_formatado)}
                    </div>
                </li>
            `;
        });

        html += `
            </ul>
            <div class="search_dropdown_footer">
                <span>Clique ou pressione <kbd>Enter</kbd> para abrir</span>
                <span><kbd>&uarr;</kbd> <kbd>&darr;</kbd> navegar</span>
            </div>
        `;

        searchDropdown.innerHTML = html;
        searchDropdown.classList.add('active');

        // Adiciona evento de clique a cada item do resultado
        const items = searchDropdown.querySelectorAll('.search_dropdown_item');
        items.forEach((itemEl) => {
            itemEl.addEventListener('click', function () {
                const idx = parseInt(this.dataset.index, 10);
                if (results[idx]) {
                    window.location.href = results[idx].url;
                }
            });
        });
    }

    function updateHighlight(items) {
        items.forEach((item, i) => {
            if (i === selectedIndex) {
                item.classList.add('highlighted');
                item.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
            } else {
                item.classList.remove('highlighted');
            }
        });
    }

    function closeDropdown() {
        searchDropdown.classList.remove('active');
        selectedIndex = -1;
    }

    function escapeHTML(str) {
        return str.replace(/[&<>'"]/g, 
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag] || tag)
        );
    }
}

/* ==========================================================================
   2. Modal de Login Overlay
   ========================================================================== */
function initUserModal() {
    const userBtn = document.getElementById('user_btn');
    const userModal = document.getElementById('user_menu');
    const closeBtn = document.getElementById('modal_close_btn');

    if (!userModal) return;

    function openModal() {
        userModal.classList.add('active');
        userModal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        const firstInput = userModal.querySelector('input');
        if (firstInput) setTimeout(() => firstInput.focus(), 150);
    }

    function closeModal() {
        userModal.classList.remove('active');
        userModal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    }

    if (userBtn) {
        userBtn.addEventListener('click', function (e) {
            e.preventDefault();
            openModal();
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', function () {
            closeModal();
        });
    }

    userModal.addEventListener('click', function (e) {
        if (e.target === userModal) {
            closeModal();
        }
    });

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && userModal.classList.contains('active')) {
            closeModal();
        }
    });
}

/* ==========================================================================
   3. Toasts de Feedback Flutuantes
   ========================================================================== */
window.showToast = function (message, type = 'success') {
    let container = document.getElementById('toast_container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast_container';
        container.className = 'toast_container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `toast_item toast_${type}`;

    let iconClass = 'fa-circle-check';
    if (type === 'error') iconClass = 'fa-circle-xmark';
    if (type === 'info') iconClass = 'fa-circle-info';

    toast.innerHTML = `
        <div class="toast_content">
            <i class="fa-solid ${iconClass}"></i>
            <span>${message}</span>
        </div>
        <button class="toast_close" type="button" aria-label="Fechar notificação">&times;</button>
    `;

    const closeBtn = toast.querySelector('.toast_close');
    closeBtn.addEventListener('click', () => {
        dismissToast(toast);
    });

    container.appendChild(toast);

    setTimeout(() => {
        dismissToast(toast);
    }, 3800);
};

function dismissToast(toast) {
    if (!toast || toast.dataset.dismissed) return;
    toast.dataset.dismissed = 'true';
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 300);
}

function initAutoDismissDjangoToasts() {
    const existingToasts = document.querySelectorAll('.toast_container .toast_item');
    existingToasts.forEach((toast) => {
        setTimeout(() => {
            dismissToast(toast);
        }, 4000);
    });
}

/* ==========================================================================
   4. Adicionar ao Carrinho via AJAX com Badge Dinâmico e Checagem de Autenticação
   ========================================================================== */
function initCartAjax() {
    document.addEventListener('click', function (e) {
        const btn = e.target.closest('.btn_add_to_cart');
        if (!btn) return;

        e.preventDefault();
        
        // Verifica se o usuário está autenticado
        const isAuthenticated = document.body.dataset.authenticated === 'true';
        if (!isAuthenticated) {
            const carrinhoUrl = document.body.dataset.carrinhoUrl || '/carrinho/';
            window.location.href = carrinhoUrl;
            return;
        }

        // Localiza a URL a partir do atributo href ou do formulário pai
        const form = btn.closest('form');
        let url = btn.getAttribute('href');
        let method = 'GET';
        let bodyData = null;

        if (!url && form) {
            url = form.getAttribute('action');
            method = 'POST';
            const formData = new FormData(form);
            formData.append('ajax', '1');
            bodyData = formData;
        }

        if (!url) return;

        const originalText = btn.innerHTML;
        const isIconOnly = btn.classList.contains('btn_cart_quick');
        
        if (isIconOnly) {
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
        } else {
            btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> ADICIONANDO...';
        }
        btn.style.pointerEvents = 'none';

        let fetchOptions = {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        };

        let requestUrl = url;
        if (method === 'POST' && bodyData) {
            fetchOptions.method = 'POST';
            fetchOptions.body = bodyData;
        } else {
            const separator = url.includes('?') ? '&' : '?';
            requestUrl = `${url}${separator}ajax=1`;
        }

        fetch(requestUrl, fetchOptions)
            .then((response) => response.json())
            .then((data) => {
                if (data.status === 'success') {
                    updateCartBadge(data.total_items);
                    window.showToast(data.message || 'Produto adicionado ao carrinho!', 'success');
                } else {
                    window.showToast('Não foi possível adicionar o produto.', 'error');
                }
            })
            .catch((err) => {
                console.error('Erro na requisição do carrinho:', err);
                if (method === 'POST' && form) {
                    form.submit();
                } else {
                    window.location.href = url;
                }
            })
            .finally(() => {
                btn.innerHTML = originalText;
                btn.style.pointerEvents = '';
            });
    });
}

function updateCartBadge(count) {
    const badge = document.getElementById('cart_badge');
    if (!badge) return;

    badge.textContent = count;
    if (count > 0) {
        badge.style.display = 'flex';
        badge.style.animation = 'none';
        badge.offsetHeight; /* Trigger reflow */
        badge.style.animation = 'badgePop 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
    } else {
        badge.style.display = 'none';
    }
}

/* ==========================================================================
   5. Botão "Voltar ao Topo" (Back to Top)
   Posicionado no canto inferior esquerdo. Aparece suavemente quando o
   header principal sai de vista e some quando o header volta a ser visível.
   ========================================================================== */
function initBackToTop() {
    const backToTopBtn = document.getElementById('back_to_top_btn');
    if (!backToTopBtn) return;

    // Localiza o header da página (seja .header_standard ou .hero_conteiner)
    const headerEl = document.querySelector('.header_standard') || document.querySelector('.header_conteiner');

    function checkVisibility() {
        let triggerDistance = 250;
        if (headerEl) {
            const rect = headerEl.getBoundingClientRect();
            // O header saiu de vista se sua borda inferior for menor ou igual a 0
            if (rect.bottom <= 0) {
                backToTopBtn.classList.add('visible');
            } else {
                backToTopBtn.classList.remove('visible');
            }
        } else {
            if (window.pageYOffset > triggerDistance) {
                backToTopBtn.classList.add('visible');
            } else {
                backToTopBtn.classList.remove('visible');
            }
        }
    }

    window.addEventListener('scroll', checkVisibility, { passive: true });
    window.addEventListener('resize', checkVisibility, { passive: true });
    checkVisibility();

    backToTopBtn.addEventListener('click', function (e) {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

/* ==========================================================================
   6. Correção do Efeito de Rolagem Suave para a Vitrine
   Executado exclusivamente se a seção #vitrine existir no DOM atual.
   Se o usuário estiver em outra página, o link padrão navega normalmente
   para a home trazendo o foco para a vitrine.
   ========================================================================== */
function initSmoothScrollVitrine() {
    // Escuta cliques em links que apontem para #vitrine
    document.addEventListener('click', function (e) {
        const link = e.target.closest('a[href*="#vitrine"]');
        if (!link) return;

        const vitrineSection = document.getElementById('vitrine');

        // Se a seção da vitrine existir no DOM atual (ex: na Home)
        if (vitrineSection) {
            e.preventDefault();
            const headerOffset = 100;
            const elementPosition = vitrineSection.getBoundingClientRect().top + window.pageYOffset;
            const offsetPosition = elementPosition - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });

            // Atualiza a URL sem recarregar
            if (window.history && window.history.pushState) {
                window.history.pushState(null, null, '#vitrine');
            }
        }
        // Se a vitrine NÃO existir nesta página (ex: Carrinho, Detalhes, Login),
        // deixa o comportamento normal do link seguir (ex: href="{% url 'home' %}#vitrine")
    });

    // Se a página atual foi carregada diretamente com o hash #vitrine e a seção existe
    if (window.location.hash === '#vitrine') {
        const vitrineSection = document.getElementById('vitrine');
        if (vitrineSection) {
            setTimeout(() => {
                const headerOffset = 100;
                const elementPosition = vitrineSection.getBoundingClientRect().top + window.pageYOffset;
                const offsetPosition = elementPosition - headerOffset;
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }, 100);
        }
    }
}
