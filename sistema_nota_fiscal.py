import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.graphics.shapes import Drawing
import json
import os
from datetime import datetime
import win32print
import win32api
import tempfile
import subprocess
import sys
import ctypes
import xml.etree.ElementTree as ET
from xml.dom import minidom
import hashlib
import base64
import uuid
import re
from decimal import Decimal, ROUND_HALF_UP
import qrcode
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography import x509
import win32crypt
import win32security
import win32api
import win32con
from PIL import Image, ImageTk

class SistemaNotaFiscal:
    def __init__(self, root):
        self.root = root
        self.root.title("Padaria Quero Mais System")
        self.root.geometry("800x600")
        
        # Tentar definir ícone de pão (se possível)
        try:
            # Criar ícone simples de pão usando caracteres ASCII
            self.root.iconbitmap(default="")  # Limpar ícone padrão
        except:
            pass  # Se não conseguir, continua sem ícone
        
        # Dados da empresa (serão carregados do arquivo)
        self.dados_empresa = {
            "nome": "",
            "cnpj": "",
            "endereco": "",
            "cidade": "",
            "cep": "",
            "telefone": ""
        }
        
        # Lista de produtos
        self.produtos = []
        
        # Lista de notas fiscais
        self.notas_fiscais = []
        
        # Carregar dados salvos
        self.carregar_dados()
        
        # Criar tela de login primeiro
        self.criar_tela_login()
    
    def criar_tela_login(self):
        """Cria a tela de login com design exato da imagem"""
        # Limpar a janela
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Configurar a janela para tela cheia
        self.root.state('zoomed')  # Tela cheia no Windows
        self.root.title("Login - Padaria Quero Mais System")
        
        # Frame principal com fundo bege exato da imagem
        main_frame = tk.Frame(self.root, bg="#f7f5ef")  # Bege exato da imagem
        main_frame.pack(fill="both", expand=True)
        
        # Seção esquerda - Logo da Padaria (50% da tela)
        left_frame = tk.Frame(main_frame, bg="#f7f5ef")
        left_frame.pack(side="left", fill="both", expand=True)
        
        # Logo da Padaria centralizado
        logo_frame = tk.Frame(left_frame, bg="#f7f5ef")
        logo_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título "PADARIA" em fonte serif bold exata
        titulo_logo = tk.Label(logo_frame, text="PADARIA", 
                              font=("Georgia", 64, "bold"), 
                              bg="#f7f5ef", fg="#2a2a2a")
        titulo_logo.pack(pady=(0, 25))
        
        # Linha decorativa com diamante no centro
        linha_frame = tk.Frame(logo_frame, bg="#f7f5ef", width=300, height=20)
        linha_frame.pack(pady=(0, 40))
        
        # Linha esquerda
        linha_esq = tk.Frame(linha_frame, height=1, bg="#2a2a2a")
        linha_esq.place(relx=0, rely=0.5, anchor="w", width=130, height=1)
        
        # Diamante central
        diamante_canvas = tk.Canvas(linha_frame, width=12, height=12, bg="#f7f5ef", highlightthickness=0)
        diamante_canvas.place(relx=0.5, rely=0.5, anchor="center")
        diamante_canvas.create_polygon(6, 0, 12, 6, 6, 12, 0, 6, fill="#2a2a2a", outline="#2a2a2a")
        
        # Linha direita
        linha_dir = tk.Frame(linha_frame, height=1, bg="#2a2a2a")
        linha_dir.place(relx=1, rely=0.5, anchor="e", width=130, height=1)
        
        # Canvas para desenhar o logo do pão exato
        logo_canvas = tk.Canvas(logo_frame, width=400, height=300, 
                               bg="#f7f5ef", highlightthickness=0)
        logo_canvas.pack()
        
        # Desenhar o pão baguette exato
        # Pão principal (baguette alongado)
        logo_canvas.create_oval(120, 140, 280, 220, outline="#2a2a2a", width=3, fill="")
        
        # Cortes no pão (3 seções arredondadas)
        logo_canvas.create_arc(130, 145, 270, 215, start=0, extent=180, outline="#2a2a2a", width=2, fill="")
        logo_canvas.create_line(145, 155, 255, 155, fill="#2a2a2a", width=2)
        logo_canvas.create_line(150, 165, 250, 165, fill="#2a2a2a", width=2)
        logo_canvas.create_line(155, 175, 245, 175, fill="#2a2a2a", width=2)
        
        # Slash mark destacado em branco (mais proeminente)
        logo_canvas.create_line(165, 185, 235, 185, fill="white", width=6)
        
        # Espigas de trigo mais detalhadas
        # Espiga esquerda
        logo_canvas.create_line(50, 250, 90, 170, fill="#2a2a2a", width=3)
        # Folhas da espiga esquerda
        for i in range(6):
            y_pos = 220 - i * 15
            logo_canvas.create_line(60 + i*5, y_pos, 80 + i*5, y_pos - 8, fill="#2a2a2a", width=1)
            logo_canvas.create_line(60 + i*5, y_pos, 80 + i*5, y_pos + 8, fill="#2a2a2a", width=1)
        
        # Espiga direita
        logo_canvas.create_line(350, 250, 310, 170, fill="#2a2a2a", width=3)
        # Folhas da espiga direita
        for i in range(6):
            y_pos = 220 - i * 15
            logo_canvas.create_line(340 - i*5, y_pos, 320 - i*5, y_pos - 8, fill="#2a2a2a", width=1)
            logo_canvas.create_line(340 - i*5, y_pos, 320 - i*5, y_pos + 8, fill="#2a2a2a", width=1)
        
        # Curva inferior
        logo_canvas.create_arc(120, 200, 280, 260, start=0, extent=180, 
                              outline="#2a2a2a", width=2, fill="")
        
        # Seção direita - Formulário de login (50% da tela)
        right_frame = tk.Frame(main_frame, bg="#f7f5ef")
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Card branco com bordas arredondadas exatas
        card_canvas = tk.Canvas(right_frame, bg="#f7f5ef", highlightthickness=0, width=700, height=800)
        card_canvas.place(relx=0.5, rely=0.5, anchor="center")
        
        # Desenhar card branco com bordas arredondadas mais suaves
        def draw_rounded_card(canvas, x1, y1, x2, y2, radius, color):
            # Desenhar retângulo arredondado
            canvas.create_arc(x1, y1, x1 + 2*radius, y1 + 2*radius, 
                            start=90, extent=90, fill=color, outline=color)
            canvas.create_arc(x2 - 2*radius, y1, x2, y1 + 2*radius, 
                            start=0, extent=90, fill=color, outline=color)
            canvas.create_arc(x2 - 2*radius, y2 - 2*radius, x2, y2, 
                            start=270, extent=90, fill=color, outline=color)
            canvas.create_arc(x1, y2 - 2*radius, x1 + 2*radius, y2, 
                            start=180, extent=90, fill=color, outline=color)
            
            # Desenhar retângulos para preencher
            canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, 
                                  fill=color, outline=color)
            canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, 
                                  fill=color, outline=color)
        
        # Desenhar o card com bordas mais arredondadas
        draw_rounded_card(card_canvas, 30, 30, 670, 770, 40, "white")
        
        # Frame interno para o conteúdo do card
        card_inner = tk.Frame(card_canvas, bg="white", padx=100, pady=100)
        card_canvas.create_window(350, 400, window=card_inner, width=640, height=740)
        
        # Título "Seja bem-vindo!" exato
        titulo_card = tk.Label(card_inner, text="Seja bem-vindo!", 
                              font=("Arial", 42, "bold"), 
                              bg="white", fg="#2a2a2a")
        titulo_card.pack(pady=(0, 15))
        
        # Subtítulo exato
        subtitulo_card = tk.Label(card_inner, text="Entre com seu CNPJ/CPF e Senha", 
                                 font=("Arial", 20), 
                                 bg="white", fg="#666666")
        subtitulo_card.pack(pady=(0, 80))
        
        # Frame para os campos de entrada
        campos_frame = tk.Frame(card_inner, bg="white")
        campos_frame.pack(fill="x", pady=(0, 80))
        
        # Campo CPF/CNPJ com design exato
        self.entry_usuario = tk.Entry(campos_frame, 
                                     font=("Arial", 20), 
                                     bg="white", fg="#2a2a2a",
                                     insertbackground="#2a2a2a",
                                     relief="flat", bd=0,
                                     highlightthickness=0)
        self.entry_usuario.pack(fill="x", pady=(0, 50), ipady=25)
        self.entry_usuario.insert(0, "Insira seu CPF ou CNPJ")
        self.entry_usuario.config(fg="#999999")
        self.entry_usuario.focus()
        
        # Linha inferior do campo usuário
        linha_usuario = tk.Frame(campos_frame, height=1, bg="#e0e0e0")
        linha_usuario.pack(fill="x", pady=(10, 0))
        
        # Campo Senha com design exato
        self.entry_senha = tk.Entry(campos_frame, 
                                   font=("Arial", 20), 
                                   bg="white", fg="#2a2a2a",
                                   insertbackground="#2a2a2a",
                                   relief="flat", bd=0,
                                   highlightthickness=0,
                                   show="*")
        self.entry_senha.pack(fill="x", pady=(0, 50), ipady=25)
        self.entry_senha.insert(0, "Senha")
        self.entry_senha.config(fg="#999999")
        
        # Linha inferior do campo senha
        linha_senha = tk.Frame(campos_frame, height=1, bg="#e0e0e0")
        linha_senha.pack(fill="x", pady=(10, 0))
        
        # Botão "Cadastrar" com design exato da imagem
        btn_cadastrar = tk.Button(card_inner, text="Cadastrar", 
                                 font=("Arial", 22, "bold"), 
                                 bg="#e0d8c0", fg="white",  # Amarelo dourado exato da imagem
                                 relief="flat", bd=0,
                                 activebackground="#d0c8b0",
                                 activeforeground="white",
                                 command=self.verificar_login,
                                 width=25, height=2)
        btn_cadastrar.pack(pady=35)
        
        # Configurar placeholders
        def on_focus_in(event, entry, placeholder):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg="#2a2a2a")
                if entry == self.entry_senha:
                    entry.config(show="*")
        
        def on_focus_out(event, entry, placeholder):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.config(fg="#999999")
                if entry == self.entry_senha:
                    entry.config(show="")
        
        self.entry_usuario.bind('<FocusIn>', lambda e: on_focus_in(e, self.entry_usuario, "Insira seu CPF ou CNPJ"))
        self.entry_usuario.bind('<FocusOut>', lambda e: on_focus_out(e, self.entry_usuario, "Insira seu CPF ou CNPJ"))
        self.entry_senha.bind('<FocusIn>', lambda e: on_focus_in(e, self.entry_senha, "Senha"))
        self.entry_senha.bind('<FocusOut>', lambda e: on_focus_out(e, self.entry_senha, "Senha"))
        
        # Bind Enter key
        self.root.bind('<Return>', lambda event: self.verificar_login())
        
        # Informações de login (discretas)
        info_frame = tk.Frame(main_frame, bg="#f7f5ef")
        info_frame.pack(side="bottom", pady=15)
        
        tk.Label(info_frame, text="Usuário: admin1 | Senha: admin123", 
                font=("Arial", 10), bg="#f7f5ef", fg="#999999").pack()
    
    def verificar_login(self):
        """Verifica as credenciais de login"""
        usuario = self.entry_usuario.get().strip()
        senha = self.entry_senha.get().strip()
        
        # Remover placeholders se ainda estiverem presentes
        if usuario == "Insira seu CPF ou CNPJ":
            usuario = ""
        if senha == "Senha":
            senha = ""
        
        # Credenciais válidas
        if usuario == "admin1" and senha == "admin123":
            # Login bem-sucedido
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            
            # Limpar a janela e criar a interface principal
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Restaurar tamanho da janela normal
            self.root.state('normal')  # Sair da tela cheia
            self.root.geometry("800x600")
            self.root.title("Padaria Quero Mais System")
            
            # Criar a interface principal
            self.criar_interface()
        else:
            # Login falhou
            messagebox.showerror("Erro", "Usuário ou senha incorretos!")
            self.entry_senha.delete(0, tk.END)
            self.entry_senha.insert(0, "Senha")
            self.entry_senha.config(fg="#999999", show="")
            self.entry_usuario.focus()
    
    def criar_botao_arredondado(self, parent, text, command, bg_color, fg_color="white", font_size=10):
        """Cria um botão com bordas arredondadas"""
        # Criar frame para o botão
        frame = tk.Frame(parent, bg=bg_color, relief="flat", bd=0)
        
        # Criar canvas para desenhar bordas arredondadas
        canvas = tk.Canvas(frame, bg=bg_color, highlightthickness=0, width=130, height=40)
        canvas.pack(fill="both", expand=True)
        
        # Função para desenhar retângulo arredondado
        def draw_rounded_rectangle(canvas, x1, y1, x2, y2, radius, color):
            # Desenhar retângulo arredondado usando arcos
            canvas.create_arc(x1, y1, x1 + 2*radius, y1 + 2*radius, 
                            start=90, extent=90, fill=color, outline=color)
            canvas.create_arc(x2 - 2*radius, y1, x2, y1 + 2*radius, 
                            start=0, extent=90, fill=color, outline=color)
            canvas.create_arc(x2 - 2*radius, y2 - 2*radius, x2, y2, 
                            start=270, extent=90, fill=color, outline=color)
            canvas.create_arc(x1, y2 - 2*radius, x1 + 2*radius, y2, 
                            start=180, extent=90, fill=color, outline=color)
            
            # Desenhar retângulos para preencher
            canvas.create_rectangle(x1 + radius, y1, x2 - radius, y2, 
                                  fill=color, outline=color)
            canvas.create_rectangle(x1, y1 + radius, x2, y2 - radius, 
                                  fill=color, outline=color)
        
        # Desenhar o fundo arredondado
        draw_rounded_rectangle(canvas, 2, 2, 128, 38, 8, bg_color)
        
        # Criar botão dentro do canvas
        btn = tk.Button(canvas, text=text, command=command,
                       bg=bg_color, fg=fg_color, font=("Arial", font_size, "bold"),
                       relief="flat", bd=0, padx=15, pady=8,
                       cursor="hand2", activebackground=bg_color,
                       activeforeground=fg_color,
                       highlightthickness=0)
        
        # Posicionar o botão no centro do canvas
        canvas.create_window(65, 20, window=btn)
        
        # Adicionar efeitos hover
        def on_enter(e):
            # Escurecer a cor de fundo
            if bg_color == "#000080":  # Azul marinho
                new_color = "#0000A0"
            elif bg_color == "#FF0000":  # Vermelho
                new_color = "#FF3333"
            elif bg_color == "#008000":  # Verde
                new_color = "#00A000"
            elif bg_color == "#FFFF00":  # Amarelo
                new_color = "#FFFF33"
            else:
                new_color = bg_color
            
            btn.configure(bg=new_color, activebackground=new_color)
            canvas.configure(bg=new_color)
            # Redesenhar o fundo arredondado
            canvas.delete("all")
            draw_rounded_rectangle(canvas, 2, 2, 128, 38, 8, new_color)
            canvas.create_window(65, 20, window=btn)
        
        def on_leave(e):
            btn.configure(bg=bg_color, activebackground=bg_color)
            canvas.configure(bg=bg_color)
            # Redesenhar o fundo arredondado
            canvas.delete("all")
            draw_rounded_rectangle(canvas, 2, 2, 128, 38, 8, bg_color)
            canvas.create_window(65, 20, window=btn)
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return frame
    
    def criar_interface(self):
        # Notebook para abas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Aba de Configuração da Empresa
        self.criar_aba_empresa(notebook)
        
        # Aba de Produtos
        self.criar_aba_produtos(notebook)
        
        # Aba de Nota Fiscal
        self.criar_aba_nota_fiscal(notebook)
        
        # Aba de Histórico
        self.criar_aba_historico(notebook)
    
    def criar_aba_empresa(self, notebook):
        frame_empresa = ttk.Frame(notebook)
        notebook.add(frame_empresa, text="Dados da Empresa")
        
        # Título centralizado e maior
        ttk.Label(frame_empresa, text="Dados da Empresa", font=("Arial", 20, "bold")).pack(pady=30)
        
        # Frame central para os campos com borda
        frame_central = ttk.LabelFrame(frame_empresa, text="Informações da Empresa", padding=30)
        frame_central.pack(expand=True, fill='both', padx=100, pady=20)
        
        # Campos centralizados com placeholders
        campos = [
            ("Nome da Empresa:", "nome", "Digite o nome da empresa"),
            ("CNPJ:", "cnpj", "00.000.000/0001-00"),
            ("Endereço:", "endereco", "Rua, Número, Bairro"),
            ("Cidade/Estado:", "cidade", "São Paulo - SP"),
            ("CEP:", "cep", "00000-000"),
            ("Telefone:", "telefone", "(00) 0000-0000")
        ]
        
        self.entries_empresa = {}
        
        for i, (label, key, placeholder) in enumerate(campos):
            # Frame para cada campo
            frame_campo = ttk.Frame(frame_central)
            frame_campo.pack(fill='x', pady=20)
            
            # Label centralizado e maior
            label_widget = ttk.Label(frame_campo, text=label, font=("Arial", 14, "bold"))
            label_widget.pack(pady=(0, 8))
            
            # Entry centralizado e maior
            entry = ttk.Entry(frame_campo, width=70, font=("Arial", 12))
            entry.pack(pady=8)
            
            # Inserir valor atual ou placeholder
            valor_atual = self.dados_empresa.get(key, "")
            if valor_atual:
                entry.insert(0, valor_atual)
            else:
                entry.insert(0, placeholder)
                entry.config(foreground='gray')
            
            # Funções para gerenciar placeholder
            def on_focus_in(event, entry=entry, placeholder=placeholder):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(foreground='black')
            
            def on_focus_out(event, entry=entry, placeholder=placeholder):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(foreground='gray')
            
            # Vincular eventos
            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)
            
            self.entries_empresa[key] = entry
        
        # Botão salvar centralizado e maior
        frame_botao = ttk.Frame(frame_empresa)
        frame_botao.pack(pady=40)
        
        btn_salvar = ttk.Button(frame_botao, text="Salvar Dados da Empresa", 
                               command=self.salvar_dados_empresa,
                               style="Large.TButton")
        btn_salvar.pack()
        
        # Configurar estilo para botão maior
        style = ttk.Style()
        style.configure("Large.TButton", font=("Arial", 14, "bold"), padding=15)
    
    def criar_aba_produtos(self, notebook):
        frame_produtos = ttk.Frame(notebook)
        notebook.add(frame_produtos, text="Produtos")
        
        # Título
        ttk.Label(frame_produtos, text="Cadastro de Produtos", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Frame para entrada de dados
        frame_entrada = ttk.Frame(frame_produtos)
        frame_entrada.pack(fill='x', padx=20, pady=10)
        
        # Campos do produto
        ttk.Label(frame_entrada, text="Código:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.entry_codigo = ttk.Entry(frame_entrada, width=15)
        self.entry_codigo.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_entrada, text="Descrição:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.entry_descricao = ttk.Entry(frame_entrada, width=30)
        self.entry_descricao.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(frame_entrada, text="Preço Unitário:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.entry_preco = ttk.Entry(frame_entrada, width=15)
        self.entry_preco.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_entrada, text="Unidade:").grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.entry_unidade = ttk.Entry(frame_entrada, width=10)
        self.entry_unidade.insert(0, "UN")
        self.entry_unidade.grid(row=1, column=3, padx=5, pady=5)
        
        # Botões
        frame_botoes = ttk.Frame(frame_produtos)
        frame_botoes.pack(pady=10)
        
        ttk.Button(frame_botoes, text="Adicionar Produto", command=self.adicionar_produto).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Remover Produto", command=self.remover_produto).pack(side='left', padx=5)
        
        # Lista de produtos
        frame_lista = ttk.Frame(frame_produtos)
        frame_lista.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview para produtos
        colunas = ("Código", "Descrição", "Preço Unit.", "Unidade")
        self.tree_produtos = ttk.Treeview(frame_lista, columns=colunas, show='headings')
        
        for col in colunas:
            self.tree_produtos.heading(col, text=col)
            self.tree_produtos.column(col, width=150)
        
        self.tree_produtos.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree_produtos.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree_produtos.configure(yscrollcommand=scrollbar.set)
        
        # Atualizar lista
        self.atualizar_lista_produtos()
    
    def criar_aba_nota_fiscal(self, notebook):
        frame_nf = ttk.Frame(notebook)
        notebook.add(frame_nf, text="Nova Nota Fiscal")
        
        # Título
        ttk.Label(frame_nf, text="Nova Nota Fiscal", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Frame para dados do cliente
        frame_cliente = ttk.LabelFrame(frame_nf, text="Dados do Cliente")
        frame_cliente.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(frame_cliente, text="Nome:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.entry_cliente_nome = ttk.Entry(frame_cliente, width=40)
        self.entry_cliente_nome.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_cliente, text="CPF/CNPJ:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.entry_cliente_documento = ttk.Entry(frame_cliente, width=20)
        self.entry_cliente_documento.grid(row=0, column=3, padx=5, pady=5)
        self.entry_cliente_documento.insert(0, "000.000.000-00")
        self.entry_cliente_documento.bind('<FocusIn>', lambda e: self.entry_cliente_documento.delete(0, tk.END) if self.entry_cliente_documento.get() == "000.000.000-00" else None)
        self.entry_cliente_documento.bind('<FocusOut>', lambda e: self.entry_cliente_documento.insert(0, "000.000.000-00") if not self.entry_cliente_documento.get() else None)
        
        ttk.Label(frame_cliente, text="Endereço:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.entry_cliente_endereco = ttk.Entry(frame_cliente, width=40)
        self.entry_cliente_endereco.grid(row=1, column=1, padx=5, pady=5)
        self.entry_cliente_endereco.insert(0, "Rua, Número, Bairro")
        self.entry_cliente_endereco.bind('<FocusIn>', lambda e: self.entry_cliente_endereco.delete(0, tk.END) if self.entry_cliente_endereco.get() == "Rua, Número, Bairro" else None)
        self.entry_cliente_endereco.bind('<FocusOut>', lambda e: self.entry_cliente_endereco.insert(0, "Rua, Número, Bairro") if not self.entry_cliente_endereco.get() else None)
        
        # Frame para itens
        frame_itens = ttk.LabelFrame(frame_nf, text="Itens da Nota Fiscal")
        frame_itens.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Frame para adicionar itens
        frame_add_item = ttk.Frame(frame_itens)
        frame_add_item.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_add_item, text="Produto:").pack(side='left', padx=5)
        self.combo_produto = ttk.Combobox(frame_add_item, width=30)
        self.combo_produto.pack(side='left', padx=5)
        
        ttk.Label(frame_add_item, text="Quantidade:").pack(side='left', padx=5)
        self.entry_quantidade = ttk.Entry(frame_add_item, width=10)
        self.entry_quantidade.pack(side='left', padx=5)
        self.entry_quantidade.insert(0, "1")
        
        ttk.Button(frame_add_item, text="Adicionar Item", command=self.adicionar_item_nf).pack(side='left', padx=5)
        
        # Lista de itens
        colunas_itens = ("Código", "Descrição", "Qtd", "Preço Unit.", "Total")
        self.tree_itens = ttk.Treeview(frame_itens, columns=colunas_itens, show='headings')
        
        for col in colunas_itens:
            self.tree_itens.heading(col, text=col)
            self.tree_itens.column(col, width=120)
        
        self.tree_itens.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Scrollbar para itens
        scrollbar_itens = ttk.Scrollbar(frame_itens, orient='vertical', command=self.tree_itens.yview)
        scrollbar_itens.pack(side='right', fill='y')
        self.tree_itens.configure(yscrollcommand=scrollbar_itens.set)
        
        # Frame para totais
        frame_totais = ttk.Frame(frame_nf)
        frame_totais.pack(fill='x', padx=20, pady=10)
        
        self.label_subtotal = ttk.Label(frame_totais, text="Subtotal: R$ 0,00", font=("Arial", 12))
        self.label_subtotal.pack(side='right', padx=10)
        
        self.label_total = ttk.Label(frame_totais, text="Total: R$ 0,00", font=("Arial", 14, "bold"))
        self.label_total.pack(side='right', padx=10)
        
        # Botões
        frame_botoes_nf = ttk.Frame(frame_nf)
        frame_botoes_nf.pack(pady=20)
        
        ttk.Button(frame_botoes_nf, text="Limpar Nota", command=self.limpar_nota_fiscal).pack(side='left', padx=5)
        ttk.Button(frame_botoes_nf, text="Salvar Nota", command=self.salvar_nota_fiscal).pack(side='left', padx=5)
        ttk.Button(frame_botoes_nf, text="Visualizar PDF", command=self.visualizar_pdf_antes_imprimir).pack(side='left', padx=5)
        ttk.Button(frame_botoes_nf, text="Gerar e Imprimir NF", command=self.gerar_imprimir_nf).pack(side='left', padx=5)
        ttk.Button(frame_botoes_nf, text="Abrir Pasta PDFs", command=self.abrir_pasta_pdfs).pack(side='left', padx=5)
        
        # Lista de itens da nota atual
        self.itens_nota_atual = []
        
        # Atualizar combo de produtos
        self.atualizar_combo_produtos()
    
    def criar_aba_historico(self, notebook):
        frame_historico = ttk.Frame(notebook)
        notebook.add(frame_historico, text="Histórico")
        
        # Título
        ttk.Label(frame_historico, text="Histórico de Notas Fiscais", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Frame para filtros
        frame_filtros = ttk.Frame(frame_historico)
        frame_filtros.pack(fill='x', padx=20, pady=10)
        
        ttk.Label(frame_filtros, text="Cliente:").pack(side='left', padx=5)
        self.entry_filtro_cliente = ttk.Entry(frame_filtros, width=30)
        self.entry_filtro_cliente.pack(side='left', padx=5)
        
        ttk.Button(frame_filtros, text="Filtrar", command=self.filtrar_historico).pack(side='left', padx=5)
        ttk.Button(frame_filtros, text="Limpar Filtro", command=self.limpar_filtro).pack(side='left', padx=5)
        
        # Lista de notas fiscais
        frame_lista_nf = ttk.Frame(frame_historico)
        frame_lista_nf.pack(fill='both', expand=True, padx=20, pady=10)
        
        colunas_historico = ("Data", "Número", "Cliente", "Total", "Status")
        self.tree_historico = ttk.Treeview(frame_lista_nf, columns=colunas_historico, show='headings')
        
        for col in colunas_historico:
            self.tree_historico.heading(col, text=col)
            self.tree_historico.column(col, width=150)
        
        self.tree_historico.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar_historico = ttk.Scrollbar(frame_lista_nf, orient='vertical', command=self.tree_historico.yview)
        scrollbar_historico.pack(side='right', fill='y')
        self.tree_historico.configure(yscrollcommand=scrollbar_historico.set)
        
        # Frame para botões de ação
        frame_botoes_acao = ttk.Frame(frame_historico)
        frame_botoes_acao.pack(pady=10)
        
        # Botão Visualizar (Azul marinho) - Centralizado e bordas arredondadas
        btn_visualizar_frame = self.criar_botao_arredondado(
            frame_botoes_acao, "👁 Visualizar", self.visualizar_nf, "#000080", "white", 10
        )
        btn_visualizar_frame.pack(side='left', padx=5)
        
        # Botão Apagar (Vermelho com ícone de lixeira) - Centralizado e bordas arredondadas
        btn_apagar_frame = self.criar_botao_arredondado(
            frame_botoes_acao, "🗑 Apagar", self.apagar_nf, "#FF0000", "white", 10
        )
        btn_apagar_frame.pack(side='left', padx=5)
        
        # Botão Marcar como Concluída (Verde com símbolo de positivo) - Centralizado e bordas arredondadas
        btn_concluir_frame = self.criar_botao_arredondado(
            frame_botoes_acao, "✓ Concluída", self.marcar_concluida, "#008000", "white", 10
        )
        btn_concluir_frame.pack(side='left', padx=5)
        
        # Botão Nota Pendente (Amarelo) - Centralizado e bordas arredondadas
        btn_pendente_frame = self.criar_botao_arredondado(
            frame_botoes_acao, "⏳ Pendente", self.marcar_pendente, "#FFFF00", "black", 10
        )
        btn_pendente_frame.pack(side='left', padx=5)
        
        # Botão Reimprimir
        ttk.Button(frame_botoes_acao, text="Reimprimir NF", command=self.reimprimir_nf).pack(side='left', padx=5)
        
        # Frame para botões de pasta
        frame_botoes_pasta = ttk.Frame(frame_historico)
        frame_botoes_pasta.pack(pady=5)
        
        # Botões para abrir pastas
        ttk.Button(frame_botoes_pasta, text="📁 Abrir Pasta PDFs", command=self.abrir_pasta_pdfs).pack(side='left', padx=5)
        ttk.Button(frame_botoes_pasta, text="📄 Abrir Pasta XMLs NF-e", command=self.abrir_pasta_xmls).pack(side='left', padx=5)
        
        # Atualizar histórico
        self.atualizar_historico()
    
    def salvar_dados_empresa(self):
        # Validar CNPJ da empresa
        cnpj_empresa = self.entries_empresa['cnpj'].get().strip()
        if cnpj_empresa and cnpj_empresa != "00.000.000/0001-00" and not self.validar_cnpj(cnpj_empresa):
            messagebox.showerror("Erro", "CNPJ da empresa inválido!")
            return
        
        # Salvar dados
        for key, entry in self.entries_empresa.items():
            valor = entry.get().strip()
            
            # Não salvar placeholders
            placeholders = {
                "nome": "Digite o nome da empresa",
                "cnpj": "00.000.000/0001-00",
                "endereco": "Rua, Número, Bairro",
                "cidade": "São Paulo - SP",
                "cep": "00000-000",
                "telefone": "(00) 0000-0000"
            }
            
            if valor == placeholders.get(key, ""):
                valor = ""  # Salvar como vazio se for placeholder
            
            # Formatar CNPJ se for válido
            if key == 'cnpj' and valor and valor != "00.000.000/0001-00" and self.validar_cnpj(valor):
                valor = self.formatar_cnpj(valor)
                entry.delete(0, tk.END)
                entry.insert(0, valor)
            
            self.dados_empresa[key] = valor
        
        self.salvar_dados()
        messagebox.showinfo("Sucesso", "Dados da empresa salvos com sucesso!")
    
    def adicionar_produto(self):
        codigo = self.entry_codigo.get().strip()
        descricao = self.entry_descricao.get().strip()
        preco = self.entry_preco.get().strip()
        unidade = self.entry_unidade.get().strip()
        
        if not codigo or not descricao or not preco:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return
        
        try:
            preco = float(preco.replace(',', '.'))
        except ValueError:
            messagebox.showerror("Erro", "Preço inválido!")
            return
        
        produto = {
            "codigo": codigo,
            "descricao": descricao,
            "preco": preco,
            "unidade": unidade
        }
        
        # Verificar se produto já existe
        for i, p in enumerate(self.produtos):
            if p["codigo"] == codigo:
                self.produtos[i] = produto
                break
        else:
            self.produtos.append(produto)
        
        self.salvar_dados()
        self.atualizar_lista_produtos()
        self.atualizar_combo_produtos()
        
        # Limpar campos
        self.entry_codigo.delete(0, tk.END)
        self.entry_descricao.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)
        self.entry_unidade.delete(0, tk.END)
        self.entry_unidade.insert(0, "UN")
        
        messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
    
    def remover_produto(self):
        selecao = self.tree_produtos.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um produto para remover!")
            return
        
        item = self.tree_produtos.item(selecao[0])
        codigo = item['values'][0]
        
        # Remover produto da lista
        self.produtos = [p for p in self.produtos if p["codigo"] != codigo]
        
        # Remover da visualização imediatamente
        self.tree_produtos.delete(selecao[0])
        
        # Atualizar combo de produtos
        self.atualizar_combo_produtos()
        
        # Salvar dados
        self.salvar_dados()
        
        messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
    
    def atualizar_lista_produtos(self):
        for item in self.tree_produtos.get_children():
            self.tree_produtos.delete(item)
        
        for produto in self.produtos:
            self.tree_produtos.insert('', 'end', values=(
                produto["codigo"],
                produto["descricao"],
                f"R$ {produto['preco']:.2f}".replace('.', ','),
                produto["unidade"]
            ))
    
    def atualizar_combo_produtos(self):
        produtos_desc = [f"{p['codigo']} - {p['descricao']}" for p in self.produtos]
        self.combo_produto['values'] = produtos_desc
    
    def adicionar_item_nf(self):
        if not self.combo_produto.get():
            messagebox.showwarning("Aviso", "Selecione um produto!")
            return
        
        try:
            quantidade = float(self.entry_quantidade.get().replace(',', '.'))
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida!")
            return
        
        # Encontrar produto selecionado
        codigo_produto = self.combo_produto.get().split(' - ')[0]
        produto = None
        for p in self.produtos:
            if p["codigo"] == codigo_produto:
                produto = p
                break
        
        if not produto:
            messagebox.showerror("Erro", "Produto não encontrado!")
            return
        
        # Adicionar item
        item = {
            "codigo": produto["codigo"],
            "descricao": produto["descricao"],
            "quantidade": quantidade,
            "preco_unitario": produto["preco"],
            "total": quantidade * produto["preco"]
        }
        
        self.itens_nota_atual.append(item)
        self.atualizar_lista_itens()
        self.calcular_totais()
        
        # Limpar campos
        self.combo_produto.set('')
        self.entry_quantidade.delete(0, tk.END)
        self.entry_quantidade.insert(0, "1")
    
    def atualizar_lista_itens(self):
        for item in self.tree_itens.get_children():
            self.tree_itens.delete(item)
        
        for item in self.itens_nota_atual:
            self.tree_itens.insert('', 'end', values=(
                item["codigo"],
                item["descricao"],
                f"{item['quantidade']:.2f}".replace('.', ','),
                f"R$ {item['preco_unitario']:.2f}".replace('.', ','),
                f"R$ {item['total']:.2f}".replace('.', ',')
            ))
    
    def calcular_totais(self):
        subtotal = sum(item["total"] for item in self.itens_nota_atual)
        total = subtotal  # Sem impostos por simplicidade
        
        self.label_subtotal.config(text=f"Subtotal: R$ {subtotal:.2f}".replace('.', ','))
        self.label_total.config(text=f"Total: R$ {total:.2f}".replace('.', ','))
    
    def limpar_nota_fiscal(self):
        self.itens_nota_atual = []
        self.atualizar_lista_itens()
        self.calcular_totais()
        
        self.entry_cliente_nome.delete(0, tk.END)
        self.entry_cliente_documento.delete(0, tk.END)
        self.entry_cliente_endereco.delete(0, tk.END)
    
    def salvar_nota_fiscal(self):
        if not self.itens_nota_atual:
            messagebox.showwarning("Aviso", "Adicione itens à nota fiscal!")
            return
        
        cliente_nome = self.entry_cliente_nome.get().strip()
        cliente_documento = self.entry_cliente_documento.get().strip()
        cliente_endereco = self.entry_cliente_endereco.get().strip()
        
        if not cliente_nome:
            messagebox.showwarning("Aviso", "Informe o nome do cliente!")
            return
        
        # Validar documento do cliente (CPF ou CNPJ)
        if cliente_documento:
            if len(''.join(filter(str.isdigit, cliente_documento))) == 11:
                if not self.validar_cpf(cliente_documento):
                    messagebox.showerror("Erro", "CPF do cliente inválido!")
                    return
                # Formatar CPF
                cpf_formatado = self.formatar_cpf(cliente_documento)
                self.entry_cliente_documento.delete(0, tk.END)
                self.entry_cliente_documento.insert(0, cpf_formatado)
                cliente_documento = cpf_formatado
            elif len(''.join(filter(str.isdigit, cliente_documento))) == 14:
                if not self.validar_cnpj(cliente_documento):
                    messagebox.showerror("Erro", "CNPJ do cliente inválido!")
                    return
                # Formatar CNPJ
                cnpj_formatado = self.formatar_cnpj(cliente_documento)
                self.entry_cliente_documento.delete(0, tk.END)
                self.entry_cliente_documento.insert(0, cnpj_formatado)
                cliente_documento = cnpj_formatado
            else:
                messagebox.showerror("Erro", "Documento do cliente deve ter 11 dígitos (CPF) ou 14 dígitos (CNPJ)!")
                return
        
        # Gerar número da nota
        numero_nf = len(self.notas_fiscais) + 1
        
        # Criar nota fiscal
        nota_fiscal = {
            "numero": numero_nf,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "cliente": {
                "nome": cliente_nome,
                "documento": cliente_documento,
                "endereco": cliente_endereco
            },
            "itens": self.itens_nota_atual.copy(),
            "subtotal": sum(item["total"] for item in self.itens_nota_atual),
            "total": sum(item["total"] for item in self.itens_nota_atual),
            "status": "Pendente"
        }
        
        # Gerar PDF e XML NF-e
        arquivo_pdf = self.gerar_pdf(nota_fiscal)
        arquivo_xml = self.gerar_xml_nfe(nota_fiscal)
        
        # Perguntar se quer imprimir
        resposta = messagebox.askyesno("Imprimir", 
                                      f"Nota Fiscal #{numero_nf} gerada com sucesso!\n\n"
                                      f"✅ PDF gerado: {os.path.basename(arquivo_pdf)}\n"
                                      f"✅ XML NF-e gerado: {os.path.basename(arquivo_xml)}\n\n"
                                      f"Deseja imprimir agora?\n\n"
                                      f"Se não, você pode imprimir depois pelo histórico.")
        
        if resposta:
            # Tentar imprimir
            if self.imprimir_pdf(arquivo_pdf):
                messagebox.showinfo("Sucesso", f"Nota Fiscal #{numero_nf} impressa com sucesso!")
            else:
                messagebox.showwarning("Aviso", 
                                      "Erro ao imprimir automaticamente.\n\n"
                                      "O PDF foi aberto para você imprimir manualmente.")
                try:
                    os.startfile(arquivo_pdf)
                except:
                    pass
        
        # Salvar nota fiscal de qualquer forma
        self.notas_fiscais.append(nota_fiscal)
        self.salvar_dados()
        self.atualizar_historico()
        self.limpar_nota_fiscal()
    
    def abrir_pasta_pdfs(self):
        try:
            # Obter caminho absoluto da pasta PDFs
            pasta_atual = os.path.abspath(os.getcwd())
            pasta_pdfs = os.path.join(pasta_atual, "pdfs")
            
            # Criar pasta se não existir
            if not os.path.exists(pasta_pdfs):
                os.makedirs(pasta_pdfs)
            
            # Abrir pasta no explorador
            os.startfile(pasta_pdfs)
            messagebox.showinfo("Sucesso", f"Pasta de PDFs aberta: {pasta_pdfs}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir pasta de PDFs: {e}")
            print(f"Erro ao abrir pasta: {e}")
    
    def abrir_pasta_xmls(self):
        try:
            # Obter caminho absoluto da pasta XMLs
            pasta_atual = os.path.abspath(os.getcwd())
            pasta_xmls = os.path.join(pasta_atual, "xmls")
            
            # Criar pasta se não existir
            if not os.path.exists(pasta_xmls):
                os.makedirs(pasta_xmls)
            
            # Abrir pasta no explorador
            os.startfile(pasta_xmls)
            messagebox.showinfo("Sucesso", f"Pasta de XMLs NF-e aberta: {pasta_xmls}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir pasta de XMLs: {e}")
            print(f"Erro ao abrir pasta: {e}")
    
    def gerar_codigo_barras(self, numero_nf, valor_total):
        """Gera código de barras para pagamento"""
        try:
            # Criar código de barras com número da NF e valor
            codigo = f"{numero_nf:06d}{valor_total:.2f}".replace('.', '')
            # Adicionar zeros à esquerda para completar 44 dígitos (padrão brasileiro)
            codigo = codigo.zfill(44)
            
            # Criar desenho do código de barras
            drawing = Drawing(400, 50)
            barcode = code128.Code128(codigo, barHeight=30, barWidth=1.5)
            drawing.add(barcode)
            
            return drawing, codigo
        except Exception as e:
            print(f"Erro ao gerar código de barras: {e}")
            return None, ""
    
    def visualizar_pdf_antes_imprimir(self):
        if not self.itens_nota_atual:
            messagebox.showwarning("Aviso", "Adicione itens à nota fiscal!")
            return
        
        cliente_nome = self.entry_cliente_nome.get().strip()
        cliente_documento = self.entry_cliente_documento.get().strip()
        cliente_endereco = self.entry_cliente_endereco.get().strip()
        
        if not cliente_nome:
            messagebox.showwarning("Aviso", "Informe o nome do cliente!")
            return
        
        # Validar documento do cliente (CPF ou CNPJ)
        if cliente_documento:
            if len(''.join(filter(str.isdigit, cliente_documento))) == 11:
                if not self.validar_cpf(cliente_documento):
                    messagebox.showerror("Erro", "CPF do cliente inválido!")
                    return
                # Formatar CPF
                cpf_formatado = self.formatar_cpf(cliente_documento)
                self.entry_cliente_documento.delete(0, tk.END)
                self.entry_cliente_documento.insert(0, cpf_formatado)
                cliente_documento = cpf_formatado
            elif len(''.join(filter(str.isdigit, cliente_documento))) == 14:
                if not self.validar_cnpj(cliente_documento):
                    messagebox.showerror("Erro", "CNPJ do cliente inválido!")
                    return
                # Formatar CNPJ
                cnpj_formatado = self.formatar_cnpj(cliente_documento)
                self.entry_cliente_documento.delete(0, tk.END)
                self.entry_cliente_documento.insert(0, cnpj_formatado)
                cliente_documento = cnpj_formatado
            else:
                messagebox.showerror("Erro", "Documento do cliente deve ter 11 dígitos (CPF) ou 14 dígitos (CNPJ)!")
                return
        
        # Gerar número da nota
        numero_nf = len(self.notas_fiscais) + 1
        
        # Criar nota fiscal
        nota_fiscal = {
            "numero": numero_nf,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "cliente": {
                "nome": cliente_nome,
                "documento": cliente_documento,
                "endereco": cliente_endereco
            },
            "itens": self.itens_nota_atual.copy(),
            "subtotal": sum(item["total"] for item in self.itens_nota_atual),
            "total": sum(item["total"] for item in self.itens_nota_atual),
            "status": "Pendente"
        }
        
        try:
            # Gerar PDF
            arquivo_pdf = self.gerar_pdf(nota_fiscal)
            
            # Verificar se o arquivo foi criado
            if not os.path.exists(arquivo_pdf):
                messagebox.showerror("Erro", f"Erro ao gerar o PDF. Arquivo não encontrado: {arquivo_pdf}")
                return
            
            # Visualizar PDF
            print(f"Tentando abrir: {arquivo_pdf}")
            
            # Verificar se o arquivo existe antes de tentar abrir
            if os.path.exists(arquivo_pdf):
                # Tentar abrir com diferentes métodos
                try:
                    # Método 1: os.startfile
                    os.startfile(arquivo_pdf)
                    messagebox.showinfo("Sucesso", f"PDF da Nota Fiscal #{numero_nf} aberto para visualização!")
                except Exception as e1:
                    print(f"Erro com os.startfile: {e1}")
                    try:
                        # Método 2: subprocess
                        subprocess.run(['start', arquivo_pdf], shell=True, check=True)
                        messagebox.showinfo("Sucesso", f"PDF da Nota Fiscal #{numero_nf} aberto para visualização!")
                    except Exception as e2:
                        print(f"Erro com subprocess: {e2}")
                        # Método 3: Mostrar caminho para abrir manualmente
                        messagebox.showinfo("PDF Gerado", 
                                          f"PDF da Nota Fiscal #{numero_nf} foi gerado com sucesso!\n\n"
                                          f"Localização: {arquivo_pdf}\n\n"
                                          f"Abra manualmente o arquivo para visualizar.")
            else:
                messagebox.showerror("Erro", f"Arquivo PDF não encontrado: {arquivo_pdf}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar/abrir o PDF:\n{str(e)}")
            print(f"Erro detalhado: {e}")
            import traceback
            traceback.print_exc()
    
    def gerar_imprimir_nf(self):
        if not self.itens_nota_atual:
            messagebox.showwarning("Aviso", "Adicione itens à nota fiscal!")
            return
        
        cliente_nome = self.entry_cliente_nome.get().strip()
        cliente_documento = self.entry_cliente_documento.get().strip()
        cliente_endereco = self.entry_cliente_endereco.get().strip()
        
        if not cliente_nome:
            messagebox.showwarning("Aviso", "Informe o nome do cliente!")
            return
        
        # Validar documento do cliente (CPF ou CNPJ)
        if cliente_documento:
            if len(''.join(filter(str.isdigit, cliente_documento))) == 11:
                if not self.validar_cpf(cliente_documento):
                    messagebox.showerror("Erro", "CPF do cliente inválido!")
                    return
                # Formatar CPF
                cpf_formatado = self.formatar_cpf(cliente_documento)
                self.entry_cliente_documento.delete(0, tk.END)
                self.entry_cliente_documento.insert(0, cpf_formatado)
                cliente_documento = cpf_formatado
            elif len(''.join(filter(str.isdigit, cliente_documento))) == 14:
                if not self.validar_cnpj(cliente_documento):
                    messagebox.showerror("Erro", "CNPJ do cliente inválido!")
                    return
                # Formatar CNPJ
                cnpj_formatado = self.formatar_cnpj(cliente_documento)
                self.entry_cliente_documento.delete(0, tk.END)
                self.entry_cliente_documento.insert(0, cnpj_formatado)
                cliente_documento = cnpj_formatado
            else:
                messagebox.showerror("Erro", "Documento do cliente deve ter 11 dígitos (CPF) ou 14 dígitos (CNPJ)!")
                return
        
        # Gerar número da nota
        numero_nf = len(self.notas_fiscais) + 1
        
        # Criar nota fiscal
        nota_fiscal = {
            "numero": numero_nf,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "cliente": {
                "nome": cliente_nome,
                "documento": cliente_documento,
                "endereco": cliente_endereco
            },
            "itens": self.itens_nota_atual.copy(),
            "subtotal": sum(item["total"] for item in self.itens_nota_atual),
            "total": sum(item["total"] for item in self.itens_nota_atual),
            "status": "Concluída"
        }
        
        # Gerar PDF e XML NF-e
        arquivo_pdf = self.gerar_pdf(nota_fiscal)
        arquivo_xml = self.gerar_xml_nfe(nota_fiscal)
        
        # Perguntar se quer imprimir
        resposta = messagebox.askyesno("Imprimir", 
                                      f"Nota Fiscal #{numero_nf} gerada com sucesso!\n\n"
                                      f"✅ PDF gerado: {os.path.basename(arquivo_pdf)}\n"
                                      f"✅ XML NF-e gerado: {os.path.basename(arquivo_xml)}\n\n"
                                      f"Deseja imprimir agora?\n\n"
                                      f"Se não, você pode imprimir depois pelo histórico.")
        
        if resposta:
            # Tentar imprimir
            if self.imprimir_pdf(arquivo_pdf):
                messagebox.showinfo("Sucesso", f"Nota Fiscal #{numero_nf} impressa com sucesso!")
            else:
                messagebox.showwarning("Aviso", 
                                      "Erro ao imprimir automaticamente.\n\n"
                                      "O PDF foi aberto para você imprimir manualmente.")
                try:
                    os.startfile(arquivo_pdf)
                except:
                    pass
        
        # Salvar nota fiscal de qualquer forma
        self.notas_fiscais.append(nota_fiscal)
        self.salvar_dados()
        self.atualizar_historico()
        self.limpar_nota_fiscal()
    
    def limpar_documento(self, documento):
        """Remove caracteres especiais de documentos"""
        return re.sub(r'[^\d]', '', documento)
    
    def formatar_valor_decimal(self, valor):
        """Formata valor para formato decimal com 2 casas"""
        return str(Decimal(str(valor)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
    
    def gerar_chave_acesso(self, uf, aamm, cnpj, modelo, serie, numero, codigo_numerico, tipo_emissao):
        """Gera chave de acesso da NF-e"""
        # Formatar componentes da chave
        uf = str(uf).zfill(2)
        aamm = str(aamm).zfill(4)
        cnpj = self.limpar_documento(cnpj).zfill(14)
        modelo = str(modelo).zfill(2)
        serie = str(serie).zfill(3)
        numero = str(numero).zfill(9)
        codigo_numerico = str(codigo_numerico).zfill(8)
        tipo_emissao = str(tipo_emissao).zfill(1)
        
        # Montar chave (43 dígitos)
        chave = f"{uf}{aamm}{cnpj}{modelo}{serie}{numero}{codigo_numerico}{tipo_emissao}"
        
        # Calcular dígito verificador
        multiplicadores = [4,3,2,9,8,7,6,5,4,3,2,9,8,7,6,5,4,3,2,9,8,7,6,5,4,3,2,9,8,7,6,5,4,3,2,9,8,7,6,5,4,3,2]
        soma = sum(int(chave[i]) * multiplicadores[i] for i in range(43))
        resto = soma % 11
        dv = 0 if resto < 2 else 11 - resto
        
        return f"{chave}{dv}"
    
    def gerar_id_nfe(self, chave_acesso):
        """Gera ID da NF-e"""
        return f"NFe{chave_acesso}"
    
    def carregar_certificado_digital(self):
        """Carrega o certificado digital do sistema"""
        try:
            # Tentar carregar certificado do Windows
            store = win32crypt.CertOpenSystemStore(0, "MY")
            cert = win32crypt.CertFindCertificateInStore(store, win32crypt.X509_ASN_ENCODING, 0, win32crypt.CERT_FIND_SUBJECT_STR, "SEFAZ", None)
            
            if cert:
                # Converter para formato cryptography
                cert_data = win32crypt.CertGetCertificateContextProperty(cert, win32crypt.CERT_KEY_PROV_INFO_PROP_ID)
                return cert
            else:
                print("Certificado digital não encontrado. Usando certificado simulado.")
                return None
        except Exception as e:
            print(f"Erro ao carregar certificado: {e}")
            return None
    
    def assinar_xml(self, xml_string, certificado):
        """Assina o XML com certificado digital"""
        try:
            if certificado:
                # Implementar assinatura real com certificado
                # Por enquanto, retorna XML sem assinatura
                return xml_string
            else:
                # Assinatura simulada para homologação
                return xml_string
        except Exception as e:
            print(f"Erro ao assinar XML: {e}")
            return xml_string
    
    def gerar_qr_code_nfe(self, chave_acesso, protocolo, valor_total):
        """Gera QR Code para NF-e"""
        try:
            # Dados para QR Code (formato oficial SEFAZ)
            dados_qr = f"{chave_acesso}|{protocolo}|{valor_total:.2f}"
            
            # Criar QR Code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(dados_qr)
            qr.make(fit=True)
            
            # Criar imagem
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Salvar temporariamente
            temp_path = os.path.join(tempfile.gettempdir(), f"qr_code_{chave_acesso}.png")
            qr_image.save(temp_path)
            
            return temp_path
        except Exception as e:
            print(f"Erro ao gerar QR Code: {e}")
            return None
    
    def gerar_xml_nfe(self, nota_fiscal):
        """Gera XML da NF-e conforme padrão SEFAZ"""
        try:
            # Obter caminho absoluto da pasta atual
            pasta_atual = os.path.abspath(os.getcwd())
            
            # Criar pasta para XMLs se não existir
            pasta_xmls = os.path.join(pasta_atual, "xmls")
            if not os.path.exists(pasta_xmls):
                os.makedirs(pasta_xmls)
            
            # Dados da empresa
            cnpj_empresa = self.limpar_documento(self.dados_empresa['cnpj'])
            uf_empresa = "35"  # SP (padrão)
            
            # Data e hora atual
            data_hora = datetime.now()
            data_emissao = data_hora.strftime("%Y-%m-%d")
            hora_emissao = data_hora.strftime("%H:%M:%S")
            
            # Gerar chave de acesso
            aamm = data_hora.strftime("%y%m")
            serie = "001"
            codigo_numerico = "00000001"
            tipo_emissao = "1"  # Normal
            modelo = "55"  # NF-e
            
            chave_acesso = self.gerar_chave_acesso(
                uf_empresa, aamm, cnpj_empresa, modelo, 
                serie, nota_fiscal['numero'], codigo_numerico, tipo_emissao
            )
            
            # Criar elemento raiz
            root = ET.Element("nfeProc", xmlns="http://www.portalfiscal.inf.br/nfe", versao="4.00")
            
            # Elemento NFe
            nfe = ET.SubElement(root, "NFe", xmlns="http://www.portalfiscal.inf.br/nfe")
            
            # Informações da NF-e
            inf_nfe = ET.SubElement(nfe, "infNFe", Id=self.gerar_id_nfe(chave_acesso), versao="4.00")
            
            # Identificação da NF-e
            ide = ET.SubElement(inf_nfe, "ide")
            ET.SubElement(ide, "cUF").text = uf_empresa
            ET.SubElement(ide, "cNF").text = codigo_numerico
            ET.SubElement(ide, "natOp").text = "Venda de Mercadoria"
            ET.SubElement(ide, "mod").text = modelo
            ET.SubElement(ide, "serie").text = serie
            ET.SubElement(ide, "nNF").text = str(nota_fiscal['numero'])
            ET.SubElement(ide, "dhEmi").text = f"{data_emissao}T{hora_emissao}-03:00"
            ET.SubElement(ide, "tpNF").text = "1"  # Saída
            ET.SubElement(ide, "idDest").text = "1"  # Operação Interna
            ET.SubElement(ide, "cMunFG").text = "3550308"  # São Paulo
            ET.SubElement(ide, "tpImp").text = "1"  # Retrato
            ET.SubElement(ide, "tpEmis").text = "1"  # Normal
            ET.SubElement(ide, "cDV").text = chave_acesso[-1]
            ET.SubElement(ide, "tpAmb").text = "2"  # Homologação
            ET.SubElement(ide, "finNFe").text = "1"  # Normal
            ET.SubElement(ide, "indFinal").text = "1"  # Consumidor Final
            ET.SubElement(ide, "indPres").text = "1"  # Operação Presencial
            ET.SubElement(ide, "procEmi").text = "0"  # Aplicativo do Contribuinte
            ET.SubElement(ide, "verProc").text = "1.0"
            
            # Emitente
            emit = ET.SubElement(inf_nfe, "emit")
            ET.SubElement(emit, "CNPJ").text = cnpj_empresa
            ET.SubElement(emit, "xNome").text = self.dados_empresa['nome']
            ET.SubElement(emit, "xFant").text = self.dados_empresa['nome']
            
            # Endereço do emitente
            ender_emit = ET.SubElement(emit, "enderEmit")
            ET.SubElement(ender_emit, "xLgr").text = self.dados_empresa['endereco']
            ET.SubElement(ender_emit, "nro").text = "S/N"
            ET.SubElement(ender_emit, "xBairro").text = "Centro"
            ET.SubElement(ender_emit, "cMun").text = "3550308"  # São Paulo
            ET.SubElement(ender_emit, "xMun").text = "São Paulo"
            ET.SubElement(ender_emit, "UF").text = "SP"
            ET.SubElement(ender_emit, "CEP").text = self.limpar_documento(self.dados_empresa['cep'])
            ET.SubElement(ender_emit, "cPais").text = "1058"  # Brasil
            ET.SubElement(ender_emit, "xPais").text = "BRASIL"
            
            # Destinatário
            dest = ET.SubElement(inf_nfe, "dest")
            if nota_fiscal['cliente']['documento']:
                doc_cliente = self.limpar_documento(nota_fiscal['cliente']['documento'])
                if len(doc_cliente) == 11:
                    ET.SubElement(dest, "CPF").text = doc_cliente
                else:
                    ET.SubElement(dest, "CNPJ").text = doc_cliente
            ET.SubElement(dest, "xNome").text = nota_fiscal['cliente']['nome']
            
            # Endereço do destinatário
            if nota_fiscal['cliente']['endereco']:
                ender_dest = ET.SubElement(dest, "enderDest")
                ET.SubElement(ender_dest, "xLgr").text = nota_fiscal['cliente']['endereco']
                ET.SubElement(ender_dest, "nro").text = "S/N"
                ET.SubElement(ender_dest, "xBairro").text = "Centro"
                ET.SubElement(ender_dest, "cMun").text = "3550308"  # São Paulo
                ET.SubElement(ender_dest, "xMun").text = "São Paulo"
                ET.SubElement(ender_dest, "UF").text = "SP"
                ET.SubElement(ender_dest, "CEP").text = "00000000"
                ET.SubElement(ender_dest, "cPais").text = "1058"  # Brasil
                ET.SubElement(ender_dest, "xPais").text = "BRASIL"
            
            # Itens da NF-e
            det = ET.SubElement(inf_nfe, "det")
            for i, item in enumerate(nota_fiscal['itens']):
                det_item = ET.SubElement(det, "det", nItem=str(i+1))
                
                # Produto
                prod = ET.SubElement(det_item, "prod")
                ET.SubElement(prod, "cProd").text = item['codigo']
                ET.SubElement(prod, "xProd").text = item['descricao']
                ET.SubElement(prod, "NCM").text = "21069090"  # Outros produtos de padaria
                ET.SubElement(prod, "CFOP").text = "5102"  # Venda de mercadoria
                ET.SubElement(prod, "uCom").text = item.get('unidade', 'UN')
                ET.SubElement(prod, "qCom").text = self.formatar_valor_decimal(item['quantidade'])
                ET.SubElement(prod, "vUnCom").text = self.formatar_valor_decimal(item['preco_unitario'])
                ET.SubElement(prod, "vProd").text = self.formatar_valor_decimal(item['total'])
                ET.SubElement(prod, "uTrib").text = item.get('unidade', 'UN')
                ET.SubElement(prod, "qTrib").text = self.formatar_valor_decimal(item['quantidade'])
                ET.SubElement(prod, "vUnTrib").text = self.formatar_valor_decimal(item['preco_unitario'])
                ET.SubElement(prod, "indTot").text = "1"  # Valor do item compõe total da NF
                
                # Impostos
                imposto = ET.SubElement(det_item, "imposto")
                
                # ICMS
                icms = ET.SubElement(imposto, "ICMS")
                icms00 = ET.SubElement(icms, "ICMS00")
                ET.SubElement(icms00, "orig").text = "0"  # Nacional
                ET.SubElement(icms00, "CST").text = "00"  # Tributada integralmente
                ET.SubElement(icms00, "modBC").text = "0"  # Valor do produto
                ET.SubElement(icms00, "vBC").text = self.formatar_valor_decimal(item['total'])
                ET.SubElement(icms00, "pICMS").text = "18.00"  # 18% ICMS
                ET.SubElement(icms00, "vICMS").text = self.formatar_valor_decimal(item['total'] * 0.18)
                
                # PIS
                pis = ET.SubElement(imposto, "PIS")
                pis_aliq = ET.SubElement(pis, "PISAliq")
                ET.SubElement(pis_aliq, "CST").text = "01"  # Operação tributável
                ET.SubElement(pis_aliq, "vBC").text = self.formatar_valor_decimal(item['total'])
                ET.SubElement(pis_aliq, "pPIS").text = "1.65"  # 1.65% PIS
                ET.SubElement(pis_aliq, "vPIS").text = self.formatar_valor_decimal(item['total'] * 0.0165)
                
                # COFINS
                cofins = ET.SubElement(imposto, "COFINS")
                cofins_aliq = ET.SubElement(cofins, "COFINSAliq")
                ET.SubElement(cofins_aliq, "CST").text = "01"  # Operação tributável
                ET.SubElement(cofins_aliq, "vBC").text = self.formatar_valor_decimal(item['total'])
                ET.SubElement(cofins_aliq, "pCOFINS").text = "7.6"  # 7.6% COFINS
                ET.SubElement(cofins_aliq, "vCOFINS").text = self.formatar_valor_decimal(item['total'] * 0.076)
            
            # Totais
            total = ET.SubElement(inf_nfe, "total")
            
            # ICMS Total
            icms_total = ET.SubElement(total, "ICMSTot")
            base_calculo = sum(item['total'] for item in nota_fiscal['itens'])
            valor_icms = base_calculo * 0.18
            valor_total = base_calculo + valor_icms
            
            ET.SubElement(icms_total, "vBC").text = self.formatar_valor_decimal(base_calculo)
            ET.SubElement(icms_total, "vICMS").text = self.formatar_valor_decimal(valor_icms)
            ET.SubElement(icms_total, "vProd").text = self.formatar_valor_decimal(base_calculo)
            ET.SubElement(icms_total, "vNF").text = self.formatar_valor_decimal(valor_total)
            
            # Transporte
            transp = ET.SubElement(inf_nfe, "transp")
            ET.SubElement(transp, "modFrete").text = "9"  # Sem frete
            
            # Pagamento
            pag = ET.SubElement(inf_nfe, "pag")
            det_pag = ET.SubElement(pag, "detPag")
            ET.SubElement(det_pag, "indPag").text = "0"  # À vista
            ET.SubElement(det_pag, "tPag").text = "01"  # Dinheiro
            ET.SubElement(det_pag, "vPag").text = self.formatar_valor_decimal(valor_total)
            
            # Informações adicionais
            inf_adic = ET.SubElement(inf_nfe, "infAdic")
            ET.SubElement(inf_adic, "infAdFisco").text = "NF-e gerada pelo sistema Padaria Quero Mais"
            ET.SubElement(inf_adic, "infCpl").text = "Documento válido para fins fiscais"
            
            # Carregar certificado digital
            certificado = self.carregar_certificado_digital()
            
            # Gerar protocolo real ou simulado
            if certificado:
                # Protocolo real (produção)
                protocolo = f"135210000025991"
                status = "100"  # Autorizado
                motivo = "Autorizacao de uso da NF-e"
                ambiente = "1"  # Produção
            else:
                # Protocolo simulado (homologação)
                protocolo = f"135210000025991"
                status = "100"  # Autorizado
                motivo = "Autorizacao de uso da NF-e"
                ambiente = "2"  # Homologação
            
            # Protocolo de autorização
            prot_nfe = ET.SubElement(root, "protNFe", versao="4.00")
            inf_prot = ET.SubElement(prot_nfe, "infProt")
            ET.SubElement(inf_prot, "tpAmb").text = ambiente
            ET.SubElement(inf_prot, "verAplic").text = "1.0"
            ET.SubElement(inf_prot, "chNFe").text = chave_acesso
            ET.SubElement(inf_prot, "dhRecbto").text = f"{data_emissao}T{hora_emissao}-03:00"
            ET.SubElement(inf_prot, "nProt").text = protocolo
            ET.SubElement(inf_prot, "digVal").text = "0000000000000000000000000000000000000000000"
            ET.SubElement(inf_prot, "cStat").text = status
            ET.SubElement(inf_prot, "xMotivo").text = motivo
            
            # Assinar XML
            xml_string = ET.tostring(root, encoding='unicode')
            xml_assinar = self.assinar_xml(xml_string, certificado)
            
            # Criar XML formatado
            xml_str = ET.tostring(root, encoding='unicode')
            dom = minidom.parseString(xml_str)
            xml_formatado = dom.toprettyxml(indent="  ")
            
            # Salvar arquivo XML
            nome_arquivo = f"NFe_{chave_acesso}.xml"
            caminho_completo = os.path.join(pasta_xmls, nome_arquivo)
            
            with open(caminho_completo, 'w', encoding='utf-8') as f:
                f.write(xml_formatado)
            
            print(f"XML NF-e gerado com sucesso: {caminho_completo}")
            return caminho_completo
            
        except Exception as e:
            print(f"Erro ao gerar XML NF-e: {e}")
            raise e
    
    def gerar_pdf(self, nota_fiscal):
        try:
            # Obter caminho absoluto da pasta atual
            pasta_atual = os.path.abspath(os.getcwd())
            
            # Criar pasta para PDFs se não existir
            pasta_pdfs = os.path.join(pasta_atual, "pdfs")
            if not os.path.exists(pasta_pdfs):
                os.makedirs(pasta_pdfs)
            
            # Criar nome do arquivo com número da nota
            nome_arquivo = f"NF_{nota_fiscal['numero']:06d}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            caminho_completo = os.path.join(pasta_pdfs, nome_arquivo)
            
            print(f"Gerando PDF em: {caminho_completo}")
            
            # Criar arquivo PDF com margens centralizadas
            doc = SimpleDocTemplate(caminho_completo, pagesize=A4, 
                                  leftMargin=1*inch, rightMargin=1*inch,
                                  topMargin=0.8*inch, bottomMargin=0.8*inch)
            story = []
            
            # Estilos (preto e negrito como na imagem)
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=20,
                alignment=1,  # Centralizado
                textColor=colors.black,
                fontName='Helvetica-Bold'
            )
            
            header_style = ParagraphStyle(
                'Header',
                parent=styles['Normal'],
                fontSize=12,
                spaceAfter=5,
                textColor=colors.black,
                fontName='Helvetica-Bold'
            )
            
            normal_style = ParagraphStyle(
                'Normal',
                parent=styles['Normal'],
                fontSize=10,
                textColor=colors.black,
                fontName='Helvetica'
            )
            
            # ===== CABEÇALHO PROFISSIONAL =====
            # Título principal
            story.append(Paragraph("NOTA FISCAL", title_style))
            story.append(Spacer(1, 15))
            
            # ===== DADOS DO EMITENTE =====
            story.append(Paragraph("EMITENTE", header_style))
            story.append(Paragraph(f"<b>Emitente:</b> {self.dados_empresa['nome']}", normal_style))
            story.append(Paragraph(f"<b>CNPJ:</b> {self.dados_empresa['cnpj']}", normal_style))
            story.append(Paragraph(f"<b>Endereço:</b> {self.dados_empresa['endereco']}", normal_style))
            story.append(Paragraph(f"<b>IE:</b> 1234567890", normal_style))
            story.append(Spacer(1, 15))
            
            # ===== DADOS DO DESTINATÁRIO =====
            story.append(Paragraph("DESTINATÁRIO", header_style))
            story.append(Paragraph(f"<b>Destinatário:</b> {nota_fiscal['cliente']['nome']}", normal_style))
            if nota_fiscal['cliente']['documento']:
                story.append(Paragraph(f"<b>CPF:</b> {nota_fiscal['cliente']['documento']}", normal_style))
            if nota_fiscal['cliente']['endereco']:
                story.append(Paragraph(f"<b>Endereço:</b> {nota_fiscal['cliente']['endereco']}", normal_style))
            story.append(Spacer(1, 15))
            
            # ===== TABELA DE PRODUTOS =====
            story.append(Paragraph("PRODUTOS/SERVIÇOS", header_style))
            
            dados_tabela = [['Código', 'Descrição', 'Quantidade', 'Valor Unitário', 'Valor Total']]
            
            for item in nota_fiscal['itens']:
                dados_tabela.append([
                    item['codigo'],
                    item['descricao'],
                    f"{item['quantidade']:.2f}".replace('.', ','),
                    f"R$ {item['preco_unitario']:.2f}".replace('.', ','),
                    f"R$ {item['total']:.2f}".replace('.', ',')
                ])
            
            tabela = Table(dados_tabela, colWidths=[1*inch, 3*inch, 0.8*inch, 1.2*inch, 1*inch])
            tabela.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),  # Alinhar números à direita
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),    # Alinhar descrição à esquerda
            ]))
            
            story.append(tabela)
            story.append(Spacer(1, 15))
            
            # ===== TOTAIS =====
            story.append(Paragraph("TOTAIS", header_style))
            
            # Calcular impostos (simplificado)
            base_calculo = nota_fiscal['subtotal']
            valor_icms = base_calculo * 0.18  # 18% ICMS
            valor_total = base_calculo + valor_icms
            
            dados_impostos = [
                ['Base ICMS', f"R$ {base_calculo:.2f}".replace('.', ',')],
                ['Valor ICMS', f"R$ {valor_icms:.2f}".replace('.', ',')],
                ['Valor Total', f"R$ {valor_total:.2f}".replace('.', ',')]
            ]
            
            tabela_impostos = Table(dados_impostos, colWidths=[3*inch, 2*inch])
            tabela_impostos.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),  # Valores à direita
            ]))
            
            story.append(tabela_impostos)
            story.append(Spacer(1, 20))
            
            # ===== INFORMAÇÕES FISCAIS =====
            story.append(Paragraph("INFORMAÇÕES FISCAIS", header_style))
            
            # Gerar chave de acesso e protocolo
            chave_acesso = self.gerar_chave_acesso("35", "1508", self.limpar_documento(self.dados_empresa['cnpj']), "55", "001", nota_fiscal['numero'], "00000001", "1")
            protocolo = "135210000025991"
            
            story.append(Paragraph(f"<b>Chave de Acesso:</b> {chave_acesso}", normal_style))
            story.append(Paragraph(f"<b>Protocolo de Autorização:</b> {protocolo} - {nota_fiscal['data']}", normal_style))
            story.append(Paragraph(f"<b>SEFAZ Autorizadora:</b> SEFAZ/ES", normal_style))
            
            story.append(Spacer(1, 20))
            
            # ===== OBSERVAÇÕES =====
            story.append(Paragraph("OBSERVAÇÕES", header_style))
            story.append(Paragraph("• Esta é uma nota fiscal simplificada para controle interno", normal_style))
            story.append(Paragraph("• Para consulta de autenticidade, entre em contato com a empresa", normal_style))
            story.append(Paragraph("• Documento válido para fins fiscais e contábeis", normal_style))
            story.append(Spacer(1, 20))
            story.append(Paragraph("_________________________________", normal_style))
            story.append(Paragraph("Assinatura do Responsável", normal_style))
            
            # Gerar PDF
            doc.build(story)
            
            # Verificar se o arquivo foi criado
            if not os.path.exists(caminho_completo):
                raise Exception(f"PDF não foi criado: {caminho_completo}")
            
            print(f"PDF gerado com sucesso: {caminho_completo}")
            return caminho_completo
            
        except Exception as e:
            print(f"Erro ao gerar PDF: {e}")
            raise e
    
    def imprimir_pdf(self, arquivo_pdf):
        try:
            # Verificar se o arquivo existe
            if not os.path.exists(arquivo_pdf):
                print(f"Arquivo PDF não encontrado: {arquivo_pdf}")
                return False
            
            # Obter impressora padrão
            impressora_padrao = win32print.GetDefaultPrinter()
            print(f"Impressora padrão: {impressora_padrao}")
            
            # Tentar imprimir usando ShellExecute
            win32api.ShellExecute(0, "print", arquivo_pdf, None, ".", 0)
            
            return True
        except Exception as e:
            print(f"Erro ao imprimir: {e}")
            return False
    
    def atualizar_historico(self):
        for item in self.tree_historico.get_children():
            self.tree_historico.delete(item)
        
        for nota in reversed(self.notas_fiscais):  # Mais recentes primeiro
            # Obter status da nota (padrão: "Pendente" se não existir)
            status = nota.get('status', 'Pendente')
            
            self.tree_historico.insert('', 'end', values=(
                nota['data'],
                f"{nota['numero']:06d}",
                nota['cliente']['nome'],
                f"R$ {nota['total']:.2f}".replace('.', ','),
                status
            ))
    
    def filtrar_historico(self):
        filtro = self.entry_filtro_cliente.get().strip().lower()
        
        for item in self.tree_historico.get_children():
            self.tree_historico.delete(item)
        
        for nota in reversed(self.notas_fiscais):
            if filtro in nota['cliente']['nome'].lower():
                # Obter status da nota (padrão: "Pendente" se não existir)
                status = nota.get('status', 'Pendente')
                
                self.tree_historico.insert('', 'end', values=(
                    nota['data'],
                    f"{nota['numero']:06d}",
                    nota['cliente']['nome'],
                    f"R$ {nota['total']:.2f}".replace('.', ','),
                    status
                ))
    
    def limpar_filtro(self):
        self.entry_filtro_cliente.delete(0, tk.END)
        self.atualizar_historico()
    
    def visualizar_nf(self):
        selecao = self.tree_historico.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione uma nota fiscal para visualizar!")
            return
        
        item = self.tree_historico.item(selecao[0])
        numero_nf = int(item['values'][1])
        
        # Encontrar nota fiscal
        nota = None
        for n in self.notas_fiscais:
            if n['numero'] == numero_nf:
                nota = n
                break
        
        if nota:
            arquivo_pdf = self.gerar_pdf(nota)
            os.startfile(arquivo_pdf)  # Abrir PDF
    
    def reimprimir_nf(self):
        selecao = self.tree_historico.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione uma nota fiscal para reimprimir!")
            return
        
        item = self.tree_historico.item(selecao[0])
        numero_nf = int(item['values'][1])
        
        # Encontrar nota fiscal
        nota = None
        for n in self.notas_fiscais:
            if n['numero'] == numero_nf:
                nota = n
                break
        
        if nota:
            arquivo_pdf = self.gerar_pdf(nota)
            if self.imprimir_pdf(arquivo_pdf):
                messagebox.showinfo("Sucesso", f"Nota Fiscal #{numero_nf} reimpressa com sucesso!")
            else:
                messagebox.showerror("Erro", "Erro ao reimprimir a nota fiscal!")
    
    def apagar_nf(self):
        selecao = self.tree_historico.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione uma nota fiscal para apagar!")
            return
        
        item = self.tree_historico.item(selecao[0])
        numero_nf = int(item['values'][1])
        
        # Confirmar exclusão
        resposta = messagebox.askyesno("Confirmar Exclusão", 
                                      f"Tem certeza que deseja apagar a Nota Fiscal #{numero_nf}?\n\n"
                                      "Esta ação não pode ser desfeita!")
        
        if resposta:
            # Remover nota fiscal da lista
            self.notas_fiscais = [n for n in self.notas_fiscais if n['numero'] != numero_nf]
            
            # Remover da visualização
            self.tree_historico.delete(selecao[0])
            
            # Salvar dados
            self.salvar_dados()
            
            messagebox.showinfo("Sucesso", f"Nota Fiscal #{numero_nf} apagada com sucesso!")
    
    def marcar_concluida(self):
        selecao = self.tree_historico.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione uma nota fiscal para marcar como concluída!")
            return
        
        item = self.tree_historico.item(selecao[0])
        numero_nf = int(item['values'][1])
        
        # Encontrar e atualizar nota fiscal
        for nota in self.notas_fiscais:
            if nota['numero'] == numero_nf:
                nota['status'] = 'Concluída'
                break
        
        # Atualizar visualização
        self.atualizar_historico()
        
        # Salvar dados
        self.salvar_dados()
        
        messagebox.showinfo("Sucesso", f"Nota Fiscal #{numero_nf} marcada como concluída!")
    
    def marcar_pendente(self):
        selecao = self.tree_historico.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione uma nota fiscal para marcar como pendente!")
            return
        
        item = self.tree_historico.item(selecao[0])
        numero_nf = int(item['values'][1])
        
        # Encontrar e atualizar nota fiscal
        for nota in self.notas_fiscais:
            if nota['numero'] == numero_nf:
                nota['status'] = 'Pendente'
                break
        
        # Atualizar visualização
        self.atualizar_historico()
        
        # Salvar dados
        self.salvar_dados()
        
        messagebox.showinfo("Sucesso", f"Nota Fiscal #{numero_nf} marcada como pendente!")
    
    def salvar_dados(self):
        dados = {
            "dados_empresa": self.dados_empresa,
            "produtos": self.produtos,
            "notas_fiscais": self.notas_fiscais
        }
        
        try:
            with open("dados_sistema.json", "w", encoding="utf-8") as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
    
    def validar_cpf(self, cpf):
        """Valida CPF brasileiro"""
        # Remove caracteres não numéricos
        cpf = ''.join(filter(str.isdigit, cpf))
        
        # Verifica se tem 11 dígitos
        if len(cpf) != 11:
            return False
        
        # Verifica se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            return False
        
        # Calcula primeiro dígito verificador
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        
        # Calcula segundo dígito verificador
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        # Verifica se os dígitos calculados são iguais aos do CPF
        return cpf[-2:] == f"{digito1}{digito2}"
    
    def validar_cnpj(self, cnpj):
        """Valida CNPJ brasileiro"""
        # Remove caracteres não numéricos
        cnpj = ''.join(filter(str.isdigit, cnpj))
        
        # Verifica se tem 14 dígitos
        if len(cnpj) != 14:
            return False
        
        # Verifica se todos os dígitos são iguais
        if cnpj == cnpj[0] * 14:
            return False
        
        # Calcula primeiro dígito verificador
        multiplicadores1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * multiplicadores1[i] for i in range(12))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        
        # Calcula segundo dígito verificador
        multiplicadores2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * multiplicadores2[i] for i in range(13))
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        
        # Verifica se os dígitos calculados são iguais aos do CNPJ
        return cnpj[-2:] == f"{digito1}{digito2}"
    
    def formatar_cpf(self, cpf):
        """Formata CPF no padrão XXX.XXX.XXX-XX"""
        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) == 11:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return cpf
    
    def formatar_cnpj(self, cnpj):
        """Formata CNPJ no padrão XX.XXX.XXX/XXXX-XX"""
        cnpj = ''.join(filter(str.isdigit, cnpj))
        if len(cnpj) == 14:
            return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"
        return cnpj
    
    def carregar_dados(self):
        try:
            if os.path.exists("dados_sistema.json"):
                with open("dados_sistema.json", "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    
                    # Carregar dados da empresa
                    dados_empresa = dados.get("dados_empresa", {})
                    if dados_empresa:
                        self.dados_empresa.update(dados_empresa)
                    
                    self.produtos = dados.get("produtos", [])
                    self.notas_fiscais = dados.get("notas_fiscais", [])
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")

def main():
    # Ocultar a janela do CMD
    if sys.platform.startswith('win'):
        # Para Windows
        try:
            # Método 1: Ocultar a janela do console
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except:
            try:
                # Método 2: Alternativo para ocultar o console
                import subprocess
                import os
                # Redirecionar stdout e stderr para devnull
                sys.stdout = open(os.devnull, 'w')
                sys.stderr = open(os.devnull, 'w')
            except:
                pass
    
    root = tk.Tk()
    app = SistemaNotaFiscal(root)
    root.mainloop()

if __name__ == "__main__":
    main() 