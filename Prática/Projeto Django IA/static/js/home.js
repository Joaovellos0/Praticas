/**
 * MÙSIC Shop - JavaScript Home
 * 1. Vitrine em Carrossel Estilo Ibanez Dinâmico (filtro por marcas e paginação sem rolagem de tela)
 * 2. Carrossel Rotativo Infinito de Banners em Destaque (autoplay suave de 4.5s e navegação por setas/dots)
 */

document.addEventListener('DOMContentLoaded', function () {
    initBannerCarousel();
    initVitrineShowcase();
});

/* ==========================================================================
   Carrossel Rotativo Infinito de Banners
   ========================================================================== */
function initBannerCarousel() {
    const bannerCarousel = document.getElementById('banner_carousel');
    if (!bannerCarousel) return;

    const slides = bannerCarousel.querySelectorAll('.banner_slide');
    const prevBtn = document.getElementById('banner_prev_btn');
    const nextBtn = document.getElementById('banner_next_btn');
    const dots = bannerCarousel.querySelectorAll('.banner_dot');

    if (slides.length <= 1) return;

    let currentIndex = 0;
    const totalSlides = slides.length;
    let autoplayTimer = null;
    const autoplayInterval = 4500; // 4.5 segundos por slide
    let isTransitioning = false;

    function showSlide(newIndex, direction = 'next') {
        if (isTransitioning || newIndex === currentIndex) return;
        isTransitioning = true;

        const currentSlide = slides[currentIndex];
        const nextSlide = slides[newIndex];

        // Animação de saída do slide atual
        currentSlide.classList.remove('active');
        if (direction === 'next') {
            currentSlide.classList.add('slide_out_left');
        } else {
            currentSlide.style.transform = 'translateX(60px)';
        }

        // Prepara slide de entrada
        nextSlide.style.transform = direction === 'next' ? 'translateX(60px)' : 'translateX(-60px)';
        void nextSlide.offsetWidth; // Dispara reflow do DOM

        nextSlide.classList.remove('slide_out_left');
        nextSlide.classList.add('active');
        nextSlide.style.transform = 'translateX(0)';

        // Atualiza indicadores (dots)
        dots.forEach((dot, idx) => {
            if (idx === newIndex) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });

        setTimeout(() => {
            currentSlide.classList.remove('slide_out_left');
            currentSlide.style.transform = '';
            currentIndex = newIndex;
            isTransitioning = false;
        }, 650);
    }

    function nextSlide() {
        const nextIdx = (currentIndex + 1) % totalSlides;
        showSlide(nextIdx, 'next');
    }

    function prevSlide() {
        const prevIdx = (currentIndex - 1 + totalSlides) % totalSlides;
        showSlide(prevIdx, 'prev');
    }

    function startAutoplay() {
        stopAutoplay();
        autoplayTimer = setInterval(nextSlide, autoplayInterval);
    }

    function stopAutoplay() {
        if (autoplayTimer) {
            clearInterval(autoplayTimer);
            autoplayTimer = null;
        }
    }

    // Eventos dos botões de controle
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            nextSlide();
            startAutoplay();
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            prevSlide();
            startAutoplay();
        });
    }

    // Eventos dos dots
    dots.forEach((dot) => {
        dot.addEventListener('click', function () {
            const targetIdx = parseInt(this.dataset.index, 10);
            if (!isNaN(targetIdx) && targetIdx !== currentIndex) {
                const dir = targetIdx > currentIndex ? 'next' : 'prev';
                showSlide(targetIdx, dir);
                startAutoplay();
            }
        });
    });

    // Pausa no hover para leitura agradável do usuário
    bannerCarousel.addEventListener('mouseenter', stopAutoplay);
    bannerCarousel.addEventListener('mouseleave', startAutoplay);

    // Inicia autoplay contínuo infinito
    startAutoplay();
}

/* ==========================================================================
   Vitrine em Carrossel Dinâmica Estilo Ibanez
   ========================================================================== */
