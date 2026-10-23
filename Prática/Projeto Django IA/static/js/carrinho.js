/**
 * MÙSIC Shop - JavaScript da Página de Carrinho
 * Atualização assíncrona de quantidades, exclusão dinâmica e recalculo de totais
 */

document.addEventListener('DOMContentLoaded', function () {
    initCartQuantityControls();
    initCartRemoveControls();
});

function initCartQuantityControls() {
    const rows = document.querySelectorAll('.carrinho_item_row');

    rows.forEach((row) => {
        const decreaseBtn = row.querySelector('.btn_decrease');
        const increaseBtn = row.querySelector('.btn_increase');
        const input = row.querySelector('.qty_input');

        if (!decreaseBtn || !increaseBtn || !input) return;

        const itemId = input.dataset.id;

        decreaseBtn.addEventListener('click', function () {
            let currentVal = parseInt(input.value, 10) || 1;
            if (currentVal > 1) {
                updateQuantity(itemId, 'decrease', input, row);
            } else {
                // Se for 1 e diminuir, pergunta se deseja remover
                if (confirm('Deseja remover este produto do carrinho?')) {
                    removeItem(itemId, row);
                }
            }
        });

        increaseBtn.addEventListener('click', function () {
            updateQuantity(itemId, 'increase', input, row);
        });
    });
}

function updateQuantity(itemId, action, inputElement, rowElement) {
    const url = `/carrinho/atualizar/${itemId}/?action=${action}&ajax=1`;

    fetch(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === 'success') {
                if (data.item_quantidade > 0) {
                    inputElement.value = data.item_quantidade;

                    const subtotalEl = rowElement.querySelector(`#subtotal_${itemId}`);
                    if (subtotalEl) {
                        subtotalEl.textContent = `R$ ${formatPrice(data.item_subtotal)}`;
                    }
                } else {
                    // Produto foi removido
                    rowElement.style.opacity = '0';
                    setTimeout(() => rowElement.remove(), 250);
                }

                // Atualiza resumo
                updateSummary(data.total_items, data.total_price);

                // Atualiza badge do header
                if (typeof window.showToast === 'function') {
                    // Atualiza badge global
                    const badge = document.getElementById('cart_badge');
                    if (badge) {
                        badge.textContent = data.total_items;
                        badge.style.display = data.total_items > 0 ? 'flex' : 'none';
                    }
                }

                if (data.total_items === 0) {
                    window.location.reload();
                }
            }
        })
        .catch((err) => {
            console.error('Erro ao atualizar quantidade:', err);
        });
}

function initCartRemoveControls() {
    const removeBtns = document.querySelectorAll('.btn_remove_item');

    removeBtns.forEach((btn) => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const itemId = this.dataset.id;
            const row = document.getElementById(`cart_row_${itemId}`);
            removeItem(itemId, row);
        });
    });
}

function removeItem(itemId, rowElement) {
    const url = `/carrinho/remover/${itemId}/?ajax=1`;

    fetch(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === 'success') {
                if (rowElement) {
                    rowElement.style.transition = 'all 0.3s ease';
                    rowElement.style.opacity = '0';
                    rowElement.style.transform = 'translateX(20px)';
                    setTimeout(() => {
                        rowElement.remove();
                        if (data.total_items === 0) {
                            window.location.reload();
                        }
                    }, 300);
                }

                updateSummary(data.total_items, data.total_price);

                const badge = document.getElementById('cart_badge');
                if (badge) {
                    badge.textContent = data.total_items;
                    badge.style.display = data.total_items > 0 ? 'flex' : 'none';
                }

                if (typeof window.showToast === 'function') {
                    window.showToast('Produto removido do carrinho.', 'info');
                }
            }
        })
        .catch((err) => {
            console.error('Erro ao remover produto:', err);
        });
}

function updateSummary(totalItems, totalPrice) {
    const totalItemsEl = document.getElementById('summary_total_items');
    const subtotalEl = document.getElementById('summary_subtotal');
    const totalPriceEl = document.getElementById('summary_total_price');

    if (totalItemsEl) totalItemsEl.textContent = totalItems;
    if (subtotalEl) subtotalEl.textContent = `R$ ${formatPrice(totalPrice)}`;
    if (totalPriceEl) totalPriceEl.textContent = `R$ ${formatPrice(totalPrice)}`;
}

function formatPrice(val) {
    return parseFloat(val).toLocaleString('pt-BR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    });
}
