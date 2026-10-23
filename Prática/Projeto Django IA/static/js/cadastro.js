/**
 * MÙSIC Shop - JavaScript da Página de Cadastro
 * Formatação de campos e Preenchimento Automático de Endereço via API ViaCEP
 */

document.addEventListener('DOMContentLoaded', function () {
    initTelefoneMask();
    initViaCepAutocomplete();
});

function initTelefoneMask() {
    const telInput = document.getElementById('cad_telefone');
    if (telInput) {
        telInput.addEventListener('input', function () {
            this.value = this.value.replace(/\D/g, '').slice(0, 9);
        });
    }
}

function initViaCepAutocomplete() {
    const cepInput = document.getElementById('id_cep');
    const logradouroInput = document.getElementById('cad_logradouro');
    const bairroInput = document.getElementById('cad_bairro');
    const cidadeInput = document.getElementById('cad_cidade');
    const estadoInput = document.getElementById('cad_estado');
    const numeroInput = document.getElementById('cad_numero');
    const spinner = document.getElementById('cep_spinner');
    const feedbackMsg = document.getElementById('cep_feedback');

    if (!cepInput) return;

    let lastSearchedCep = '';

    // Aplica máscara dinâmica de CEP: 00000-000
    cepInput.addEventListener('input', function () {
        let val = this.value.replace(/\D/g, '').slice(0, 8);
        if (val.length > 5) {
            this.value = val.slice(0, 5) + '-' + val.slice(5);
        } else {
            this.value = val;
        }

        if (val.length === 8 && val !== lastSearchedCep) {
            buscarEnderecoPorCep(val);
        } else if (val.length < 8) {
            hideFeedback();
        }
    });

    cepInput.addEventListener('blur', function () {
        let val = this.value.replace(/\D/g, '');
        if (val.length === 8 && val !== lastSearchedCep) {
            buscarEnderecoPorCep(val);
        }
    });

    function showLoading(show) {
        if (spinner) {
            spinner.style.display = show ? 'inline-flex' : 'none';
        }
        if (show) {
            cepInput.classList.add('loading');
        } else {
            cepInput.classList.remove('loading');
        }
    }

    function showFeedback(text, type = 'error') {
        if (!feedbackMsg) return;
        feedbackMsg.textContent = text;
        feedbackMsg.className = `cep_feedback_msg ${type}`;
        feedbackMsg.style.display = 'block';
    }

    function hideFeedback() {
        if (!feedbackMsg) return;
        feedbackMsg.style.display = 'none';
        feedbackMsg.textContent = '';
    }

    function limparCamposEndereco() {
        if (logradouroInput) logradouroInput.value = '';
        if (bairroInput) bairroInput.value = '';
        if (cidadeInput) cidadeInput.value = '';
        if (estadoInput) estadoInput.value = '';
    }

    function buscarEnderecoPorCep(cepClean) {
        lastSearchedCep = cepClean;
        showLoading(true);
        hideFeedback();

        fetch(`https://viacep.com.br/ws/${cepClean}/json/`)
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Falha na resposta do serviço de CEP');
                }
                return response.json();
            })
            .then((data) => {
                showLoading(false);

                if (data.erro) {
                    limparCamposEndereco();
                    showFeedback('CEP não encontrado. Por favor, confira os números digitados.', 'error');
                    cepInput.focus();
                    return;
                }

                // Preenchimento automático dos dados do endereço
                if (logradouroInput) logradouroInput.value = data.logradouro || '';
                if (bairroInput) bairroInput.value = data.bairro || '';
                if (cidadeInput) cidadeInput.value = data.localidade || '';
                if (estadoInput) estadoInput.value = data.uf || '';

                showFeedback('Endereço localizado com sucesso!', 'success');

                // Foco imediato no campo de Número para agilidade no checkout
                if (numeroInput) {
                    setTimeout(() => {
                        numeroInput.focus();
                    }, 120);
                }
            })
            .catch((err) => {
                showLoading(false);
                console.warn('Erro ao consultar ViaCEP:', err);
                showFeedback('Não foi possível consultar o CEP automaticamente. Digite o endereço manualmente.', 'warning');
            });
    }
}
