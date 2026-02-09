import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

# Lista de produtos em memória
produtos = []

# Categorias pré-definidas
categorias = ["Alimentos", "Bebidas", "Higiene", "Eletrónica", "Roupas"]

# Gerar ID automático por categoria
def gerar_id(categoria):
    total = sum(1 for p in produtos if p["categoria"] == categoria) + 1
    return f"{categoria[:2].upper()}-{total:03d}"

# Atualizar ecrã
def carregar():
    lista.delete("1.0", "end")
    total_qtde = 0
    total_valor = 0.0

    for p in produtos:
        if filtro_nome.get().lower() not in p["nome"].lower():
            continue
        if filtro_id.get() and filtro_id.get() != p["id"]:
            continue

        aviso = " ⚠️ STOCK BAIXO" if p["quantidade"] <= p["limite"] else ""

        lista.insert(
            "end",
            f'{p["id"]} | {p["nome"]} | {p["categoria"]} | '
            f'Preço: {p["preco"]:.2f} Kz | Qtde: {p["quantidade"]}{aviso}\n'
        )

        total_qtde += p["quantidade"]
        total_valor += p["quantidade"] * p["preco"]

    totais.configure(
        text=f"Quantidade Total: {total_qtde} | Valor Total: {total_valor:.2f} Kz"
    )

# Adicionar produto
def adicionar():
    try:
        categoria = categoria_combo.get()
        if not categoria or categoria == "Selecione Categoria":
            messagebox.showwarning("Aviso", "Selecione uma categoria!")
            return

        produto = {
            "id": gerar_id(categoria),
            "nome": nome_entry.get(),
            "categoria": categoria,
            "preco": float(preco_entry.get()),
            "quantidade": int(qtde_entry.get()),
            "limite": int(limite_entry.get())
        }

        produtos.append(produto)
        carregar()
        limpar_campos()
        messagebox.showinfo("Sucesso", f'Produto {produto["id"]} adicionado!')

        # Alerta automático se stock baixo
        if produto["quantidade"] <= produto["limite"]:
            messagebox.showwarning(
                "Atenção",
                f'O produto {produto["nome"]} atingiu o limite mínimo de stock!'
            )

    except:
        messagebox.showerror("Erro", "Dados inválidos!")

# Atualizar produto
def atualizar():
    pid = filtro_id.get().strip()
    if not pid:
        messagebox.showwarning("Aviso", "Informe o ID para atualizar!")
        return

    for p in produtos:
        if p["id"] == pid:
            p["nome"] = nome_entry.get()
            p["categoria"] = categoria_combo.get()
            p["preco"] = float(preco_entry.get())
            p["quantidade"] = int(qtde_entry.get())
            p["limite"] = int(limite_entry.get())
            carregar()
            limpar_campos()
            messagebox.showinfo("Sucesso", "Produto atualizado!")

            # Alerta automático se stock baixo
            if p["quantidade"] <= p["limite"]:
                messagebox.showwarning(
                    "Atenção",
                    f'O produto {p["nome"]} atingiu o limite mínimo de stock!'
                )
            return

    messagebox.showerror("Erro", "Produto não encontrado!")

# Remover produto
def remover():
    pid = filtro_id.get().strip()
    if not pid:
        messagebox.showwarning("Aviso", "Informe o ID para remover!")
        return

    for i, p in enumerate(produtos):
        if p["id"] == pid:
            confirm = messagebox.askyesno("Confirmar", f"Remover produto {pid}?")
            if confirm:
                produtos.pop(i)
                carregar()
                limpar_campos()
            return

    messagebox.showerror("Erro", "Produto não encontrado!")

# Selecionar produto da lista
def selecionar():
    try:
        linha = lista.get("sel.first", "sel.last").strip()
        if not linha:
            messagebox.showwarning("Aviso", "Selecione uma linha da lista!")
            return
        pid = linha.split(" | ")[0]
        filtro_id.set(pid)

        for p in produtos:
            if p["id"] == pid:
                nome_entry.set(p["nome"])
                categoria_combo.set(p["categoria"])
                preco_entry.set(str(p["preco"]))
                qtde_entry.set(str(p["quantidade"]))
                limite_entry.set(str(p["limite"]))
                return
    except:
        messagebox.showwarning("Aviso", "Selecione corretamente um produto!")

# Limpar campos
def limpar_campos():
    nome_entry.set("")
    categoria_combo.set("Selecione Categoria")
    preco_entry.set("")
    qtde_entry.set("")
    limite_entry.set("")
    filtro_id.set("")

# ===============================
# JANELA PRINCIPAL
# ===============================

app = ctk.CTk()
app.title("Gestão de Produtos")
app.geometry("940x650")
app.resizable(False, False)

titulo = ctk.CTkLabel(app, text="Gestão de Produtos", font=("Arial", 26, "bold"))
titulo.place(x=320, y=10)

# Filtros
filtro_nome = ctk.CTkEntry(app, width=200, placeholder_text="Filtrar por nome")
filtro_nome.place(x=20, y=70)

filtro_id = ctk.CTkEntry(app, width=150, placeholder_text="Filtrar por ID")
filtro_id.place(x=240, y=70)

ctk.CTkButton(app, text="Filtrar", width=120, command=carregar).place(x=410, y=70)

# Listagem
lista = ctk.CTkTextbox(app, width=900, height=250)
lista.place(x=20, y=110)

# Campos de entrada
nome_entry = ctk.CTkEntry(app, width=200, placeholder_text="Nome do produto")
nome_entry.place(x=20, y=380)

categoria_combo = ctk.CTkComboBox(app, values=categorias, width=150)
categoria_combo.set("Selecione Categoria")
categoria_combo.place(x=240, y=380)

preco_entry = ctk.CTkEntry(app, width=100, placeholder_text="Preço")
preco_entry.place(x=410, y=380)

qtde_entry = ctk.CTkEntry(app, width=100, placeholder_text="Quantidade")
qtde_entry.place(x=530, y=380)

limite_entry = ctk.CTkEntry(app, width=120, placeholder_text="Limite mínimo")
limite_entry.place(x=650, y=380)

# Botões
ctk.CTkButton(app, text="Adicionar Produto", width=160, command=adicionar).place(x=20, y=440)
ctk.CTkButton(app, text="Atualizar Produto", width=160, command=atualizar).place(x=200, y=440)
ctk.CTkButton(app, text="Remover Produto", width=160, command=remover).place(x=380, y=440)
ctk.CTkButton(app, text="Editar Selecionado", width=160, command=selecionar).place(x=560, y=440)
ctk.CTkButton(app, text="Limpar Campos", width=140, command=limpar_campos).place(x=740, y=440)

# Totais
totais = ctk.CTkLabel(app, text="", font=("Arial", 14, "bold"))
totais.place(x=20, y=520)

# Rodapé com os nomes dos desenvolvedores
rodape = ctk.CTkLabel(
    app,
    text="Desenvolvedores: António Bravo, Felícia Campos, Jorge Cabaça, Santo Moreira",
    font=("Arial", 12),
    text_color="gray"
)
rodape.place(x=20, y=600)

carregar()
app.mainloop()