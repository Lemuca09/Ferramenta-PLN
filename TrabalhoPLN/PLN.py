import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import statistics as st
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Inicializa o NLTK
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class IDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recomendaões Spotify (TD-IDF)")
        self.root.geometry("600x700")
        
        self.label = tk.Label(root, text="Escoha o Arquivo CSV:")
        self.label.grid(row=0, column=0, columnspan=2, pady=10, padx=50)
        
        self.btn_upload = tk.Button(root, text="Escolher", command=self.upload_file_text)
        self.btn_upload.grid(row=1, column=0, columnspan=2, pady=10, padx=50) 
        
        self.lbl_colunas = tk.Label(root, text="Selecione a Coluna:") 
        self.lbl_colunas.grid(row=2, column=0, pady=10, padx=50)
        self.lbx_colunas = tk.Listbox(root, selectmode=tk.SINGLE, width=50) 
        self.lbx_colunas.grid(row=3, column=0, columnspan=2, pady=10, padx=50) 
        
        self.lbl_amostra = tk.Label(root, text="Insira a Amostra:")
        self.lbl_amostra.grid(row=4, column=0, columnspan=2, pady=10, padx=50)
        self.txt_amostra = tk.Text(root, height=5, width=60)
        self.txt_amostra.grid(row=5, column=0, columnspan=2, pady=10, padx=50)

        self.btn_calcIDF = tk.Button(root, text="Calcule o TF-IDF", command=self.calcular_tfidf_text_linha)
        self.btn_calcIDF.grid(row=6, column=0, columnspan=2, pady=10, padx=50)
        
        self.lbl_resultado = tk.Label(root, text="Resultado:")
        self.lbl_resultado.grid(row=7, column=0, columnspan=2, pady=10, padx=50) 
        self.txt_resultado = tk.Text(root, height=10, width=60) 
        self.txt_resultado.grid(row=8, column=0, columnspan=2, pady=10, padx=50) 
        
        self.txt_elementos_analisados = tk.Label(root, text=f"") 
        self.txt_elementos_analisados.grid(row=9, column=0, columnspan=2, pady=10, padx=50)

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
    def calcular_tfidf_text_linha(self):
        colunas_selecionadas = [self.lbx_colunas.get(i) for i in self.lbx_colunas.curselection()]
        if not colunas_selecionadas:
            messagebox.showerror("[Erro!]", "Selecione Pelo Menos Uma Coluna")
            return
        try:
            N = len(self.data)
            
            amostra = self.txt_amostra.get("1.0", tk.END).strip()
            if not amostra:
                messagebox.showerror("[Erro!]", "Insira a Amostra")
                return

            # Calcula o TF-IDF para a amostra e para os documentos
            vectorizer = TfidfVectorizer(use_idf=True, stop_words="english")
            tfidf_matriz = vectorizer.fit_transform(self.data[colunas_selecionadas].fillna('').astype(str).apply(lambda x: ' '.join(x), axis=1).tolist() + [amostra])

            stop_words = vectorizer.get_stop_words()
            termos = vectorizer.get_feature_names_out()
            idf_pontos = dict(zip(termos, vectorizer.idf_)) 

            self.txt_resultado.delete(1.0, tk.END) 
            self.txt_resultado.insert(tk.END, f"TF-IDF (Matriz por Coluna): {colunas_selecionadas}\n\n")
            tfidf_array = tfidf_matriz.toarray()

            # Remove as stopwords da lista de termos
            termos = [term for term in termos if term not in stop_words] 

            # Calcula a similaridade do cosseno entre a amostra e os documentos
            similaridades = cosine_similarity(tfidf_array[-1].reshape(1, -1), tfidf_array[:-1])

            # Ordena os documentos pela similaridade em ordem decrescente
            ordens = np.argsort(similaridades[0])[::-1]

            # Exibe os documentos mais próximos à amostra
            self.txt_resultado.insert(tk.END, f"Documentos mais próximos à amostra:\n\n")
            for i in ordens:
                porcentagem_similaridade = similaridades[0][i] * 100
                # Obtém o nome da música da coluna "Title"
                nome_musica = self.data['Title'].iloc[i] 
                # Obtém o nome do artista da coluna "Artist"
                nome_artista = self.data['Artist'].iloc[i]
                self.txt_resultado.insert(tk.END, f"{nome_musica} - {nome_artista}: {porcentagem_similaridade:.2f}%\n")
                self.txt_resultado.insert(tk.END, f" {self.data[colunas_selecionadas].iloc[i].to_string()}\n\n")

            self.txt_elementos_analisados.config(text=f"De {N} elementos analisados")

            messagebox.showinfo("Sucesso", "TF-IDF Calculado com Suceso!")
            
        except Exception as e:
            messagebox.showerror("[Erro!]", f"Erro ao Calcular o TF-IDF: {e}")
#endregion

if __name__ == "__main__":
    root = tk.Tk()
    app = IDFApp(root)
    root.mainloop()
