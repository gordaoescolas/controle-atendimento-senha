import re
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class VendorIdUpdater(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Atualizar VendorID")
        self.geometry("225x200")
        
        # Container principal
        main_frame = ttk.Frame(self, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Label e campo de entrada
        ttk.Label(main_frame, text="Novo VendorID (formato 0xXXXX):").grid(row=0, column=0, pady=10)
        self.vendor_id = tk.StringVar()
        self.entry = ttk.Entry(main_frame, textvariable=self.vendor_id)
        self.entry.grid(row=1, column=0, pady=5)

        # Botões
        ttk.Button(main_frame, text="Atualizar", command=self.update_vendor_id).grid(row=2, column=0, pady=20)
        ttk.Button(main_frame, text="Cancelar", command=self.quit).grid(row=3, column=0)

    def update_vendor_id(self):
        new_id = self.vendor_id.get()
        if not re.match(r'0x[0-9a-fA-F]+', new_id):
            messagebox.showerror("Erro", "Formato inválido. Use o formato 0xXXXX")
            return

        try:
            with open('templates/emit.html', 'r', encoding='utf-8') as file:
                content = file.read()

            pattern = r'vendorId: (0x[0-9a-fA-F]+)'
            match = re.search(pattern, content)
            
            if match:
                current_id = match.group(1)
                new_content = content.replace(f'vendorId: {current_id}', f'vendorId: {new_id}')
                
                with open('templates/emit.html', 'w', encoding='utf-8') as file:
                    file.write(new_content)
                
                messagebox.showinfo("Sucesso", f"VendorId atualizado com sucesso para {new_id}")
            else:
                messagebox.showerror("Erro", "VendorId não encontrado no arquivo")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar arquivo: {str(e)}")

if __name__ == "__main__":
    app = VendorIdUpdater()
    app.mainloop()