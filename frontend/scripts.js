// Configuração da API
const API_URL = "http://localhost:8000";
let turmas = [];
let alunos = [];

// Função para mostrar mensagens toast
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Função para mostrar/esconder loading
function toggleLoading(element, show = true) {
    if (show) {
        element.classList.add('loading');
        element.disabled = true;
    } else {
        element.classList.remove('loading');
        element.disabled = false;
    }
}

// Funções de API
async function fetchTurmas() {
    try {
        const response = await fetch(`${API_URL}/turmas`);
        if (!response.ok) throw new Error('Erro ao buscar turmas');
        turmas = await response.json();
        return turmas;
    } catch (error) {
        showToast('Erro ao carregar turmas', 'error');
        return [];
    }
}

async function fetchAlunos() {
    try {
        const response = await fetch(`${API_URL}/alunos`);
        if (!response.ok) throw new Error('Erro ao buscar alunos');
        alunos = await response.json();
        return alunos;
    } catch (error) {
        showToast('Erro ao carregar alunos', 'error');
        return [];
    }
}

async function criarAluno(dados) {
    try {
        const response = await fetch(`${API_URL}/alunos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });
        
        if (!response.ok) throw new Error('Erro ao criar aluno');
        
        showToast('Aluno criado com sucesso!');
        await fetchAlunos();
        renderizarAlunos();
        atualizarEstatisticas();
        
        // Fecha o modal
        document.getElementById('modalNovoAluno').classList.remove('active');
    } catch (error) {
        showToast('Erro ao criar aluno', 'error');
    }
}

// Funções de UI
function atualizarEstatisticas() {
    document.getElementById("totalAlunos").textContent = alunos.length;
    document.getElementById("alunosAtivos").textContent = alunos.filter(a => a.status === "ativo").length;
    
    const estatisticasTurma = turmas.map(t => {
        const alunosNaTurma = alunos.filter(a => a.turma_id === t.id).length;
        return `${t.nome}: ${alunosNaTurma}/${t.capacidade}`;
    }).join(", ");
    
    document.getElementById("alunosPorTurma").textContent = estatisticasTurma;
}

function preencherFiltros() {
    const turmaFiltro = document.getElementById("turmaFiltro");
    const turmaAluno = document.getElementById("turmaAluno");
    
    // Opções padrão
    const defaultOption = '<option value="">Todas</option>';
    const noneOption = '<option value="">Nenhuma</option>';
    
    // Opções de turmas
    const turmaOptions = turmas.map(t => {
        const alunosNaTurma = alunos.filter(a => a.turma_id === t.id).length;
        return `<option value="${t.id}">${t.nome} (${alunosNaTurma}/${t.capacidade})</option>`;
    }).join("");
    
    // Preencher selects
    turmaFiltro.innerHTML = defaultOption + turmaOptions;
    turmaAluno.innerHTML = noneOption + turmaOptions;
}

function renderizarAlunos() {
    const tbody = document.querySelector("#tabelaAlunos tbody");
    const filtroTurma = document.getElementById("turmaFiltro").value;
    const filtroStatus = document.getElementById("statusFiltro").value;
    const busca = document.getElementById("searchAluno").value.toLowerCase();
    
    // Filtrar alunos
    const alunosFiltrados = alunos.filter(aluno => {
        const matchTurma = !filtroTurma || aluno.turma_id === parseInt(filtroTurma);
        const matchStatus = !filtroStatus || aluno.status === filtroStatus;
        const matchBusca = !busca || 
            aluno.nome.toLowerCase().includes(busca) || 
            (aluno.email && aluno.email.toLowerCase().includes(busca));
        
        return matchTurma && matchStatus && matchBusca;
    });
    
    // Ordenar por nome
    alunosFiltrados.sort((a, b) => a.nome.localeCompare(b.nome));
    
    // Renderizar tabela
    tbody.innerHTML = alunosFiltrados.map(aluno => {
        const turma = turmas.find(t => t.id === aluno.turma_id);
        const statusClass = aluno.status === 'ativo' ? 'status-ativo' : 'status-inativo';
        
        return `
            <tr>
                <td>${aluno.nome}</td>
                <td>${aluno.data_nascimento || '-'}</td>
                <td>${aluno.email || '-'}</td>
                <td><span class="${statusClass}">${aluno.status}</span></td>
                <td>${turma ? turma.nome : '-'}</td>
                <td>
                    <button onclick="editarAluno(${aluno.id})" class="btn-editar">
                        Editar
                    </button>
                    <button onclick="confirmarRemocao(${aluno.id})" class="btn-remover">
                        Remover
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

// Event Listeners
document.getElementById('searchAluno').addEventListener('input', renderizarAlunos);
document.getElementById('turmaFiltro').addEventListener('change', renderizarAlunos);
document.getElementById('statusFiltro').addEventListener('change', renderizarAlunos);

// Modal Handlers
function abrirModal(id) {
    document.getElementById(id).classList.add('active');
}

function fecharModal(id) {
    document.getElementById(id).classList.remove('active');
}

// Form Handlers
document.getElementById('formNovoAluno').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const dados = Object.fromEntries(formData.entries());
    
    // Converter alguns campos
    dados.turma_id = dados.turma_id ? parseInt(dados.turma_id) : null;
    
    await criarAluno(dados);
});

// Confirmação de remoção
function confirmarRemocao(id) {
    if (confirm('Tem certeza que deseja remover este aluno?')) {
        removerAluno(id);
    }
}

// Inicialização
async function inicializar() {
    try {
        await Promise.all([
            fetchTurmas(),
            fetchAlunos()
        ]);
        
        preencherFiltros();
        renderizarAlunos();
        atualizarEstatisticas();
    } catch (error) {
        showToast('Erro ao inicializar aplicação', 'error');
    }
}

// Iniciar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', inicializar);
