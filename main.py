import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser
import pyttsx3
from datetime import datetime
from fpdf import FPDF

# ========== CONFIGURAÇÕES GLOBAIS ==========
USUARIOS = {"admin": "admin"}
# Os dados de médicos e CRMs abaixo são meramente fictícios e ilustrativos, utilizados apenas para exemplo. &copy; joaolacerdaconsorte.
MEDICOS = [
    {"nome": "Dr. João Silva", "especialidade": "Cardiologia", "crm": "12345-SP", "horarios": ["08:00", "09:00", "10:00", "14:00", "15:00", "16:00"]},
    {"nome": "Dra. Maria Souza", "especialidade": "Neurologia", "crm": "23456-SP", "horarios": ["08:30", "09:30", "10:30", "14:30", "15:30", "16:30"]},
    {"nome": "Dr. Pedro Lima", "especialidade": "Ortopedia", "crm": "34567-SP", "horarios": ["09:00", "10:00", "11:00", "15:00", "16:00", "17:00"]},
    {"nome": "Dra. Ana Paula", "especialidade": "Pediatria", "crm": "45678-SP", "horarios": ["08:00", "09:00", "10:00", "14:00", "15:00", "16:00"]},
    {"nome": "Dr. Lucas Rocha", "especialidade": "Ginecologia", "crm": "56789-SP", "horarios": ["08:30", "09:30", "10:30", "14:30", "15:30", "16:30"]},
    {"nome": "Dr. Carlos Santos", "especialidade": "Dermatologia", "crm": "67890-SP", "horarios": ["09:00", "10:00", "11:00", "15:00", "16:00", "17:00"]},
    {"nome": "Dra. Juliana Costa", "especialidade": "Oftalmologia", "crm": "78901-SP", "horarios": ["08:00", "09:00", "10:00", "14:00", "15:00", "16:00"]},
    {"nome": "Dr. Rafael Oliveira", "especialidade": "Urologia", "crm": "89012-SP", "horarios": ["08:30", "09:30", "10:30", "14:30", "15:30", "16:30"]},
    {"nome": "Dra. Beatriz Lima", "especialidade": "Endocrinologia", "crm": "90123-SP", "horarios": ["09:00", "10:00", "11:00", "15:00", "16:00", "17:00"]},
    {"nome": "Dr. Gabriel Martins", "especialidade": "Gastroenterologia", "crm": "01234-SP", "horarios": ["08:00", "09:00", "10:00", "14:00", "15:00", "16:00"]}
]

ESPECIALIDADES = [
    {"nome": "Cardiologia", "icone": "❤️", "descricao": "Especialidade médica que se ocupa do diagnóstico e tratamento das doenças que acometem o coração."},
    {"nome": "Neurologia", "icone": "🧠", "descricao": "Especialidade médica que trata dos distúrbios estruturais do sistema nervoso."},
    {"nome": "Ortopedia", "icone": "🦴", "descricao": "Especialidade médica que cuida das doenças e deformidades dos ossos, músculos, ligamentos e articulações."},
    {"nome": "Pediatria", "icone": "👶", "descricao": "Especialidade médica dedicada à assistência da criança e do adolescente."},
    {"nome": "Ginecologia", "icone": "👩", "descricao": "Especialidade médica que trata da saúde do sistema reprodutor feminino."},
    {"nome": "Dermatologia", "icone": "🧴", "descricao": "Especialidade médica que se ocupa do diagnóstico e tratamento de doenças da pele."},
    {"nome": "Oftalmologia", "icone": "👁️", "descricao": "Especialidade médica que estuda e trata as doenças relacionadas aos olhos."},
    {"nome": "Urologia", "icone": "🔬", "descricao": "Especialidade médica que trata do trato urinário de homens e mulheres."},
    {"nome": "Endocrinologia", "icone": "⚖️", "descricao": "Especialidade médica que trata dos distúrbios das glândulas endócrinas."},
    {"nome": "Gastroenterologia", "icone": "🍽️", "descricao": "Especialidade médica que se ocupa do estudo, diagnóstico e tratamento clínico das doenças do aparelho digestivo."}
]

CONSULTAS = []
NOTIFICACOES = [
    "Bem-vindo ao sistema!",
    "Lembre-se de atualizar seus dados.",
    "Novos horários disponíveis para agendamento.",
    "Confira as especialidades disponíveis."
]

# ========== ACESSIBILIDADE ==========
engine = pyttsx3.init()
def falar_texto(texto):
    try:
        engine.say(texto)
        engine.runAndWait()
    except Exception:
        pass

# ========== PDF ==========
def exportar_historico_pdf(consultas):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 20, "Hospital das Clínicas", ln=True, align="C")
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Histórico de Consultas", ln=True, align="C")
    pdf.ln(10)
    
    # Data e hora da exportação
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 5, f"Exportado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.ln(5)
    
    # Tabela de consultas
    pdf.set_font("Arial", "B", 12)
    pdf.cell(40, 10, "Paciente", 1)
    pdf.cell(40, 10, "Especialidade", 1)
    pdf.cell(40, 10, "Médico", 1)
    pdf.cell(30, 10, "Data", 1)
    pdf.cell(30, 10, "Hora", 1)
    pdf.cell(30, 10, "Agendado em", 1)
    pdf.ln()
    
    pdf.set_font("Arial", size=10)
    for c in consultas:
        pdf.cell(40, 8, c['paciente'], 1)
        pdf.cell(40, 8, c['especialidade'], 1)
        pdf.cell(40, 8, c['medico'], 1)
        pdf.cell(30, 8, c['data'], 1)
        pdf.cell(30, 8, c['hora'], 1)
        pdf.cell(30, 8, c['agendado_em'], 1)
        pdf.ln()
    
    # Rodapé
    pdf.ln(10)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 5, "Este documento foi gerado automaticamente pelo sistema do Hospital das Clínicas.", ln=True)
    pdf.cell(0, 5, "© 2025 joaolacerdaconsorte Hospital das Clínicas - Todos os direitos reservados", ln=True)
    
    caminho = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if caminho:
        pdf.output(caminho)
        messagebox.showinfo("Exportação", "Histórico exportado com sucesso!")

# ========== LOGIN ==========
class LoginScreen(ctk.CTkFrame):
    def __init__(self, master, callback_login):
        super().__init__(master, fg_color=("#eaf0fa", "#181a20"))
        self.callback_login = callback_login
        self.pack(fill="both", expand=True)
        self.build()
        
    def build(self):
        # Frame principal com gradiente
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=50, pady=50)
        
        # Frame do formulário com efeito de vidro
        form_frame = ctk.CTkFrame(main_frame, fg_color=("#ffffff", "#23272f"), corner_radius=20)
        form_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Logo e título
        ctk.CTkLabel(form_frame, text="🏥", font=("Segoe UI", 48)).pack(pady=(40, 10))
        ctk.CTkLabel(form_frame, text="Hospital das Clínicas", 
                     font=("Segoe UI", 28, "bold"), 
                     text_color=("#1e40af", "#93c5fd")).pack(pady=5)
        ctk.CTkLabel(form_frame, text="Saúde Digital", 
                     font=("Segoe UI", 18, "italic"), 
                     text_color=("#2563eb", "#60a5fa")).pack(pady=5)
        
        # Separador
        ctk.CTkFrame(form_frame, height=2, fg_color=("#e5e7eb", "#374151")).pack(fill="x", padx=50, pady=20)
        
        # Formulário de login
        ctk.CTkLabel(form_frame, text="Login", 
                     font=("Segoe UI", 20, "bold"), 
                     text_color=("#2563eb", "#60a5fa")).pack(pady=10)
        
        # Campos de entrada com ícones
        self.user_entry = ctk.CTkEntry(form_frame, 
                                      placeholder_text="👤 Usuário", 
                                      width=300, 
                                      height=40,
                                      corner_radius=10)
        self.user_entry.pack(pady=10)
        
        self.pass_entry = ctk.CTkEntry(form_frame, 
                                      placeholder_text="🔒 Senha", 
                                      show="*", 
                                      width=300, 
                                      height=40,
                                      corner_radius=10)
        self.pass_entry.pack(pady=10)
        
        # Mensagem de erro
        self.msg = ctk.CTkLabel(form_frame, text="", text_color="red")
        self.msg.pack(pady=5)
        
        # Botões
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(btn_frame, 
                      text="Entrar", 
                      fg_color="#2563eb", 
                      hover_color="#1e40af", 
                      width=140, 
                      height=40,
                      corner_radius=10, 
                      command=self.login).pack(side="left", padx=5)
        
        ctk.CTkButton(btn_frame, 
                      text="Entrar sem Cadastro", 
                      fg_color="#4b5563", 
                      hover_color="#374151", 
                      width=140, 
                      height=40,
                      corner_radius=10, 
                      command=self.entrar_sem_cadastro).pack(side="left", padx=5)
        
        # Rodapé
        ctk.CTkLabel(form_frame, 
                     text="© 2025 joaolacerdaconsorte Hospital das Clínicas - Todos os direitos reservados", 
                     font=("Segoe UI", 10), 
                     text_color=("#6b7280", "#9ca3af")).pack(pady=20)

    def login(self):
        user = self.user_entry.get()
        pw = self.pass_entry.get()
        if user in USUARIOS and USUARIOS[user] == pw:
            self.callback_login()
        else:
            self.msg.configure(text="Usuário ou senha inválidos!")

    def entrar_sem_cadastro(self):
        self.callback_login()

