import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

alunos = []
turmas = []
aluno_id_seq = 1
turma_id_seq = 1

# Funções auxiliares

def atualizar_ocupacao():
    for turma in turmas:
        turma["ocupacao"] = len([a for a in alunos if a["turma_id"] == turma["id"]])

def validar_aluno(nome, data_nascimento, email, status):
    if len(nome) < 3 or len(nome) > 80:
        return "Nome deve ter entre 3 e 80 caracteres."
    try:
        data_min = datetime.now() - timedelta(days=5*365)
        if not data_nascimento or datetime.strptime(data_nascimento, "%Y-%m-%d") > data_min:
            return "Data de nascimento inválida."
    except:
        return "Data de nascimento inválida."
    if email and "@" not in email:
        return "Email inválido."
    if status not in ["ativo", "inativo"]:
        return "Status inválido."
    return None

def adicionar_aluno():
    global aluno_id_seq
    nome = entry_nome.get().strip()
    data_nascimento = entry_data.get().strip()
    email = entry_email.get().strip()
    status = combo_status.get()
    turma_nome = combo_turma.get()
    turma_id = next((t["id"] for t in turmas if t["nome"] == turma_nome), None) if turma_nome else None
    erro = validar_aluno(nome, data_nascimento, email, status)
    if erro:
        messagebox.showerror("Erro", erro)
        return
    alunos.append({
        "id": aluno_id_seq,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "email": email,
        "status": status,
        "turma_id": turma_id
    })
    aluno_id_seq += 1
    atualizar_ocupacao()
    atualizar_listagem()
    limpar_formulario()
    atualizar_combo_matricula()

def limpar_formulario():
    entry_nome.delete(0, tk.END)
    entry_data.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    combo_status.set("")
    combo_turma.set("")

def atualizar_listagem():
    for i in tree_alunos.get_children():
        tree_alunos.delete(i)
    for aluno in alunos:
        turma_nome = next((t["nome"] for t in turmas if t["id"] == aluno["turma_id"]), "-")
        tree_alunos.insert("", tk.END, values=(aluno["nome"], aluno["data_nascimento"], aluno["email"], aluno["status"], turma_nome))
    # Estatísticas
    total = len(alunos)
    ativos = len([a for a in alunos if a["status"] == "ativo"])
    estatisticas.set(f"Total: {total} | Ativos: {ativos} | " + ", ".join([f'{t["nome"]}: {t["ocupacao"]}/{t["capacidade"]}' for t in turmas]))

def matricular_aluno():
    aluno_nome = combo_matricula_aluno.get()
    turma_nome = combo_matricula_turma.get()
    aluno = next((a for a in alunos if a["nome"] == aluno_nome), None)
    turma = next((t for t in turmas if t["nome"] == turma_nome), None)
    if not aluno or not turma:
        messagebox.showerror("Erro", "Selecione aluno e turma.")
        return
    if turma["ocupacao"] >= turma["capacidade"]:
        messagebox.showerror("Erro", "Turma lotada!")
        return
    aluno["turma_id"] = turma["id"]
    aluno["status"] = "ativo"
    atualizar_ocupacao()
    atualizar_listagem()
    atualizar_combo_matricula()

def atualizar_combo_matricula():
    combo_matricula_aluno['values'] = [a["nome"] for a in alunos]
    combo_matricula_turma['values'] = [t["nome"] for t in turmas]
    combo_turma['values'] = [t["nome"] for t in turmas]

def adicionar_turma():
    global turma_id_seq
    nome = entry_turma_nome.get().strip()
    capacidade = entry_turma_capacidade.get().strip()
    if not nome:
        messagebox.showerror("Erro", "Nome da turma obrigatório.")
        return
    try:
        capacidade = int(capacidade)
        if capacidade <= 0:
            raise ValueError
    except:
        messagebox.showerror("Erro", "Capacidade deve ser um número positivo.")
        return
    turmas.append({"id": turma_id_seq, "nome": nome, "capacidade": capacidade, "ocupacao": 0})
    turma_id_seq += 1
    atualizar_combo_matricula()
    entry_turma_nome.delete(0, tk.END)
    entry_turma_capacidade.delete(0, tk.END)
    atualizar_listagem()

# Interface Tkinter
root = tk.Tk()
root.title("Gestão Escolar - Desktop")
root.geometry("900x700")
root.configure(bg="#F1F5F9")

