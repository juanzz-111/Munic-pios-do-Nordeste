// ==========================================
// ELEMENTOS DA PÁGINA
// ==========================================

const formMunicipio = document.getElementById("formMunicipio");
const corpoTabela = document.getElementById("corpoTabela");
const totalMunicipios = document.getElementById("totalMunicipios");

const campoNome = document.getElementById("nome");
const campoIbge = document.getElementById("id_ibge");
const campoEstado = document.getElementById("estado");
const campoUF = document.getElementById("sigla_uf");
const campoCapital = document.getElementById("capital");
const campoPopulacao = document.getElementById("populacao_estimada");

const buscaNome = document.getElementById("buscaNome");
const filtroUF = document.getElementById("filtroUF");

const tituloFormulario = document.getElementById("tituloFormulario");
const btnSalvar = document.getElementById("btnSalvar");
const btnCancelar = document.getElementById("btnCancelar");
const mensagem = document.getElementById("mensagem");

// Guarda o nome original quando um município está sendo editado.
let municipioEmEdicao = null;


// ==========================================
// MOSTRAR MENSAGENS
// ==========================================

function mostrarMensagem(texto, tipo) {
    mensagem.textContent = texto;
    mensagem.className = "mensagem " + tipo;
}


// ==========================================
// CARREGAR MUNICÍPIOS
// ==========================================

async function carregarMunicipios() {
    corpoTabela.innerHTML = "";

    const linhaCarregamento = document.createElement("tr");
    const celulaCarregamento = document.createElement("td");

    celulaCarregamento.colSpan = 6;
    celulaCarregamento.className = "tabela-vazia";
    celulaCarregamento.textContent = "Carregando municípios...";

    linhaCarregamento.appendChild(celulaCarregamento);
    corpoTabela.appendChild(linhaCarregamento);

    try {
        const resposta = await fetch("/municipios");

        if (!resposta.ok) {
            throw new Error("Não foi possível carregar os municípios.");
        }

        const municipios = await resposta.json();

        exibirMunicipios(municipios);

    } catch (erro) {
        corpoTabela.innerHTML = "";

        const linhaErro = document.createElement("tr");
        const celulaErro = document.createElement("td");

        celulaErro.colSpan = 6;
        celulaErro.className = "tabela-vazia";
        celulaErro.textContent = erro.message;

        linhaErro.appendChild(celulaErro);
        corpoTabela.appendChild(linhaErro);
    }
}


// ==========================================
// EXIBIR MUNICÍPIOS NA TABELA
// ==========================================

function exibirMunicipios(municipios) {
    corpoTabela.innerHTML = "";

    const nomes = Object.keys(municipios);

    // Aplica a pesquisa pelo nome.
    const termoPesquisa = buscaNome.value.trim().toLowerCase();

    // Aplica o filtro pelo estado.
    const ufSelecionada = filtroUF.value;

    const nomesFiltrados = nomes.filter(nome => {
        const dados = municipios[nome];

        const correspondeNome = nome.toLowerCase().includes(termoPesquisa);
        const correspondeUF = !ufSelecionada || dados.sigla_uf === ufSelecionada;

        return correspondeNome && correspondeUF;
    });

    totalMunicipios.textContent = nomesFiltrados.length;

    if (nomesFiltrados.length === 0) {
        const linha = document.createElement("tr");
        const celula = document.createElement("td");

        celula.colSpan = 6;
        celula.className = "tabela-vazia";
        celula.textContent = "Nenhum município encontrado.";

        linha.appendChild(celula);
        corpoTabela.appendChild(linha);
        return;
    }

    nomesFiltrados.forEach(nome => {
        const dados = municipios[nome];

        const linha = document.createElement("tr");

        // Nome do município.
        const celulaNome = document.createElement("td");
        celulaNome.textContent = nome;

        // Sigla do estado.
        const celulaUF = document.createElement("td");
        celulaUF.textContent = dados.sigla_uf;

        // Informa se é capital.
        const celulaCapital = document.createElement("td");
        celulaCapital.textContent = dados.capital ? "Sim" : "Não";

        // População formatada.
        const celulaPopulacao = document.createElement("td");
        celulaPopulacao.textContent =
            Number(dados.populacao_estimada).toLocaleString("pt-BR");

        // Código IBGE.
        const celulaIbge = document.createElement("td");
        celulaIbge.textContent = dados.id_ibge;

        // Botões de ação.
        const celulaAcoes = document.createElement("td");
        const divAcoes = document.createElement("div");

        divAcoes.className = "acoes";

        const botaoEditar = document.createElement("button");
        botaoEditar.type = "button";
        botaoEditar.className = "botao-editar";
        botaoEditar.textContent = "Editar";
        botaoEditar.addEventListener("click", () => editarMunicipio(nome, dados));

        const botaoExcluir = document.createElement("button");
        botaoExcluir.type = "button";
        botaoExcluir.className = "botao-excluir";
        botaoExcluir.textContent = "Excluir";
        botaoExcluir.addEventListener("click", () => excluirMunicipio(nome));

        divAcoes.appendChild(botaoEditar);
        divAcoes.appendChild(botaoExcluir);
        celulaAcoes.appendChild(divAcoes);

        linha.appendChild(celulaNome);
        linha.appendChild(celulaUF);
        linha.appendChild(celulaCapital);
        linha.appendChild(celulaPopulacao);
        linha.appendChild(celulaIbge);
        linha.appendChild(celulaAcoes);

        corpoTabela.appendChild(linha);
    });
}


