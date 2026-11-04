# ⚙️ Simulador de Autômatos (AFD e AFN)

Uma aplicação gráfica simples e intuitiva desenvolvida em Python para simular a execução de **Autômatos Finitos Determinísticos (AFD)** e **Autômatos Finitos Não-Determinísticos (AFN)** a partir de arquivos de configuração em formato JSON.

---

## 📌 Sobre o Projeto

O projeto permite que o usuário carregue a definição de um autômato via arquivo `.json`, insira uma cadeia de entrada e visualize o trajeto detalhado das transições passo a passo até o resultado final (aceitação ou rejeição da cadeia).

### 🧑‍💻 Funcionalidades
* **Suporte a AFD e AFN:** Trata transições simples (string) ou múltiplas (listas).
* **Carregamento Dinâmico:** Leitura de autômatos via interface gráfica (`filedialog`).
* **Validação de Alfabeto:** Verifica se cada símbolo da cadeia pertence ao alfabeto definido.
* **Log de Transições:** Exibe cada passo da simulação e os estados atingidos.
* **Interface Moderna:** Desenvolvida em CustomTkinter.

---

## 🛠️ Como Instalar e Executar

### 1. Instalar as Dependências
Abra o terminal ou prompt de comando na pasta do projeto e execute o comando abaixo para instalar todas as bibliotecas necessárias automaticamente a partir do `requirements.txt`:

```bash
pip install -r requirements.txt
