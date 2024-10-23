import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import customtkinter
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class IDFApp:
    def __init__(self, root):
        self.root = root
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")
        customtkinter.set_window_scaling(0.9) 
        customtkinter.set_widget_scaling(0.9)
        self.root.resizable(width=False, height=False)
        self.root.title("Recomendações de Música (Similiaridade dos Cossenos)")
        self.root.geometry("700x900")
        #customtkinter.deactivate_automatic_dpi_awareness()
        self.root.configure(bg="#f0f0f0")
        #self.root.iconbitmap(r"../img/favicon.ico") # Converte .png etc para .ico / salvar como favicon.ico na pasta img 
        
        estilo_titulo = ("Arial", 14, "bold")
        estilo_normal = ("Arial", 14)

        for i in range(10):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.root.grid_columnconfigure(i, weight=1)
       
        self.label = customtkinter.CTkLabel(root, text="Escoha o Arquivo CSV:", font=estilo_titulo)
        self.label.grid(row=0, column=0, columnspan=2, pady=10, padx=20, sticky='w')
        
        self.btn_upload = customtkinter.CTkButton(root, text="Escolher", font=estilo_normal, command=self.upload_file_text)
        self.btn_upload.grid(row=1, column=0, columnspan=2, pady=10, padx=150, sticky="nsew") 
        
        self.lbl_colunas = customtkinter.CTkLabel(root, text="Selecione a Coluna:", font=estilo_titulo)
        self.lbl_colunas.grid(row=2, column=0, pady=10, padx=20, sticky='w')
        
        self.lbx_colunas = tk.Listbox(root, selectmode=tk.SINGLE, width=40, height=8, font=estilo_normal, bd=2, relief='solid')
        self.lbx_colunas.grid(row=3, column=0, columnspan=2, pady=10, padx=50, sticky="nsew")
        
        self.lbl_amostra = customtkinter.CTkLabel(root, text="Insira a Amostra:", font=estilo_titulo)
        self.lbl_amostra.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky='w')
        
        self.txt_amostra = tk.Text(root, height=5, width=40, font=estilo_normal, bd=2, relief="solid")
        self.txt_amostra.grid(row=5, column=0, columnspan=2, pady=10, padx=20, sticky="nsew")

        self.btn_calcIDF = customtkinter.CTkButton(root, text="Calcular", font=estilo_normal, command=self.calcular_similiaridade_cosseno_text)
        self.btn_calcIDF.grid(row=6, column=0, columnspan=2, pady=20, padx=150, sticky="nsew")
        
        self.lbl_resultado = customtkinter.CTkLabel(root, text="Resultado:", font=estilo_titulo)
        self.lbl_resultado.grid(row=7, column=0, columnspan=2, padx=20, sticky='w')
        
        self.txt_resultado = tk.Text(root, height=8, width=60, font=estilo_normal, bd=2, relief='solid', state="disabled")
        self.txt_resultado.grid(row=8, column=0, columnspan=2, pady=10, padx=20, sticky="nsew")
        
        self.txt_elementos_analisados = customtkinter.CTkLabel(root, text=f"De xxx \nelementos analisados", font=estilo_titulo, text_color="lightgreen")
        self.txt_elementos_analisados.grid(row=8, column=2, columnspan=2, pady=10, padx=20, sticky='nsew')

        self.todas_colunas = []  # Armazena todas as colunas do arquivo CSV
                
    def upload_file_text(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                self.data = pd.read_csv(file_path, encoding='utf-8') # Tenta abrir como UTF-8
                self.gera_colunas_listbox()
                
            except UnicodeDecodeError: # Corrige o erro se o arquivo não estiver em utf-8
                try:
                    self.data = pd.read_csv(file_path, encoding='ISO-8859-1')  # Tenta abrir com ISO-8859-1
                    self.gera_colunas_listbox()
                    
                except Exception as e:
                    messagebox.showerror("[Erro!]", f"[Erro!] : {e}") 
    
    def gera_colunas_listbox(self):
        self.todas_colunas = list(self.data.columns)  # columns Propriedade DataFrame Pandas
        self.lbx_colunas.delete(0, tk.END)
        for col in self.todas_colunas:
            self.lbx_colunas.insert(tk.END, col)
                         
#region tfidf linhas
    def calcular_similiaridade_cosseno_text(self):
        colunas_selecionadas = [self.lbx_colunas.get(i) for i in self.lbx_colunas.curselection()]
        if not colunas_selecionadas:
            messagebox.showerror("[Erro!]", "Selecione Uma Coluna")
            return
        try:
            N = len(self.data)

            amostra = self.txt_amostra.get("1.0", tk.END).strip().lower()
            if not amostra:
                messagebox.showerror("[Erro!]", "Insira a Amostra")
                return

            self.txt_resultado.configure(state='normal')
            self.txt_resultado.delete(1.0, tk.END) 

            vectorizer = TfidfVectorizer(use_idf=True, stop_words="english")
            tfidf_matriz = vectorizer.fit_transform(self.data[colunas_selecionadas].fillna('').astype(str).apply(lambda x: ' '.join(x), axis=1).tolist() + [amostra])

            stop_words = vectorizer.get_stop_words()
            termos = vectorizer.get_feature_names_out()
            
            nm_coluna = colunas_selecionadas.copy()
            for i in nm_coluna:
                nome = str(i).replace("[]'", "")
                       
            self.txt_resultado.insert(tk.END, f"Top 5 Elementos Mais Semelhantes à amostra(%): ({nome})\n\n")
            tfidf_array = tfidf_matriz.toarray()

            termos = [term for term in termos if term not in stop_words] 

            similaridades = cosine_similarity(tfidf_array[-1].reshape(1, -1), tfidf_array[:-1])

            ordens = np.argsort(similaridades[0])[-5:][::-1] # top 5
            
            for i in ordens:
                porcentagem_similaridade = similaridades[0][i] * 100
                grau_similiaridade = porcentagem_similaridade / 100

                if porcentagem_similaridade > 0 and ordens.size != 0:
                    info =  self.data[colunas_selecionadas].iloc[i].to_string().replace(r"\n", " ")
                    nome_musica = self.data['Title'].iloc[i]
                    nome_artista = self.data['Artist'].iloc[i]
                    
                    self.txt_resultado.configure(state='normal')
                    self.txt_resultado.insert(tk.END, f"{i+1}) {nome_musica} - {nome_artista}:\n")
                    self.txt_resultado.insert(tk.END, f" {info}\n")
                    self.txt_resultado.insert(tk.END, f" Similiaridade: {porcentagem_similaridade:.2f}%\n")
                    self.txt_resultado.insert(tk.END, f" Similiaridade: {grau_similiaridade:.4f}º\n\n")
                else:
                    self.txt_resultado.delete(1.0, tk.END) 
                    self.txt_resultado.insert(tk.END, f"Top 5 Elementos Mais Semelhantes à amostra (%): ({nome})\n\n")
                    self.txt_resultado.insert(tk.END, f"0 Resultados Encontrados! Sem Possíveis Recomendações.\n\n")

            self.txt_elementos_analisados.configure(text=f"De {N} \nelementos analisados")
            
            self.txt_resultado.configure(state='disabled')

            messagebox.showinfo("Sucesso", "Similiaridade dos Cossenos Calculada com Sucesso!")
            
        except Exception as e:
            messagebox.showerror("[Erro!]", f"Erro ao Calcular a Similiaridade dos Cossenos: {e}")
#endregion

if __name__ == "__main__":
    root = customtkinter.CTk()
    app = IDFApp(root)
    root.mainloop()