// ==========================================
// CADASTRAR OU EDITAR MUNICÍPIO
// ==========================================

formMunicipio.addEventListener("submit", async function(event) {
    event.preventDefault();

    const dados = {
        nome: campoNome.value.trim(),
        id_ibge: Number(campoIbge.value),
        estado: campoEstado.value.trim(),
        sigla_uf: campoUF.value,
        capital: campoCapital.value === "true",
        populacao_estimada: Number(campoPopulacao.value)
    };

    // Verifica se os números são válidos.
    if (
        !dados.nome ||
        !dados.estado ||
        !dados.sigla_uf ||
        !Number.isInteger(dados.id_ibge) ||
        dados.id_ibge <= 0 ||
        !Number.isInteger(dados.populacao_estimada) ||
        dados.populacao_estimada < 0
    ) {
        mostrarMensagem("Confira os dados preenchidos.", "erro");
        return;
    }

    try {
        let resposta;

        if (municipioEmEdicao) {
            // PATCH: altera os dados de um município existente.
            const dadosAtualizacao = {
                id_ibge: dados.id_ibge,
                estado: dados.estado,
                sigla_uf: dados.sigla_uf,
                capital: dados.capital,
                populacao_estimada: dados.populacao_estimada
            };

            resposta = await fetch(
                `/municipios/${encodeURIComponent(municipioEmEdicao)}`,
                {
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(dadosAtualizacao)
                }
            );

        } else {
            // POST: cadastra um novo município.
            resposta = await fetch("/municipios", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(dados)
            });
        }

        const resultado = await resposta.json();

        if (!resposta.ok) {
            throw new Error(resultado.erro || resultado.mensagem || "Não foi possível salvar o município.");
        }

        const estavaEditando = Boolean(municipioEmEdicao);

        limparFormulario();
        await carregarMunicipios();

        mostrarMensagem(
            estavaEditando
                ? "Município atualizado com sucesso!"
                : "Município cadastrado com sucesso!",
            "sucesso"
        );

    } catch (erro) {
        mostrarMensagem(erro.message, "erro");
    }
});


// ==========================================
// PREPARAR EDIÇÃO
// ==========================================

function editarMunicipio(nome, dados) {
    municipioEmEdicao = nome;

    campoNome.value = nome;
    campoIbge.value = dados.id_ibge;
    campoEstado.value = dados.estado;
    campoUF.value = dados.sigla_uf;
    campoCapital.value = String(dados.capital);
    campoPopulacao.value = dados.populacao_estimada;

    // O nome é a chave do município no dicionário.
    // Por isso, não alteramos essa chave durante o PATCH.
    campoNome.readOnly = true;

    tituloFormulario.textContent = "Editar município";
    btnSalvar.textContent = "Salvar alterações";
    btnCancelar.hidden = false;

    mostrarMensagem("Editando: " + nome, "sucesso");

    formMunicipio.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


// ==========================================
// CANCELAR EDIÇÃO / LIMPAR FORMULÁRIO
// ==========================================

function limparFormulario() {
    formMunicipio.reset();

    municipioEmEdicao = null;
    campoNome.readOnly = false;

    tituloFormulario.textContent = "Cadastrar município";
    btnSalvar.textContent = "Cadastrar município";
    btnCancelar.hidden = true;
}

btnCancelar.addEventListener("click", function() {
    limparFormulario();
    mostrarMensagem("Edição cancelada.", "sucesso");
});


// ==========================================
// EXCLUIR MUNICÍPIO
// ==========================================

async function excluirMunicipio(nome) {
    const confirmou = confirm(
        `Tem certeza de que deseja excluir o município ${nome}?`
    );

    if (!confirmou) {
        return;
    }

    try {
        const resposta = await fetch(
            `/municipios/${encodeURIComponent(nome)}`,
            {
                method: "DELETE"
            }
        );

        const resultado = await resposta.json();

        if (!resposta.ok) {
            throw new Error(resultado.erro || resultado.mensagem || "Não foi possível excluir o município.");
        }

        if (municipioEmEdicao === nome) {
            limparFormulario();
        }

        await carregarMunicipios();
        mostrarMensagem("Município excluído com sucesso!", "sucesso");

    } catch (erro) {
        mostrarMensagem(erro.message, "erro");
    }
}


// ==========================================
// PESQUISA E FILTRO
// ==========================================

buscaNome.addEventListener("input", carregarMunicipios);
filtroUF.addEventListener("change", carregarMunicipios);


// ==========================================
// INICIALIZAÇÃO
// ==========================================

document.addEventListener("DOMContentLoaded", carregarMunicipios);