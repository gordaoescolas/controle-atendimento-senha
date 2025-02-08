import tkinter as tk
from tkinter import messagebox
import re
import os

# Caminho do arquivo app.py na mesma pasta deste script
APP_PATH = os.path.join(os.path.dirname(__file__), "app.py")

def get_current_port():
    """Lê a porta atual configurada no app.py"""
    try:
        with open(APP_PATH, "r", encoding="utf-8") as file:
            content = file.readlines()
        for line in content:
            match = re.search(r'port\s*=\s*(\d+)', line)
            if match:
                return match.group(1)
    except FileNotFoundError:
        messagebox.showerror("Erro", "O arquivo app.py não foi encontrado.")
    return "80"  # Valor padrão caso não encontre

def update_port():
    """Atualiza a porta dentro do app.py"""
    new_port = entry_port.get().strip()
    
    if not new_port.isdigit():
        messagebox.showerror("Erro", "A porta deve ser um número.")
        return
    
    new_port = int(new_port)
    if new_port < 1 or new_port > 65535:
        messagebox.showerror("Erro", "Escolha uma porta entre 1 e 65535.")
        return
    
    try:
        with open(APP_PATH, "r", encoding="utf-8") as file:
            content = file.readlines()
        
        with open(APP_PATH, "w", encoding="utf-8") as file:
            for line in content:
                if "port=" in line or "port =" in line:  # Substitui a linha correta
                    file.write(f'    app.run(host="0.0.0.0", port={new_port}, debug=False)\n')
                else:
                    file.write(line)
        
        messagebox.showinfo("Sucesso", f"Porta alterada para {new_port}.")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao modificar o arquivo: {e}")

# Criar a janela principal
root = tk.Tk()
root.title("Configuração de Porta")
root.geometry("300x150")

# Obter a porta atual
current_port = get_current_port()

# Criar os elementos da interface
tk.Label(root, text="Porta Atual:").pack(pady=5)
label_port = tk.Label(root, text=current_port, font=("Arial", 12, "bold"))
label_port.pack()

tk.Label(root, text="Nova Porta:").pack(pady=5)
entry_port = tk.Entry(root)
entry_port.pack()

btn_update = tk.Button(root, text="Salvar", command=update_port)
btn_update.pack(pady=10)

# Rodar a interface
root.mainloop()