function initVitrineShowcase() {
    const filterBtns = document.querySelectorAll('.vitrine_filter_btn');
    const brandBlocks = document.querySelectorAll('.vitrine_brand_block');
    const paginationContainer = document.getElementById('vitrine_pagination');
    const arrowPrev = document.getElementById('vitrine_arrow_prev');
    const arrowNext = document.getElementById('vitrine_arrow_next');

    if (!filterBtns.length || !brandBlocks.length || !paginationContainer) return;

    let currentMarcaId = null;
    let currentPage = 1;
    let totalPages = 1;

    // Escuta cliques nas setas das extremidades
    if (arrowPrev) {
        arrowPrev.addEventListener('click', () => {
            if (currentPage > 1) {
                goToPage(currentPage - 1);
            }
        });
    }

    if (arrowNext) {
        arrowNext.addEventListener('click', () => {
            if (currentPage < totalPages) {
                goToPage(currentPage + 1);
            }
        });
    }

    // 1. Alternância de Marca pelo Filtro
    filterBtns.forEach((btn) => {
        btn.addEventListener('click', function () {
            if (this.classList.contains('active')) return;

            // Atualiza botões do filtro com animação fluida
            filterBtns.forEach((b) => b.classList.remove('active'));
            this.classList.add('active');

            const marcaId = this.dataset.marcaId;
            selectMarca(marcaId);
        });
    });

    function selectMarca(marcaId) {
        currentMarcaId = marcaId;
        currentPage = 1;

        // Ativa o bloco da marca selecionada e calcula dinamicamente as páginas
        brandBlocks.forEach((block) => {
            if (block.dataset.marcaId === marcaId) {
                block.classList.add('active');
                
                // Calcula dinamicamente quantas páginas existem neste bloco (sem travas ou limites fixos)
                const pages = block.querySelectorAll('.vitrine_page');
                totalPages = pages.length;
                block.dataset.totalPages = totalPages;
                
                showPage(block, 1);
            } else {
                block.classList.remove('active');
            }
        });

        // Atualiza estado das setas de borda e indicadores de página
        updateEdgeArrows();
        renderIndicators();
    }

    function showPage(block, pageNum) {
        const pages = block.querySelectorAll('.vitrine_page');
        pages.forEach((page) => {
            const p = parseInt(page.dataset.page, 10);
            if (p === pageNum) {
                // Remove e readiciona a classe 'active' com reflow para re-disparar a animação fluida dos cards
                page.classList.remove('active');
                void page.offsetWidth; // Dispara reflow para reiniciar animação CSS dos cards
                page.classList.add('active');
            } else {
                page.classList.remove('active');
            }
        });
    }

    function updateEdgeArrows() {
        if (!arrowPrev || !arrowNext) return;

        if (totalPages <= 1) {
            arrowPrev.style.display = 'none';
            arrowNext.style.display = 'none';
        } else {
            arrowPrev.style.display = 'inline-flex';
            arrowNext.style.display = 'inline-flex';
            arrowPrev.disabled = currentPage === 1;
            arrowNext.disabled = currentPage === totalPages;
        }
    }

    // 2. Renderização dos Indicadores de Página (Estilo dos filtros de marca, tamanho compacto)
    function renderIndicators() {
        paginationContainer.innerHTML = '';

        // Se tiver apenas 1 página ou menos, não há necessidade de indicadores
        if (totalPages <= 1) {
            return;
        }

        // Botões Numéricos servindo exclusivamente como indicadores visuais da página atual
        for (let i = 1; i <= totalPages; i++) {
            const indicator = document.createElement('button');
            indicator.className = `vitrine_page_indicator ${i === currentPage ? 'active' : ''}`;
            indicator.textContent = i;
            indicator.dataset.page = i;
            indicator.type = 'button';
            indicator.title = `Página ${i} de ${totalPages}`;
            indicator.setAttribute('aria-label', `Página ${i} de ${totalPages}`);
            // Permite também alternar para a página ao clicar no indicador para máxima flexibilidade
            indicator.addEventListener('click', () => {
                goToPage(i);
            });
            paginationContainer.appendChild(indicator);
        }
    }

    function goToPage(pageNum) {
        if (pageNum < 1 || pageNum > totalPages) return;
        currentPage = pageNum;
        
        const activeBlock = document.querySelector(`.vitrine_brand_block[data-marca-id="${currentMarcaId}"]`);
        if (activeBlock) {
            showPage(activeBlock, pageNum);
        }
        updateEdgeArrows();
        renderIndicators();
    }

    // Inicialização com a primeira marca ativa
    const initialActiveBtn = document.querySelector('.vitrine_filter_btn.active') || filterBtns[0];
    if (initialActiveBtn) {
        initialActiveBtn.classList.add('active');
        selectMarca(initialActiveBtn.dataset.marcaId);
    }
}