# ========== MENU LATERAL ==========
class MenuLateral(ctk.CTkFrame):
    def __init__(self, master, callback_tela):
        super().__init__(master, width=250, corner_radius=0, fg_color=("#f5f8ff", "#23272f"))
        self.callback_tela = callback_tela
        self.pack_propagate(False)
        self.menu_aberto = True
        self.tela_atual = "home"
        self.build()

    def build(self):
        # Cabeçalho do menu
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(20, 10))
        
        self.menu_btn = ctk.CTkButton(header_frame, 
                                     text="☰", 
                                     width=40, 
                                     height=40,
                                     fg_color="#2563eb", 
                                     hover_color="#1e40af", 
                                     command=self.toggle_menu, 
                                     font=("Segoe UI", 18, "bold"),
                                     corner_radius=10)
        self.menu_btn.pack(side="left", padx=5)
        
        ctk.CTkLabel(header_frame, 
                     text="Menu", 
                     font=("Segoe UI", 20, "bold"),
                     text_color=("#1e40af", "#93c5fd")).pack(side="left", padx=10)
        
        # Separador
        ctk.CTkFrame(self, height=2, fg_color=("#e5e7eb", "#374151")).pack(fill="x", padx=20, pady=10)
        
        # Botões do menu
        self.botoes = []
        opcoes = [
            ("🏠 Home", self.ir_home),
            ("📅 Agendar Consulta", self.ir_agendar),
            ("📋 Histórico", self.ir_historico),
            ("👨‍⚕️ Médicos", self.ir_medicos),
            ("⚙️ Configurações", self.ir_config),
            ("ℹ️ Sobre", self.ir_sobre),
            ("❓ Ajuda", self.ir_ajuda),
            ("🔔 Notificações", self.ir_notificacoes),
            ("📤 Exportar PDF", self.ir_exportar),
            ("🚪 Sair", self.ir_sair)
        ]
        
        for texto, comando in opcoes:
            btn = ctk.CTkButton(self, 
                               text=texto, 
                               width=220, 
                               height=40,
                               fg_color="#2563eb", 
                               hover_color="#1e40af", 
                               corner_radius=10, 
                               command=comando, 
                               font=("Segoe UI", 14),
                               anchor="w")
            btn.pack(pady=5, padx=15)
            self.botoes.append(btn)
            
            # Adicionar eventos de mouse
            btn.bind("<Enter>", lambda e, b=btn: self.on_hover(b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_leave(b))
        
        # Rodapé do menu
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(footer_frame, 
                     text="v1.0.0", 
                     font=("Segoe UI", 10),
                     text_color=("#6b7280", "#9ca3af")).pack(side="left", padx=10)
        
        ctk.CTkLabel(footer_frame, 
                     text="© 2025 joaolacerdaconsorte", 
                     font=("Segoe UI", 10),
                     text_color=("#6b7280", "#9ca3af")).pack(side="right", padx=10)

    def on_hover(self, button):
        if button.cget("text") != self.tela_atual:
            button.configure(fg_color="#1e40af", hover_color="#1e40af")

    def on_leave(self, button):
        if button.cget("text") != self.tela_atual:
            button.configure(fg_color="#2563eb", hover_color="#1e40af")

    def toggle_menu(self):
        if self.menu_aberto:
            for btn in self.botoes:
                btn.pack_forget()
            self.menu_aberto = False
        else:
            for btn in self.botoes:
                btn.pack(pady=5, padx=15)
            self.menu_aberto = True

    def atualizar_tela_atual(self, tela):
        self.tela_atual = tela
        for btn in self.botoes:
            if btn.cget("text") == tela:
                btn.configure(fg_color="#1e40af", hover_color="#1e40af")
            else:
                btn.configure(fg_color="#2563eb", hover_color="#1e40af")

    def ir_home(self): 
        self.atualizar_tela_atual("🏠 Home")
        self.callback_tela("home")
    def ir_agendar(self): 
        self.atualizar_tela_atual("📅 Agendar Consulta")
        self.callback_tela("agendar")
    def ir_historico(self): 
        self.atualizar_tela_atual("📋 Histórico")
        self.callback_tela("historico")
    def ir_medicos(self): 
        self.atualizar_tela_atual("👨‍⚕️ Médicos")
        self.callback_tela("medicos")
    def ir_config(self): 
        self.atualizar_tela_atual("⚙️ Configurações")
        self.callback_tela("config")
    def ir_sobre(self): 
        self.atualizar_tela_atual("ℹ️ Sobre")
        self.callback_tela("sobre")
    def ir_ajuda(self): 
        self.atualizar_tela_atual("❓ Ajuda")
        self.callback_tela("ajuda")
    def ir_notificacoes(self): 
        self.atualizar_tela_atual("🔔 Notificações")
        self.callback_tela("notificacoes")
    def ir_exportar(self): 
        self.atualizar_tela_atual("📤 Exportar PDF")
        self.callback_tela("exportar")
    def ir_sair(self): 
        self.callback_tela("sair")

# ========== APP PRINCIPAL ==========
class HospitalApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hospital das Clínicas - Sistema Profissional")
        self.geometry("1050x700")
        # Configuração inicial do tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.tema_atual = "Claro"
        self.login_screen = LoginScreen(self, self.iniciar_app)
        self.menu = None
        self.container = None
        self.telas = {}
        self.tela_atual = None
    def iniciar_app(self):
        self.login_screen.pack_forget()
        self.menu = MenuLateral(self, self.mudar_tela)
        self.menu.pack(side="left", fill="y")
        self.container = ctk.CTkFrame(self, fg_color=("#eaf0fa", "#181a20"))
        self.container.pack(side="left", fill="both", expand=True)
        self.mudar_tela("home")
    def mudar_tela(self, tela):
        if self.tela_atual:
            self.telas[self.tela_atual].pack_forget()
        if tela not in self.telas:
            if tela == "home":
                self.telas[tela] = self.criar_home()
            elif tela == "agendar":
                self.telas[tela] = self.criar_agendamento()
            elif tela == "historico":
                self.telas[tela] = self.criar_historico()
            elif tela == "medicos":
                self.telas[tela] = self.criar_medicos()
            elif tela == "config":
                self.telas[tela] = self.criar_configuracoes()
            elif tela == "sobre":
                self.telas[tela] = self.criar_sobre()
            elif tela == "ajuda":
                self.telas[tela] = self.criar_ajuda()
            elif tela == "notificacoes":
                self.telas[tela] = self.criar_notificacoes()
            elif tela == "exportar":
                exportar_historico_pdf(CONSULTAS)
                return
            elif tela == "sair":
                self.destroy()
                return
        self.telas[tela].pack(fill="both", expand=True)
        self.tela_atual = tela
    def criar_home(self):
        cores = self.get_cores_tema()
        frame = ctk.CTkFrame(self.container, fg_color=(cores["bg"], cores["fg"]))
        
        # Cabeçalho com gradiente
        header_frame = ctk.CTkFrame(frame, fg_color=(cores["bg"], cores["fg"]))
        header_frame.pack(fill="x", padx=30, pady=30)
        
        titulo = ctk.CTkLabel(header_frame, 
                             text="Bem-vindo ao Sistema do Hospital das Clínicas", 
                             font=("Segoe UI", 26, "bold"), 
                             text_color=(cores["titulo"], cores["titulo"]))
        titulo.pack(pady=10)
        
        subtitulo = ctk.CTkLabel(header_frame, 
                                text="Saúde Digital: tecnologia a serviço do seu bem-estar.", 
                                font=("Segoe UI", 18), 
                                text_color=(cores["subtitulo"], cores["subtitulo"]))
        subtitulo.pack(pady=5)
        
        # Mensagem informativa
        ctk.CTkLabel(
            frame,
            text="Este sistema é uma demonstração do Hospital das Clínicas. Todos os dados de médicos, pacientes e consultas são fictícios e utilizados apenas para fins ilustrativos. Para dúvidas ou sugestões, entre em contato: joaovitorlacerda51@gmail.com",
            font=("Segoe UI", 14),
            text_color=(cores["texto"], cores["texto"]),
            wraplength=900,
            justify="center"
        ).pack(pady=10)
        
        # Separador
        ctk.CTkFrame(frame, height=2, fg_color=("#e5e7eb", "#374151")).pack(fill="x", padx=50, pady=20)
        
        # Cards de estatísticas
        stats_frame = ctk.CTkFrame(frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=30, pady=20)
        
        # Card de Consultas
        consultas_card = ctk.CTkFrame(stats_frame, fg_color=(cores["bg"], cores["fg"]), corner_radius=15)
        consultas_card.pack(side="left", fill="both", expand=True, padx=10)
        ctk.CTkLabel(consultas_card, text="📅", font=("Segoe UI", 32)).pack(pady=(20, 5))
        ctk.CTkLabel(consultas_card, text=f"{len(CONSULTAS)}", font=("Segoe UI", 24, "bold"), text_color=(cores["titulo"], cores["titulo"])).pack()
        ctk.CTkLabel(consultas_card, text="Consultas Agendadas", font=("Segoe UI", 14), text_color=(cores["texto"], cores["texto"])).pack(pady=(0, 20))
        
        # Espaço informativo entre os cards
        info_label = ctk.CTkLabel(stats_frame, text="Dica: Use o menu ao lado para navegar pelo sistema!", font=("Segoe UI", 16, "italic"), text_color=(cores["subtitulo"], cores["subtitulo"]))
        info_label.pack(side="left", fill="both", expand=True)
        
        # Card de Médicos
        medicos_card = ctk.CTkFrame(stats_frame, fg_color=(cores["bg"], cores["fg"]), corner_radius=15)
        medicos_card.pack(side="left", fill="both", expand=True, padx=10)
        ctk.CTkLabel(medicos_card, text="👨‍⚕️", font=("Segoe UI", 32)).pack(pady=(20, 5))
        ctk.CTkLabel(medicos_card, text=f"{len(MEDICOS)}", font=("Segoe UI", 24, "bold"), text_color=(cores["titulo"], cores["titulo"])).pack()
        ctk.CTkLabel(medicos_card, text="Médicos Cadastrados", font=("Segoe UI", 14), text_color=(cores["texto"], cores["texto"])).pack(pady=(0, 20))
        
        # Área de ações rápidas centralizada
        acoes_frame = ctk.CTkFrame(frame, fg_color="transparent")
        acoes_frame.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(acoes_frame, 
            text="Ações Rápidas", 
            font=("Segoe UI", 20, "bold"), 
            text_color=(cores["titulo"], cores["titulo"])).pack(pady=10)
        botoes_frame = ctk.CTkFrame(acoes_frame, fg_color="transparent")
        botoes_frame.pack(fill="x", pady=10)
        ctk.CTkButton(botoes_frame, 
            text="📅 Agendar Consulta", 
            fg_color=cores["botao"], 
            hover_color=cores["botao_hover"],
            width=200, 
            height=40,
            corner_radius=10,
            command=lambda: self.mudar_tela("agendar")).pack(side="left", padx=5)
        ctk.CTkButton(botoes_frame, 
            text="👨‍⚕️ Ver Médicos", 
            fg_color=cores["botao"], 
            hover_color=cores["botao_hover"],
            width=200, 
            height=40,
            corner_radius=10,
            command=lambda: self.mudar_tela("medicos")).pack(side="left", padx=5)
        ctk.CTkButton(botoes_frame, 
            text="📋 Histórico", 
            fg_color=cores["botao"], 
            hover_color=cores["botao_hover"],
            width=200, 
            height=40,
            corner_radius=10,
            command=lambda: self.mudar_tela("historico")).pack(side="left", padx=5)
        ctk.CTkButton(botoes_frame, 
            text="🔊 Descrição em Áudio", 
            fg_color=cores["botao"], 
            hover_color=cores["botao_hover"],
            width=200, 
            height=40,
            corner_radius=10,
            command=lambda: falar_texto("Bem-vindo ao Sistema do Hospital das Clínicas. Saúde Digital: tecnologia a serviço do seu bem-estar. Agende consultas, acesse informações médicas, conheça nossos profissionais e muito mais!")).pack(side="left", padx=5)
        
        return frame
    def criar_agendamento(self):
        cores = self.get_cores_tema()
        frame = ctk.CTkFrame(self.container, fg_color=(cores["bg"], cores["fg"]), corner_radius=20)
        
        # Cabeçalho com gradiente
        header_frame = ctk.CTkFrame(frame, fg_color=(cores["bg"], cores["fg"]))
        header_frame.pack(fill="x", padx=30, pady=30)
        
        titulo = ctk.CTkLabel(header_frame, 
                             text="📅 Agendar Consulta", 
                             font=("Segoe UI", 26, "bold"), 
                             text_color=(cores["titulo"], cores["titulo"]))
        titulo.pack(pady=10)
        
        subtitulo = ctk.CTkLabel(header_frame, 
                                text="Preencha os dados abaixo para agendar sua consulta", 
                                font=("Segoe UI", 16), 
                                text_color=(cores["subtitulo"], cores["subtitulo"]))
        subtitulo.pack(pady=5)
        
        # Separador
        ctk.CTkFrame(frame, height=2, fg_color=("#e5e7eb", "#374151")).pack(fill="x", padx=50, pady=20)
        
        # Frame do formulário com duas colunas
        form_frame = ctk.CTkFrame(frame, fg_color="transparent")
        form_frame.pack(fill="x", padx=50, pady=20)
        
        # Coluna esquerda
        coluna_esquerda = ctk.CTkFrame(form_frame, fg_color="transparent")
        coluna_esquerda.pack(side="left", fill="both", expand=True, padx=10)
        
        # Nome do Paciente
        nome_label = ctk.CTkLabel(coluna_esquerda, 
                                 text="👤 Nome do Paciente:", 
                                 font=("Segoe UI", 14, "bold"),
                                 text_color=(cores["texto"], cores["texto"]))
        nome_label.pack(pady=5)
        
        self.nome_entry = ctk.CTkEntry(coluna_esquerda, 
                                      width=400, 
                                      height=40,
                                      corner_radius=10,
                                      placeholder_text="Digite seu nome completo")
        self.nome_entry.pack(pady=5)
        
        # Especialidade
        especialidade_label = ctk.CTkLabel(coluna_esquerda, 
                                         text="🏥 Especialidade:", 
                                         font=("Segoe UI", 14, "bold"),
                                         text_color=(cores["texto"], cores["texto"]))
        especialidade_label.pack(pady=5)
        
        self.especialidade_combo = ctk.CTkComboBox(coluna_esquerda, 
                                                  values=[e["nome"] for e in ESPECIALIDADES], 
                                                  width=400, 
                                                  height=40,
                                                  corner_radius=10,
                                                  command=self.atualizar_medicos)
        self.especialidade_combo.pack(pady=5)
        
        # Botão azul "Confirmar Agendamento" na coluna esquerda
        confirmar_btn = ctk.CTkButton(
            coluna_esquerda,
            text="Confirmar Agendamento",
            fg_color="#2563eb",
            hover_color="#1e40af",
            font=("Segoe UI", 14, "bold"),
            width=400,
            height=45,
            corner_radius=10,
            command=self.agendar_consulta
        )
        confirmar_btn.pack(pady=30)
        
        # Coluna direita
        coluna_direita = ctk.CTkFrame(form_frame, fg_color="transparent")
        coluna_direita.pack(side="right", fill="both", expand=True, padx=10)
        
        # Médico
        medico_label = ctk.CTkLabel(coluna_direita, 
                                  text="👨‍⚕️ Médico:", 
                                  font=("Segoe UI", 14, "bold"),
                                  text_color=(cores["texto"], cores["texto"]))
        medico_label.pack(pady=5)
        
        self.medico_combo = ctk.CTkComboBox(coluna_direita, 
                                           values=[m['nome'] for m in MEDICOS], 
                                           width=400, 
                                           height=40,
                                           corner_radius=10,
                                           command=self.atualizar_horarios)
        self.medico_combo.pack(pady=5)
        
        # Data
        data_label = ctk.CTkLabel(coluna_direita, 
                                text="📅 Data da Consulta:", 
                                font=("Segoe UI", 14, "bold"),
                                text_color=(cores["texto"], cores["texto"]))
        data_label.pack(pady=5)
        
        self.data_entry = ctk.CTkEntry(coluna_direita, 
                                      width=400, 
                                      height=40,
                                      corner_radius=10,
                                      placeholder_text="DD/MM/AAAA")
        self.data_entry.pack(pady=5)
        self.data_entry.bind("<KeyRelease>", self.formatar_data)
        
        # Horário
        horario_label = ctk.CTkLabel(coluna_direita, 
                                   text="⏰ Horário:", 
                                   font=("Segoe UI", 14, "bold"),
                                   text_color=(cores["texto"], cores["texto"]))
        horario_label.pack(pady=5)
        
        # Horários genéricos
        horarios_genericos = ["08:00", "09:00", "10:00", "11:00", "14:00", "15:00"]
        self.horario_combo = ctk.CTkComboBox(coluna_direita, 
                                            values=horarios_genericos, 
                                            width=400, 
                                            height=40,
                                            corner_radius=10)
        self.horario_combo.pack(pady=5)
        
        # Frame de informações adicionais
        info_frame = ctk.CTkFrame(frame, fg_color=(cores["bg"], cores["fg"]), corner_radius=15)
        info_frame.pack(fill="x", padx=50, pady=20)
        
        ctk.CTkLabel(info_frame, 
                     text="ℹ️ Informações Importantes:", 
                     font=("Segoe UI", 16, "bold"),
                     text_color=(cores["titulo"], cores["titulo"])).pack(pady=10)
        
        info_texto = ("• Chegue com 15 minutos de antecedência\n"
                     "• Traga documentos pessoais e cartão do convênio\n"
                     "• Em caso de desistência, cancele com 24h de antecedência\n"
                     "• Para remarcar, acesse o histórico de consultas")
        
        ctk.CTkLabel(info_frame, 
                     text=info_texto, 
                     font=("Segoe UI", 14),
                     text_color=(cores["texto"], cores["texto"]),
                     justify="left").pack(padx=20, pady=10)
        
        # Frame de ações
        acoes_frame = ctk.CTkFrame(frame, fg_color="transparent")
        acoes_frame.pack(fill="x", padx=50, pady=20)
        
        # Botão de Agendamento
        agendar_btn = ctk.CTkButton(acoes_frame, 
                                  text="✅ Agendar Consulta", 
                                  fg_color=cores["botao"], 
                                  hover_color=cores["botao_hover"],
                                  font=("Segoe UI", 14, "bold"), 
                                  width=200,
                                  height=45,
                                  corner_radius=10, 
                                  command=self.agendar_consulta)
        agendar_btn.pack(side="left", padx=10)
        
        # Botão de Limpar
        limpar_btn = ctk.CTkButton(acoes_frame, 
                                  text="🔄 Limpar Campos", 
                                  fg_color="#4b5563", 
                                  hover_color="#374151",
                                  font=("Segoe UI", 14, "bold"), 
                                  width=200,
                                  height=45,
                                  corner_radius=10, 
                                  command=self.limpar_campos_agendamento)
        limpar_btn.pack(side="left", padx=10)
        
        # Botão de Áudio
        audio_btn = ctk.CTkButton(acoes_frame, 
                                text="🔊 Ouvir Instruções", 
                                fg_color=cores["botao"], 
                                hover_color=cores["botao_hover"],
                                font=("Segoe UI", 14, "bold"), 
                                width=200,
                                height=45,
                                corner_radius=10, 
                                command=lambda: falar_texto("Tela de Agendamento de Consultas. Preencha seu nome, escolha a especialidade, selecione o médico, data e horário desejados. Clique em Agendar Consulta para confirmar."))
        audio_btn.pack(side="right", padx=10)
        
        # Mensagem de status
        self.mensagem_label = ctk.CTkLabel(frame, 
                                         text="", 
                                         font=("Segoe UI", 13), 
                                         text_color=(cores["texto"], cores["texto"]))
        self.mensagem_label.pack(pady=10)
        
        return frame
        
    def limpar_campos_agendamento(self):
        self.nome_entry.delete(0, "end")
        self.especialidade_combo.set("")
        self.medico_combo.set("")
        self.data_entry.delete(0, "end")
        self.horario_combo.set("")
        self.mensagem_label.configure(text="")
    def atualizar_medicos(self, especialidade):
        medicos_especialidade = [m['nome'] for m in MEDICOS if m['especialidade'] == especialidade]
        self.medico_combo.configure(values=medicos_especialidade)
        if medicos_especialidade:
            self.medico_combo.set(medicos_especialidade[0])
            self.atualizar_horarios(medicos_especialidade[0])
        else:
            self.medico_combo.set("")
            self.horario_combo.configure(values=[])
            
    def atualizar_horarios(self, medico):
        medico_selecionado = next((m for m in MEDICOS if m['nome'] == medico), None)
        if medico_selecionado:
            self.horario_combo.configure(values=medico_selecionado['horarios'])
            if medico_selecionado['horarios']:
                self.horario_combo.set(medico_selecionado['horarios'][0])
        else:
            self.horario_combo.configure(values=[])
            
    def agendar_consulta(self):
        nome = self.nome_entry.get().strip()
        especialidade = self.especialidade_combo.get().strip()
        medico = self.medico_combo.get().strip()
        data = self.data_entry.get().strip()
        hora = self.horario_combo.get().strip()
        
        if not nome or not especialidade or not medico or not data or not hora:
            self.mensagem_label.configure(text="Por favor, preencha todos os campos!")
            return
            
        try:
            datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            self.mensagem_label.configure(text="Data inválida! Use DD/MM/AAAA.")
            return
            
        agendado_em = datetime.now().strftime("%d/%m/%Y %H:%M")
        consulta = {
            "paciente": nome,
            "especialidade": especialidade,
            "medico": medico,
            "data": data,
            "hora": hora,
            "agendado_em": agendado_em
        }
        
        CONSULTAS.append(consulta)
        self.mensagem_label.configure(text="Consulta agendada com sucesso!")
        
        # Limpar campos
        self.nome_entry.delete(0, "end")
        self.data_entry.delete(0, "end")
        
        # Atualizar telas
        if "home" in self.telas:
            self.telas["home"].destroy()
            self.telas["home"] = self.criar_home()
        if "historico" in self.telas:
            self.telas["historico"].destroy()
            self.telas["historico"] = self.criar_historico()
    def criar_historico(self):
        cores = self.get_cores_tema()
        frame = ctk.CTkFrame(self.container, fg_color=(cores["bg"], cores["fg"]), corner_radius=20)
        
        # Cabeçalho com gradiente
        header_frame = ctk.CTkFrame(frame, fg_color=(cores["bg"], cores["fg"]))
        header_frame.pack(fill="x", padx=30, pady=30)
        
        titulo = ctk.CTkLabel(header_frame, 
                             text="Histórico de Consultas", 
                             font=("Segoe UI", 26, "bold"), 
                             text_color=(cores["titulo"], cores["titulo"]))
        titulo.pack(pady=10)
        
        subtitulo = ctk.CTkLabel(header_frame, 
                                text="Acompanhe todas as suas consultas agendadas", 
                                font=("Segoe UI", 16), 
                                text_color=(cores["subtitulo"], cores["subtitulo"]))
        subtitulo.pack(pady=5)
        
        # Separador
        ctk.CTkFrame(frame, height=2, fg_color=("#e5e7eb", "#374151")).pack(fill="x", padx=50, pady=20)
        
        # Frame de filtros
        filtros_frame = ctk.CTkFrame(frame, fg_color="transparent")
        filtros_frame.pack(fill="x", padx=50, pady=10)
        
        # Filtro por paciente
        paciente_label = ctk.CTkLabel(filtros_frame, 
                                    text="Buscar por paciente:", 
                                    font=("Segoe UI", 14, "bold"),
                                    text_color=(cores["texto"], cores["texto"]))
        paciente_label.pack(side="left", padx=10)
        
        self.filtro_paciente = ctk.CTkEntry(filtros_frame, 
                                           width=200, 
                                           height=35,
                                           corner_radius=10,
                                           placeholder_text="Digite o nome do paciente")
        self.filtro_paciente.pack(side="left", padx=10)
        self.filtro_paciente.bind("<KeyRelease>", lambda e: self.atualizar_historico(tabela))
        
        # Filtro por especialidade
        especialidade_label = ctk.CTkLabel(filtros_frame, 
                                         text="Filtrar por especialidade:", 
                                         font=("Segoe UI", 14, "bold"),
                                         text_color=(cores["texto"], cores["texto"]))
        especialidade_label.pack(side="left", padx=10)
        
        self.filtro_especialidade = ctk.CTkComboBox(filtros_frame, 
                                                   values=["Todas"] + [e["nome"] for e in ESPECIALIDADES], 
                                                   width=200, 
                                                   height=35,
                                                   corner_radius=10,
                                                   command=lambda e: self.atualizar_historico(tabela))
        self.filtro_especialidade.pack(side="left", padx=10)
        self.filtro_especialidade.set("Todas")
        
        # Frame da tabela
        tabela_frame = ctk.CTkFrame(frame, fg_color="transparent")
        tabela_frame.pack(fill="both", expand=True, padx=50, pady=20)
        
        # Configurar estilo da tabela
        style = ttk.Style()
        style.configure("Treeview", 
                       background=cores["bg"],
                       foreground=cores["texto"],
                       fieldbackground=cores["bg"],
                       rowheight=40)
        style.configure("Treeview.Heading",
                       background=cores["bg"],
                       foreground=cores["titulo"],
                       font=("Segoe UI", 12, "bold"))
        style.map("Treeview",
                 background=[("selected", cores["botao"])],
                 foreground=[("selected", "#ffffff")])
        
        # Criar tabela
        colunas = ("Paciente", "Especialidade", "Médico", "Data", "Hora", "Agendado em")
        tabela = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=10)
        
        # Configurar colunas
        for col in colunas:
            tabela.heading(col, text=col)
            tabela.column(col, width=140, anchor="center")
        
        # Adicionar scrollbar
        scrollbar = ttk.Scrollbar(tabela_frame, orient="vertical", command=tabela.yview)
        tabela.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar elementos
        tabela.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Preencher tabela
        self.atualizar_historico(tabela)
        
        # Frame de ações
        acoes_frame = ctk.CTkFrame(frame, fg_color="transparent")
        acoes_frame.pack(fill="x", padx=50, pady=20)
        
        # Botão de exportar
        ctk.CTkButton(acoes_frame, 
                      text="📤 Exportar PDF", 
                      fg_color=cores["botao"], 
                      hover_color=cores["botao_hover"],
                      width=200, 
                      height=40,
                      corner_radius=10,
                      command=lambda: exportar_historico_pdf(CONSULTAS)).pack(side="left", padx=10)
        
        # Botão de limpar filtros
        ctk.CTkButton(acoes_frame, 
                      text="🔄 Limpar Filtros", 
                      fg_color=cores["botao"], 
                      hover_color=cores["botao_hover"],
                      width=200, 
                      height=40,
                      corner_radius=10,
                      command=lambda: self.limpar_filtros_historico(tabela)).pack(side="left", padx=10)
        
        return frame
        
    def atualizar_historico(self, tabela):
        filtro_paciente = self.filtro_paciente.get().lower() if hasattr(self, 'filtro_paciente') else ""
        filtro_especialidade = self.filtro_especialidade.get() if hasattr(self, 'filtro_especialidade') else "Todas"
        
        for i in tabela.get_children():
            tabela.delete(i)
            
        for c in CONSULTAS:
            if (filtro_paciente in c['paciente'].lower() and 
                (filtro_especialidade == "Todas" or filtro_especialidade == c['especialidade'])):
                tabela.insert("", "end", values=(
                    c['paciente'],
                    c['especialidade'],
                    c['medico'],
                    c['data'],
                    c['hora'],
                    c['agendado_em']
                ))
                
    def limpar_filtros_historico(self, tabela):
        if hasattr(self, 'filtro_paciente'):
            self.filtro_paciente.delete(0, "end")
        if hasattr(self, 'filtro_especialidade'):
            self.filtro_especialidade.set("Todas")
        self.atualizar_historico(tabela)
    def criar_medicos(self):
        cores = self.get_cores_tema()
        frame = ctk.CTkFrame(self.container, fg_color=(cores["bg"], cores["fg"]), corner_radius=20)
        
        # Cabeçalho com gradiente
        header_frame = ctk.CTkFrame(frame, fg_color=(cores["bg"], cores["fg"]))
        header_frame.pack(fill="x", padx=30, pady=30)
        
        titulo = ctk.CTkLabel(header_frame, 
                             text="Nossa Equipe Médica", 
                             font=("Segoe UI", 26, "bold"), 
                             text_color=(cores["titulo"], cores["titulo"]))
        titulo.pack(pady=10)
        
        subtitulo = ctk.CTkLabel(header_frame, 
                                text="Conheça nossos profissionais de saúde", 
                                font=("Segoe UI", 16), 
                                text_color=(cores["subtitulo"], cores["subtitulo"]))
        subtitulo.pack(pady=5)
        
        # Separador
        ctk.CTkFrame(frame, height=2, fg_color=("#e5e7eb", "#374151")).pack(fill="x", padx=50, pady=20)
        
        # Frame de filtros
        filtros_frame = ctk.CTkFrame(frame, fg_color="transparent")
        filtros_frame.pack(fill="x", padx=50, pady=10)
        
        # Filtro por especialidade
        especialidade_label = ctk.CTkLabel(filtros_frame, 
                                         text="Filtrar por especialidade:", 
                                         font=("Segoe UI", 14, "bold"),
                                         text_color=(cores["texto"], cores["texto"]))
        especialidade_label.pack(side="left", padx=10)
        
        self.filtro_especialidade = ctk.CTkComboBox(filtros_frame, 
                                                   values=["Todas"] + [e["nome"] for e in ESPECIALIDADES], 
                                                   width=200, 
                                                   height=35,
                                                   corner_radius=10,
                                                   command=self.atualizar_lista_medicos)
        self.filtro_especialidade.pack(side="left", padx=10)
        self.filtro_especialidade.set("Todas")
        
        # Frame para os cards dos médicos
        cards_frame = ctk.CTkScrollableFrame(frame, fg_color="transparent", orientation="horizontal")
        cards_frame.pack(fill="both", expand=True, padx=50, pady=20)
        
        # Criar cards para cada médico
        self.cards_medicos = []
        for medico in MEDICOS:
            especialidade = next((e for e in ESPECIALIDADES if e["nome"] == medico["especialidade"]), None)
            if especialidade:
                card = self.criar_card_medico(cards_frame, medico, especialidade, cores)
                self.cards_medicos.append(card)
        
        return frame
        
    def criar_card_medico(self, parent, medico, especialidade, cores):
        card = ctk.CTkFrame(parent, 
                           fg_color=(cores["bg"], cores["fg"]), 
                           corner_radius=15,
                           width=300,
                           height=400)
        
        # Ícone da especialidade
        ctk.CTkLabel(card, 
                     text=especialidade["icone"], 
                     font=("Segoe UI", 48)).pack(pady=(20, 10))
        
        # Nome do médico
        ctk.CTkLabel(card, 
                     text=medico["nome"], 
                     font=("Segoe UI", 18, "bold"),
                     text_color=(cores["titulo"], cores["titulo"])).pack(pady=5)
        
        # Especialidade
        ctk.CTkLabel(card, 
                     text=medico["especialidade"], 
                     font=("Segoe UI", 14),
                     text_color=(cores["subtitulo"], cores["subtitulo"])).pack(pady=5)
        
        # CRM
        ctk.CTkLabel(card, 
                     text=f"CRM: {medico['crm']}", 
                     font=("Segoe UI", 12),
                     text_color=(cores["texto"], cores["texto"])).pack(pady=5)
        
        # Horários disponíveis
        horarios_frame = ctk.CTkFrame(card, fg_color="transparent")
        horarios_frame.pack(pady=10)
        
        ctk.CTkLabel(horarios_frame, 
                     text="Horários Disponíveis:", 
                     font=("Segoe UI", 12, "bold"),
                     text_color=(cores["texto"], cores["texto"])).pack()
        
        for hora in medico["horarios"]:
            ctk.CTkLabel(horarios_frame, 
                        text=hora, 
                        font=("Segoe UI", 12),
                        text_color=(cores["texto"], cores["texto"])).pack()
        
        # Botão de agendamento
        ctk.CTkButton(card, 
                      text="Agendar Consulta", 
                      fg_color=cores["botao"], 
                      hover_color=cores["botao_hover"],
                      width=200, 
                      height=35,
                      corner_radius=10,
                      command=lambda: self.ir_agendar_medico(medico)).pack(pady=20)
        
        card.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        return card
        
    def atualizar_lista_medicos(self, especialidade):
        for card in self.cards_medicos:
            if especialidade == "Todas":
                card.pack(side="left", padx=10, pady=10, fill="both", expand=True)
            else:
                medico = next((m for m in MEDICOS if m["nome"] == card.winfo_children()[1].cget("text")), None)
                if medico and medico["especialidade"] == especialidade:
                    card.pack(side="left", padx=10, pady=10, fill="both", expand=True)
                else:
                    card.pack_forget()
                    
    def ir_agendar_medico(self, medico):
        self.mudar_tela("agendar")
        if hasattr(self, 'especialidade_combo'):
            self.especialidade_combo.set(medico["especialidade"])
            self.atualizar_medicos(medico["especialidade"])
            self.medico_combo.set(medico["nome"])
            self.atualizar_horarios(medico["nome"])
    def criar_configuracoes(self):
        cores = self.get_cores_tema()
        frame = ctk.CTkFrame(self.container, fg_color=(cores["bg"], cores["fg"]), corner_radius=20)
        
        # Cabeçalho com gradiente
        header_frame = ctk.CTkFrame(frame, fg_color=(cores["bg"], cores["fg"]))
        header_frame.pack(fill="x", padx=30, pady=30)
        
        titulo = ctk.CTkLabel(header_frame, 
                             text="Configurações", 
                             font=("Segoe UI", 26, "bold"), 
                             text_color=(cores["titulo"], cores["titulo"]))
        titulo.pack(pady=10)
        
        subtitulo = ctk.CTkLabel(header_frame, 
                                text="Personalize sua experiência no sistema", 
                                font=("Segoe UI", 16), 
                                text_color=(cores["subtitulo"], cores["subtitulo"]))
        subtitulo.pack(pady=5)
        
        # Separador
        ctk.CTkFrame(frame, height=2, fg_color=("#e5e7eb", "#374151")).pack(fill="x", padx=50, pady=20)
        
        # Frame das configurações
        config_frame = ctk.CTkFrame(frame, fg_color="transparent")
        config_frame.pack(fill="both", expand=True, padx=50, pady=20)
        
        # Aparência
        aparencia_frame = ctk.CTkFrame(config_frame, fg_color=(cores["bg"], cores["fg"]), corner_radius=15)
        aparencia_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(aparencia_frame, 
                     text="🎨 Aparência", 
                     font=("Segoe UI", 18, "bold"),
                     text_color=(cores["titulo"], cores["titulo"])).pack(pady=10)
        
        # Tema
        tema_frame = ctk.CTkFrame(aparencia_frame, fg_color="transparent")
        tema_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(tema_frame, 
                     text="Tema do Aplicativo:", 
                     font=("Segoe UI", 14, "bold"),
                     text_color=(cores["texto"], cores["texto"])).pack(side="left", padx=10)
        
        tema_combo = ctk.CTkComboBox(tema_frame, 
                                    values=["Claro", "Escuro"], 
                                    width=200, 
                                    height=35,
                                    corner_radius=10)
        tema_combo.set(self.tema_atual)
        tema_combo.pack(side="left", padx=10)
        tema_combo.bind("<<ComboboxSelected>>", lambda e: self.trocar_tema(tema_combo.get()))
        
        # Tamanho da fonte
        fonte_frame = ctk.CTkFrame(aparencia_frame, fg_color="transparent")
        fonte_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(fonte_frame, 
                     text="Tamanho da Fonte:", 
                     font=("Segoe UI", 14, "bold"),
                     text_color=(cores["texto"], cores["texto"])).pack(side="left", padx=10)
        
        fonte_combo = ctk.CTkComboBox(fonte_frame, 
                                     values=["Pequeno", "Médio", "Grande"], 
                                     width=200, 
                                     height=35,
                                     corner_radius=10)
        fonte_combo.set("Médio")
        fonte_combo.pack(side="left", padx=10)
        
        # Notificações
        notificacoes_frame = ctk.CTkFrame(config_frame, fg_color=(cores["bg"], cores["fg"]), corner_radius=15)
        notificacoes_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(notificacoes_frame, 
                     text="🔔 Notificações", 
                     font=("Segoe UI", 18, "bold"),
                     text_color=(cores["titulo"], cores["titulo"])).pack(pady=10)
        
        # Opções de notificação
        opcoes_frame = ctk.CTkFrame(notificacoes_frame, fg_color="transparent")
        opcoes_frame.pack(fill="x", padx=20, pady=10)
        
        # Notificações de consulta
        consulta_frame = ctk.CTkFrame(opcoes_frame, fg_color="transparent")
        consulta_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(consulta_frame, 
                     text="Notificações de Consulta:", 
                     font=("Segoe UI", 14, "bold"),
                     text_color=(cores["texto"], cores["texto"])).pack(side="left", padx=10)
        
        ctk.CTkSwitch(consulta_frame, 
                      text="Ativar", 
                      width=100).pack(side="right", padx=10)
        
        # Notificações de sistema
        sistema_frame = ctk.CTkFrame(opcoes_frame, fg_color="transparent")
        sistema_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(sistema_frame, 
                     text="Notificações do Sistema:", 
                     font=("Segoe UI", 14, "bold"),
                     text_color=(cores["texto"], cores["texto"])).pack(side="left", padx=10)
        
        ctk.CTkSwitch(sistema_frame, 
                      text="Ativar", 
                      width=100).pack(side="right", padx=10)
        
        # Acessibilidade
        acessibilidade_frame = ctk.CTkFrame(config_frame, fg_color=(cores["bg"], cores["fg"]), corner_radius=15)
        acessibilidade_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(acessibilidade_frame, 
                     text="♿ Acessibilidade", 
                     font=("Segoe UI", 18, "bold"),
                     text_color=(cores["titulo"], cores["titulo"])).pack(pady=10)
        
        # Opções de acessibilidade
        acess_opcoes_frame = ctk.CTkFrame(acessibilidade_frame, fg_color="transparent")
        acess_opcoes_frame.pack(fill="x", padx=20, pady=10)
        
        # Descrição em áudio
        audio_frame = ctk.CTkFrame(acess_opcoes_frame, fg_color="transparent")
        audio_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(audio_frame, 
                     text="Descrição em Áudio:", 
                     font=("Segoe UI", 14, "bold"),
                     text_color=(cores["texto"], cores["texto"])).pack(side="left", padx=10)
        
        ctk.CTkSwitch(audio_frame, 
                      text="Ativar", 
                      width=100).pack(side="right", padx=10)
        
        # Alto contraste
        contraste_frame = ctk.CTkFrame(acess_opcoes_frame, fg_color="transparent")
        contraste_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(contraste_frame, 
                     text="Alto Contraste:", 
                     font=("Segoe UI", 14, "bold"),
                     text_color=(cores["texto"], cores["texto"])).pack(side="left", padx=10)
        
        ctk.CTkSwitch(contraste_frame, 
                      text="Ativar", 
                      width=100).pack(side="right", padx=10)
        
        # Frame de ações
        acoes_frame = ctk.CTkFrame(frame, fg_color="transparent")
        acoes_frame.pack(fill="x", padx=50, pady=20)
        
        # Botão de salvar
        ctk.CTkButton(acoes_frame, 
                      text="💾 Salvar Configurações", 
                      fg_color=cores["botao"], 
                      hover_color=cores["botao_hover"],
                      width=200, 
                      height=40,
                      corner_radius=10).pack(side="left", padx=10)
        
        # Botão de restaurar padrão
        ctk.CTkButton(acoes_frame, 
                      text="🔄 Restaurar Padrão", 
                      fg_color="#ef4444", 
                      hover_color="#dc2626",
                      width=200, 
                      height=40,
                      corner_radius=10).pack(side="right", padx=10)
        
        return frame
    def trocar_tema(self, tema):
        if tema == "Claro":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")
        self.tema_atual = tema
        
        # Recria todas as telas para aplicar o novo tema
        for tela in self.telas.values():
            tela.destroy()
        self.telas = {}
        
        # Recria o menu lateral
        self.menu.destroy()
        self.menu = MenuLateral(self, self.mudar_tela)
        self.menu.pack(side="left", fill="y")
        
        # Atualiza o container principal
        cores = self.get_cores_tema()
        self.container.configure(fg_color=(cores["bg"], cores["fg"]))
        
        # Recria a tela atual
        self.mudar_tela(self.tela_atual)
    def get_cores_tema(self):
        """Retorna as cores baseadas no tema atual"""
        if self.tema_atual == "Claro":
            return {
                "bg": "#eaf0fa",
                "fg": "#181a20",
                "titulo": "#1e40af",
                "subtitulo": "#2563eb",
                "texto": "#1e40af",
                "botao": "#2563eb",
                "botao_hover": "#1e40af"
            }
        else:
            return {
                "bg": "#181a20",
                "fg": "#eaf0fa",
                "titulo": "#93c5fd",
                "subtitulo": "#60a5fa",
                "texto": "#93c5fd",
                "botao": "#2563eb",
                "botao_hover": "#1e40af"
            }
    def criar_sobre(self):
        cores = self.get_cores_tema()
        frame = ctk.CTkFrame(self.container, fg_color=(cores["bg"], cores["fg"]), corner_radius=20)
        
        titulo = ctk.CTkLabel(frame, text="Sobre o Sistema", 
                             font=("Segoe UI", 22, "bold"), 
                             text_color=(cores["titulo"], cores["titulo"]))
        titulo.pack(pady=20)
        
        texto = ("O Hospital das Clínicas oferece atendimento de excelência com tecnologia de ponta.\n"
                 "Este sistema faz parte do programa Saúde Digital, promovendo acessibilidade e inovação.\n"
                 "Acesse nossas redes sociais:")
        
        ctk.CTkLabel(frame, text=texto, 
                     font=("Segoe UI", 15), 
                     text_color=(cores["texto"], cores["texto"]), 
                     justify="left").pack(pady=10)
        
        redes = ctk.CTkFrame(frame, fg_color=(cores["bg"], cores["fg"]))
        redes.pack(pady=5)
        
        ctk.CTkButton(redes, text="Facebook", 
                     fg_color=cores["botao"], 
                     hover_color=cores["botao_hover"],
                     width=120, 
                     command=lambda: webbrowser.open("https://www.facebook.com/hospitaldasclinicasdafmusp"), 
                     corner_radius=10).pack(side="left", padx=5)
        
        ctk.CTkButton(redes, text="Instagram", 
                     fg_color=cores["botao"], 
                     hover_color=cores["botao_hover"],
                     width=120, 
                     command=lambda: webbrowser.open("https://www.instagram.com/hospitalhcfmusp/"), 
                     corner_radius=10).pack(side="left", padx=5)
        
        ctk.CTkButton(redes, text="Site Oficial", 
                     fg_color=cores["botao"], 
                     hover_color=cores["botao_hover"],
                     width=120, 
                     command=lambda: webbrowser.open("https://www.hc.fm.usp.br/"), 
                     corner_radius=10).pack(side="left", padx=5)
        
        ctk.CTkButton(frame, text="Descrição em Áudio", 
                     fg_color=cores["botao"], 
                     hover_color=cores["botao_hover"],
                     command=lambda: falar_texto(texto), 
                     corner_radius=10).pack(pady=10)
        
        return frame
    def criar_ajuda(self):
        cores = self.get_cores_tema()
        frame = ctk.CTkFrame(self.container, fg_color=(cores["bg"], cores["fg"]), corner_radius=20)
        
        # Cabeçalho com gradiente
        header_frame = ctk.CTkFrame(frame, fg_color=(cores["bg"], cores["fg"]))
        header_frame.pack(fill="x", padx=30, pady=30)
        
        titulo = ctk.CTkLabel(header_frame, 
                             text="Ajuda e Suporte", 
                             font=("Segoe UI", 26, "bold"), 
                             text_color=(cores["titulo"], cores["titulo"]))
        titulo.pack(pady=10)
        
        subtitulo = ctk.CTkLabel(header_frame, 
                                text="Encontre respostas para suas dúvidas", 
                                font=("Segoe UI", 16), 
                                text_color=(cores["subtitulo"], cores["subtitulo"]))
        subtitulo.pack(pady=5)
        
        # Separador
        ctk.CTkFrame(frame, height=2, fg_color=("#e5e7eb", "#374151")).pack(fill="x", padx=50, pady=20)
        
        # Frame de conteúdo
        conteudo_frame = ctk.CTkFrame(frame, fg_color="transparent")
        conteudo_frame.pack(fill="both", expand=True, padx=50, pady=20)
        
        # Seção de dúvidas frequentes
        faq_frame = ctk.CTkFrame(conteudo_frame, fg_color=(cores["bg"], cores["fg"]), corner_radius=15)
        faq_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(faq_frame, 
                     text="❓ Dúvidas Frequentes", 
                     font=("Segoe UI", 18, "bold"),
                     text_color=(cores["titulo"], cores["titulo"])).pack(pady=10)
        
        # Lista de dúvidas frequentes
        duvidas = [
            {
                "pergunta": "Como agendar uma consulta?",
                "resposta": "Para agendar uma consulta, acesse a tela 'Agendar Consulta' no menu lateral, preencha os dados solicitados e clique em 'Agendar Consulta'."
            },
            {
                "pergunta": "Como cancelar uma consulta?",
                "resposta": "Para cancelar uma consulta, acesse o 'Histórico de Consultas', localize a consulta desejada e clique no botão 'Cancelar'."
            },
            {
                "pergunta": "Como alterar o tema do sistema?",
                "resposta": "Para alterar o tema, acesse 'Configurações' no menu lateral e selecione o tema desejado (Claro ou Escuro)."
            },
            {
                "pergunta": "Como exportar o histórico de consultas?",
                "resposta": "Para exportar o histórico, acesse 'Histórico de Consultas' e clique no botão 'Exportar PDF'."
            }
        ]
        
        for duvida in duvidas:
            card = ctk.CTkFrame(faq_frame, fg_color="transparent")
            card.pack(fill="x", padx=20, pady=10)
            
            ctk.CTkLabel(card, 
                        text=duvida["pergunta"], 
                        font=("Segoe UI", 14, "bold"),
                        text_color=(cores["titulo"], cores["titulo"])).pack(anchor="w", pady=5)
            
            ctk.CTkLabel(card, 
                        text=duvida["resposta"], 
                        font=("Segoe UI", 13),
                        text_color=(cores["texto"], cores["texto"]),
                        wraplength=600,
                        justify="left").pack(anchor="w", pady=5)
            
            ctk.CTkFrame(card, height=1, fg_color=("#e5e7eb", "#374151")).pack(fill="x", pady=10)
        
        # Seção de contato
        contato_frame = ctk.CTkFrame(conteudo_frame, fg_color=(cores["bg"], cores["fg"]), corner_radius=15)
        contato_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(contato_frame, 
                     text="📞 Contato", 
                     font=("Segoe UI", 18, "bold"),
                     text_color=(cores["titulo"], cores["titulo"])).pack(pady=10)
        
        # Informações de contato
        contato_info = ctk.CTkFrame(contato_frame, fg_color="transparent")
        contato_info.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(contato_info, 
                     text="Precisa de ajuda adicional? Entre em contato conosco:", 
                     font=("Segoe UI", 14),
                     text_color=(cores["texto"], cores["texto"])).pack(pady=5)
        
        ctk.CTkLabel(contato_info, 
                     text="📧 E-mail: suporte@hc.br", 
                     font=("Segoe UI", 14),
                     text_color=(cores["texto"], cores["texto"])).pack(pady=5)
        
        ctk.CTkLabel(contato_info, 
                     text="📞 Telefone: (11) 1234-5678", 
                     font=("Segoe UI", 14),
                     text_color=(cores["texto"], cores["texto"])).pack(pady=5)
        
        ctk.CTkLabel(contato_info, 
                     text="⏰ Horário de Atendimento: Segunda a Sexta, das 8h às 18h", 
                     font=("Segoe UI", 14),
                     text_color=(cores["texto"], cores["texto"])).pack(pady=5)
        
        # Frame de ações
        acoes_frame = ctk.CTkFrame(frame, fg_color="transparent")
        acoes_frame.pack(fill="x", padx=50, pady=20)
        
        # Botão de acessar site
        ctk.CTkButton(acoes_frame, 
                      text="🌐 Acessar Site", 
                      fg_color=cores["botao"], 
                      hover_color=cores["botao_hover"],
                      width=200, 
                      height=40,
                      corner_radius=10,
                      command=lambda: webbrowser.open("https://www.hc.fm.usp.br/")).pack(side="left", padx=10)
        
        # Botão de enviar e-mail
        ctk.CTkButton(acoes_frame, 
                      text="📧 Enviar E-mail", 
                      fg_color=cores["botao"], 
                      hover_color=cores["botao_hover"],
                      width=200, 
                      height=40,
                      corner_radius=10,
                      command=lambda: webbrowser.open("mailto:suporte@hc.br")).pack(side="left", padx=10)
        
        # Botão de ligar
        ctk.CTkButton(acoes_frame, 
                      text="📞 Ligar", 
                      fg_color=cores["botao"], 
                      hover_color=cores["botao_hover"],
                      width=200, 
                      height=40,
                      corner_radius=10,
                      command=lambda: webbrowser.open("tel:+551112345678")).pack(side="right", padx=10)
        
        return frame
    def criar_notificacoes(self):
        cores = self.get_cores_tema()
        frame = ctk.CTkFrame(self.container, fg_color=(cores["bg"], cores["fg"]), corner_radius=20)
        
        # Cabeçalho com gradiente
        header_frame = ctk.CTkFrame(frame, fg_color=(cores["bg"], cores["fg"]))
        header_frame.pack(fill="x", padx=30, pady=30)
        
        titulo = ctk.CTkLabel(header_frame, 
                             text="Notificações", 
                             font=("Segoe UI", 26, "bold"), 
                             text_color=(cores["titulo"], cores["titulo"]))
        titulo.pack(pady=10)
        
        subtitulo = ctk.CTkLabel(header_frame, 
                                text="Fique por dentro das últimas atualizações", 
                                font=("Segoe UI", 16), 
                                text_color=(cores["subtitulo"], cores["subtitulo"]))
        subtitulo.pack(pady=5)
        
        # Separador
        ctk.CTkFrame(frame, height=2, fg_color=("#e5e7eb", "#374151")).pack(fill="x", padx=50, pady=20)
        
        # Frame das notificações
        notificacoes_frame = ctk.CTkFrame(frame, fg_color="transparent")
        notificacoes_frame.pack(fill="both", expand=True, padx=50, pady=20)
        
        # Criar cards para cada notificação
        for i, notificacao in enumerate(NOTIFICACOES):
            card = ctk.CTkFrame(notificacoes_frame, 
                              fg_color=(cores["bg"], cores["fg"]), 
                              corner_radius=15)
            card.pack(fill="x", pady=10)
            
            # Ícone e título
            header = ctk.CTkFrame(card, fg_color="transparent")
            header.pack(fill="x", padx=20, pady=10)
            
            ctk.CTkLabel(header, 
                        text="🔔", 
                        font=("Segoe UI", 24)).pack(side="left", padx=10)
            
            ctk.CTkLabel(header, 
                        text=f"Notificação {i+1}", 
                        font=("Segoe UI", 16, "bold"),
                        text_color=(cores["titulo"], cores["titulo"])).pack(side="left", padx=10)
            
            # Data e hora
            ctk.CTkLabel(header, 
                        text=datetime.now().strftime("%d/%m/%Y %H:%M"), 
                        font=("Segoe UI", 12),
                        text_color=(cores["subtitulo"], cores["subtitulo"])).pack(side="right", padx=10)
            
            # Separador
            ctk.CTkFrame(card, height=1, fg_color=("#e5e7eb", "#374151")).pack(fill="x", padx=20)
            
            # Mensagem
            ctk.CTkLabel(card, 
                        text=notificacao, 
                        font=("Segoe UI", 14),
                        text_color=(cores["texto"], cores["texto"]),
                        wraplength=600,
                        justify="left").pack(padx=20, pady=15)
            
            # Botões de ação
            botoes_frame = ctk.CTkFrame(card, fg_color="transparent")
            botoes_frame.pack(fill="x", padx=20, pady=10)
            
            ctk.CTkButton(botoes_frame, 
                         text="🔊 Ouvir", 
                         fg_color=cores["botao"], 
                         hover_color=cores["botao_hover"],
                         width=120, 
                         height=35,
                         corner_radius=10,
                         command=lambda t=notificacao: falar_texto(t)).pack(side="left", padx=5)
            
            ctk.CTkButton(botoes_frame, 
                         text="📌 Fixar", 
                         fg_color=cores["botao"], 
                         hover_color=cores["botao_hover"],
                         width=120, 
                         height=35,
                         corner_radius=10).pack(side="left", padx=5)
            
            ctk.CTkButton(botoes_frame, 
                         text="❌ Remover", 
                         fg_color="#ef4444", 
                         hover_color="#dc2626",
                         width=120, 
                         height=35,
                         corner_radius=10).pack(side="right", padx=5)
        
        # Frame de ações
        acoes_frame = ctk.CTkFrame(frame, fg_color="transparent")
        acoes_frame.pack(fill="x", padx=50, pady=20)
        
        # Botão de marcar todas como lidas
        ctk.CTkButton(acoes_frame, 
                      text="✓ Marcar todas como lidas", 
                      fg_color=cores["botao"], 
                      hover_color=cores["botao_hover"],
                      width=200, 
                      height=40,
                      corner_radius=10).pack(side="left", padx=10)
        
        # Botão de limpar todas
        ctk.CTkButton(acoes_frame, 
                      text="🗑️ Limpar todas", 
                      fg_color="#ef4444", 
                      hover_color="#dc2626",
                      width=200, 
                      height=40,
                      corner_radius=10).pack(side="right", padx=10)
        
        return frame
    def criar_placeholder(self, texto):
        frame = ctk.CTkFrame(self.container, fg_color=("#eaf0fa", "#181a20"))
        label = ctk.CTkLabel(frame, text=texto, font=("Segoe UI", 20, "italic"), text_color=("#2563eb", "#60a5fa"))
        label.pack(expand=True)
        return frame
    def formatar_data(self, event):
        texto = self.data_entry.get().replace("/", "")  # Remove barras existentes
        novo_texto = ""
        if len(texto) > 0:
            novo_texto += texto[:2]
        if len(texto) > 2:
            novo_texto += "/" + texto[2:4]
        if len(texto) > 4:
            novo_texto += "/" + texto[4:8]
        self.data_entry.delete(0, "end")
        self.data_entry.insert(0, novo_texto)

if __name__ == "__main__":
    app = HospitalApp()
    app.mainloop()
