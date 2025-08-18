# Conversas do Projeto

## Especificações do Projeto

3.3 Escola (Turmas e Matrículas)

**Identidade visual**
- Primária: #2563EB (azul)
- Secundária: #10B981 (verde)
- Acento: #F97316 (laranja)
- Fundo: #F1F5F9 (cinza claro)
- Texto: #0B1220
- Fonte sugerida: “Roboto” ou “Inter” (sans-serif)

**Layout**
- Header com “Gestão Escolar” + busca por aluno.
- Duas colunas: à esquerda filtro/estatísticas rápidas; à direita listagem principal.
- Modais para Novo Aluno e Nova Matrícula.

**Páginas/Seções**
1. Alunos: listagem com filtros (turma, status).
2. Turmas: listagem de turmas com capacidade e ocupação.
3. Relatórios (front): exportar CSV/JSON de alunos ou matrículas.

**Formulário de Aluno (front)**
- Campos: nome* (3–80), data_nascimento* (date), email (pattern), status* (ativo/inativo), turma_id (select opcional).
- Validações front: required, data válida ≥ 5 anos atrás, email regex, status.

**Interações JS**
- CRUD via fetch.
- Filtro combinado (turma + status + texto).
- Ordenação por nome/idade.
- Indicadores: total de alunos, ativos, por turma.
- Acessibilidade: foco visível, legenda em tabelas, aria-live para feedback de operações.

**Regra de negócio (front + back)**
- Ao matricular, não exceder capacidade da turma.
- Alterar status do aluno para “ativo” ao ser matriculado.

---

## Conversa com GitHub Copilot

**Usuário:**
ola, estou fazendo um projeto de ti envolvendo html, css e js, o meu tema é escola e essas sao algumas especificaçoes ... vc poderia fazer um projeto inicial envolvendo todos esses conceitos

**GitHub Copilot:**
Sure, here's a proposed directory structure for a school management system project using HTML, CSS, and JavaScript: ...

**Usuário:**
vc tem as minahs instruçoes vc poderia criar primeiro um html?

**GitHub Copilot:**
I apologize for the confusion in my previous response. I can help you create the initial HTML for your school management project. Here is a basic structure that follows your specifications: ...

**Usuário:**
agora faça um css

**GitHub Copilot:**
O arquivo style.css foi criado e estiliza todo o layout, identidade visual, responsividade, modais, tabelas e acessibilidade conforme suas especificações.

**Usuário:**
agora faça um js compativel com todo o html e css

**GitHub Copilot:**
O arquivo script.js foi criado e implementa toda a lógica de interatividade: CRUD de alunos, matrícula, filtros, estatísticas, modais, validações e renderização dinâmica, compatível com seu HTML e CSS.

**Usuário:**
agora poderia adicionar nossas conversas no md?

**GitHub Copilot:**
As conversas foram adicionadas neste arquivo para registro e acompanhamento do projeto.
