import json
import customtkinter as ctk
from customtkinter import filedialog

# Configuração do tema escuro da interface
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class SimuladorAutomatoApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Simulador de AFDs e AFNs")
        self.geometry("600x550")
        self.automato = None

        # --- Título ---
        self.label_titulo = ctk.CTkLabel(
            self,
            text="Simulador de Autômatos",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.label_titulo.pack(pady=15)

        # --- Seleção de Arquivo ---
        self.btn_carregar = ctk.CTkButton(
            self, text="Carregar JSON do Autômato", command=self.carregar_json
        )
        self.btn_carregar.pack(pady=5)

        self.lbl_arquivo = ctk.CTkLabel(
            self, text="Nenhum arquivo carregado", text_color="gray"
        )
        self.lbl_arquivo.pack(pady=5)

        # --- Entrada da Cadeia ---
        self.entry_cadeia = ctk.CTkEntry(
            self, placeholder_text="Digite a cadeia (ex: 0110)", width=300
        )
        self.entry_cadeia.pack(pady=15)

        # --- Botão Simular ---
        self.btn_simular = ctk.CTkButton(
            self,
            text="Simular Cadeia",
            fg_color="#2b8a3e",
            hover_color="#237032",
            command=self.executar_simulacao,
        )
        self.btn_simular.pack(pady=5)

        # --- Área de Log / Trajeto ---
        self.txt_log = ctk.CTkTextbox(self, width=540, height=250)
        self.txt_log.pack(pady=15)

    #Função para carregar o json desejado pelo usuário (abre uma tela dos arquivos e ele escolhe o exemplo)
    def carregar_json(self):
        caminho = filedialog.askopenfilename(
            filetypes=[("Arquivos JSON", "*.json")]
        )
        if caminho:
            try:
                with open(caminho, "r", encoding="utf-8") as f:
                    self.automato = json.load(f)

                self.lbl_arquivo.configure(
                    text=f"Carregado: {caminho.split('/')[-1]}",
                    text_color="#4dabf7",
                )
                self.txt_log.delete("1.0", "end")
                self.txt_log.insert("end", "=== AUTÔMATO CARREGADO ===\n")
                self.txt_log.insert(
                    "end", f"Alfabeto: {self.automato['alfabeto']}\n"
                )
                self.txt_log.insert(
                    "end", f"Estados: {self.automato['estados']}\n"
                )
                self.txt_log.insert(
                    "end",
                    f"Estado Inicial: {self.automato['estado_inicial']}\n",
                )
                self.txt_log.insert(
                    "end",
                    f"Estados Finais: {self.automato['estados_finais']}\n\n",
                )
            except Exception as e:
                self.lbl_arquivo.configure(
                    text="Erro ao ler o arquivo JSON!", text_color="red"
                )

    #Verificar se cada símbolo da cadeia pertence ao alfabeto do autômato:
    def pertence_alfabeto(self, simbolo):
        if simbolo not in self.automato['alfabeto']:
            return False
        return True

    #Função para simular o Autômato (AFD / AFN):
    def executar_simulacao(self):
        if not self.automato:
            self.txt_log.insert("end", "Por favor, carregue um arquivo JSON primeiro!\n")
            return

        #Pegando cadeia:
        cadeia = self.entry_cadeia.get().lower().strip()
        
        #Armazenando o estado atual (inicia no estado inicial):
        estados_atuais = {self.automato['estado_inicial']}
        estados_finais = set(self.automato['estados_finais'])

        self.txt_log.insert("end", "\n--------------------------------------------------\n")
        self.txt_log.insert("end", "           TRAJETO DE TRANSIÇÕES                  \n")
        self.txt_log.insert("end", "--------------------------------------------------\n")
        self.txt_log.insert("end", f"Estado Inicial: {estados_atuais}\n")

        #Iterando cada símbolo da cadeia passada:
        for i, simbolo in enumerate(cadeia, start=1):
            valido = self.pertence_alfabeto(simbolo)
            
            if not valido:
                self.txt_log.insert("end", f"\nCadeia rejeitada: simbolo '{simbolo}' não se encontra no alfabeto\n")
                self.txt_log.insert("end", "Resultado: Cadeia rejeitada!\n")
                return

            proximos_estados = set()

            #Fazendo a transição:
            # Validação da transição
            for estado in estados_atuais:
                transicoes_do_estado = self.automato["transicoes"].get(estado, {})

                if simbolo in transicoes_do_estado:
                    destinos = transicoes_do_estado[simbolo]

                    # Trata tanto AFD (string) quanto AFN (lista de destinos)
                    if isinstance(destinos, list):
                        proximos_estados.update(destinos)
                    else:
                        proximos_estados.add(destinos)

            #Inserindo mensagens de log na interface:
            self.txt_log.insert(
                "end",
                f"Passo {i} | Lendo '{simbolo}': {estados_atuais} -> {proximos_estados if proximos_estados else '∅ (Sem transição)'}\n"
            )

            estados_atuais = proximos_estados

            # Se todas as ramificações morrerem/travarem
            if not estados_atuais:
                self.txt_log.insert("end", f"\nCadeia rejeitada: sem transições válidas para o símbolo '{simbolo}'!\n")
                self.txt_log.insert("end", "Resultado: Cadeia rejeitada!\n")
                return

        self.txt_log.insert("end", "--------------------------------------------------\n")

        # Retornando se a cadeia foi aceita (se pelo menos um estado final foi atingido):
        intersecao = estados_atuais.intersection(estados_finais)
        if intersecao:
            self.txt_log.insert("end", f"Estados finais atingidos: {intersecao}\n")
            self.txt_log.insert("end", "\nResultado: Cadeia aceita! \n")
        else:
            self.txt_log.insert("end", f"Estados onde parou: {estados_atuais} (Nenhum é de aceitação)\n")
            self.txt_log.insert("end", "\nResultado: Cadeia rejeitada!\n")

        self.txt_log.see("end")

#Executando a interface + código:
if __name__ == "__main__":
    app = SimuladorAutomatoApp()
    app.mainloop()