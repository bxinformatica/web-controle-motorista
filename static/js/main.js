// Funções de formatação de moeda
function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(valor);
}

// Funções de formatação de data
function formatarData(data) {
    return new Intl.DateTimeFormat('pt-BR').format(new Date(data));
}

// Função para calcular consumo médio
function calcularConsumoMedio(kmRodados, litros) {
    return (kmRodados / litros).toFixed(2);
}

// Função para validar formulários
function validarFormulario(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.classList.add('is-invalid');
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Função para mostrar/esconder senha
function toggleSenha(inputId, buttonId) {
    const input = document.getElementById(inputId);
    const button = document.getElementById(buttonId);
    
    if (input.type === 'password') {
        input.type = 'text';
        button.innerHTML = '<i class="fas fa-eye-slash"></i>';
    } else {
        input.type = 'password';
        button.innerHTML = '<i class="fas fa-eye"></i>';
    }
}

// Função para confirmar exclusão
function confirmarExclusao(mensagem = 'Tem certeza que deseja excluir este item?') {
    return confirm(mensagem);
}

// Função para mostrar mensagens de alerta
function mostrarAlerta(mensagem, tipo = 'success') {
    const alertPlaceholder = document.getElementById('alertPlaceholder');
    if (!alertPlaceholder) return;
    
    const wrapper = document.createElement('div');
    wrapper.innerHTML = `
        <div class="alert alert-${tipo} alert-dismissible fade show" role="alert">
            ${mensagem}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    alertPlaceholder.append(wrapper);
    
    // Auto-remover após 5 segundos
    setTimeout(() => {
        wrapper.querySelector('.alert').remove();
    }, 5000);
}

// Função para calcular totais
function calcularTotais(valores) {
    return valores.reduce((acc, curr) => acc + (parseFloat(curr) || 0), 0);
}

// Função para formatar números
function formatarNumero(numero, decimais = 2) {
    return Number(numero).toFixed(decimais);
}

// Função para validar campos numéricos
function validarNumero(event) {
    const charCode = (event.which) ? event.which : event.keyCode;
    if (charCode > 31 && (charCode < 48 || charCode > 57) && charCode !== 46) {
        event.preventDefault();
        return false;
    }
    return true;
}

// Função para calcular diferença entre datas em dias
function calcularDiferencaDias(data1, data2) {
    const diffTime = Math.abs(new Date(data2) - new Date(data1));
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
}

// Função para formatar quilometragem
function formatarKm(km) {
    return `${Number(km).toLocaleString('pt-BR')} km`;
}

// Função para calcular próxima troca de óleo
function calcularProximaTrocaOleo(kmAtual, intervaloTroca = 5000) {
    return kmAtual + intervaloTroca;
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips do Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Inicializar popovers do Bootstrap
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Adicionar validação a todos os formulários
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validarFormulario(this)) {
                e.preventDefault();
                mostrarAlerta('Por favor, preencha todos os campos obrigatórios.', 'danger');
            }
        });
    });
    
    // Adicionar máscara de moeda a campos de valor
    document.querySelectorAll('.moeda').forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            value = (value/100).toFixed(2);
            e.target.value = formatarMoeda(value);
        });
    });
    
    // Adicionar máscara de data a campos de data
    document.querySelectorAll('.data').forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length >= 8) {
                const data = new Date(
                    value.substr(4, 4),
                    value.substr(2, 2) - 1,
                    value.substr(0, 2)
                );
                e.target.value = formatarData(data);
            }
        });
    });
}); 