# Cadastro de Turma
frame_turma = tk.LabelFrame(root, text="Nova Turma", padx=10, pady=10, bg="#F1F5F9")
frame_turma.pack(fill="x", padx=20, pady=10)

entry_turma_nome = tk.Entry(frame_turma)
entry_turma_nome.grid(row=0, column=1, padx=5, pady=5)
tk.Label(frame_turma, text="Nome da Turma*:", bg="#F1F5F9").grid(row=0, column=0)

entry_turma_capacidade = tk.Entry(frame_turma)
entry_turma_capacidade.grid(row=1, column=1, padx=5, pady=5)
tk.Label(frame_turma, text="Capacidade*:", bg="#F1F5F9").grid(row=1, column=0)

btn_turma = tk.Button(frame_turma, text="Salvar Turma", command=adicionar_turma, bg="#2563EB", fg="white")
btn_turma.grid(row=2, column=0, columnspan=2, pady=10)

# Cadastro de Aluno
frame_cadastro = tk.LabelFrame(root, text="Novo Aluno", padx=10, pady=10, bg="#F1F5F9")
frame_cadastro.pack(fill="x", padx=20, pady=10)

entry_nome = tk.Entry(frame_cadastro)
entry_nome.grid(row=0, column=1, padx=5, pady=5)
tk.Label(frame_cadastro, text="Nome*:", bg="#F1F5F9").grid(row=0, column=0)

entry_data = tk.Entry(frame_cadastro)
entry_data.grid(row=1, column=1, padx=5, pady=5)
tk.Label(frame_cadastro, text="Data Nascimento* (YYYY-MM-DD):", bg="#F1F5F9").grid(row=1, column=0)

entry_email = tk.Entry(frame_cadastro)
entry_email.grid(row=2, column=1, padx=5, pady=5)
tk.Label(frame_cadastro, text="Email:", bg="#F1F5F9").grid(row=2, column=0)

combo_status = ttk.Combobox(frame_cadastro, values=["ativo", "inativo"])
combo_status.grid(row=3, column=1, padx=5, pady=5)
tk.Label(frame_cadastro, text="Status*:", bg="#F1F5F9").grid(row=3, column=0)

combo_turma = ttk.Combobox(frame_cadastro)
combo_turma.grid(row=4, column=1, padx=5, pady=5)
tk.Label(frame_cadastro, text="Turma:", bg="#F1F5F9").grid(row=4, column=0)

btn_salvar = tk.Button(frame_cadastro, text="Salvar Aluno", command=adicionar_aluno, bg="#10B981", fg="white")
btn_salvar.grid(row=5, column=0, columnspan=2, pady=10)

# Matrícula
frame_matricula = tk.LabelFrame(root, text="Nova Matrícula", padx=10, pady=10, bg="#F1F5F9")
frame_matricula.pack(fill="x", padx=20, pady=10)

combo_matricula_aluno = ttk.Combobox(frame_matricula)
combo_matricula_aluno.grid(row=0, column=1, padx=5, pady=5)
tk.Label(frame_matricula, text="Aluno*:", bg="#F1F5F9").grid(row=0, column=0)

combo_matricula_turma = ttk.Combobox(frame_matricula)
combo_matricula_turma.grid(row=1, column=1, padx=5, pady=5)
tk.Label(frame_matricula, text="Turma*:", bg="#F1F5F9").grid(row=1, column=0)

btn_matricular = tk.Button(frame_matricula, text="Matricular", command=matricular_aluno, bg="#2563EB", fg="white")
btn_matricular.grid(row=2, column=0, columnspan=2, pady=10)

# Estatísticas
estatisticas = tk.StringVar()
tk.Label(root, textvariable=estatisticas, bg="#F1F5F9", font=("Arial", 12, "bold")).pack(pady=5)

# Listagem de Alunos
frame_listagem = tk.LabelFrame(root, text="Alunos", padx=10, pady=10, bg="#F1F5F9")
frame_listagem.pack(fill="both", expand=True, padx=20, pady=10)

cols = ("Nome", "Data Nasc.", "Email", "Status", "Turma")
tree_alunos = ttk.Treeview(frame_listagem, columns=cols, show="headings")
for col in cols:
    tree_alunos.heading(col, text=col)
    tree_alunos.column(col, width=120)
tree_alunos.pack(fill="both", expand=True)

atualizar_listagem()
atualizar_combo_matricula()

root.mainloop()
