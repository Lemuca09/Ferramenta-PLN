import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import statistics as st
import math
from sklearn.feature_extraction.text import TfidfVectorizer


class IDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Recomendaões Spotify (TD-IDF)")
        self.root.geometry("600x700")
        
        self.label = tk.Label(root, text="Escoha o Arquivo CSV:")
        self.label.pack(pady=10)
        
        self.btn_upload = tk.Button(root, text="Escolher", command=self.upload_file_text)
        self.btn_upload.pack(pady=10)
        
        self.lbl_busca = tk.Label(root, text="Busque por colunas para calcular o TF-IDF (Lyrics):")
        self.lbl_busca.pack(pady=10)
        
        self.txt_search = tk.Entry(root)
        self.txt_search.pack(pady=5)
        self.txt_search.bind("<KeyRelease>", self.filtrar_colunas_text) 
        
        self.lbl_colunas = tk.Label(root, text="Selecione a Coluna:") 
        self.lbl_colunas.pack(pady=10)
        self.lbx_colunas = tk.Listbox(root, selectmode=tk.SINGLE, width=50) 
        self.lbx_colunas.pack(pady=10) 
        
        self.btn_calcIDF = tk.Button(root, text="Calcule o TF-IDF", command=self.calcular_tfidf_text_linha)
        self.btn_calcIDF.pack(pady=10)
        
        self.lbl_resultado = tk.Label(root, text="Resultado:")
        self.lbl_resultado.pack(pady=10) 
        self.txt_resultado = tk.Text(root, height=10, width=60) 
        self.txt_resultado.pack(pady=10) 
        
        self.txt_elementos_analisados = tk.Label(root, text=f"") 
        self.txt_elementos_analisados.pack(pady=10)
        
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
        self.filtrar_colunas_text() 
                   
    def filtrar_colunas_text(self, event=None):
        termo_busca = self.txt_search.get().lower()  
        self.lbx_colunas.delete(0, tk.END)  # Garante que a lista esteja vazia

        for col in self.data.select_dtypes(include=['object']).columns:   # Percorre as colunas do dataframe
            if termo_busca in col.lower():   # Verifica se a palavra está na coluna
                self.lbx_colunas.insert(tk.END, col)    
                         
#region tfidf linhas
    def calcular_tfidf_text_linha(self):
        colunas_selecionadas = [self.lbx_colunas.get(i) for i in self.lbx_colunas.curselection()]
        if not colunas_selecionadas:
            messagebox.showerror("[Erro!]", "Selecione Pelo Menos Uma Coluna")
            return
        try:
            N = len(self.data)
            
            txt_data = self.data[colunas_selecionadas].fillna('').astype(str).apply(lambda x: ' '.join(x), axis=1).tolist() # Converte o DataFrame para uma lista de strings do cónteudo das rows e dropa as linhas vazias
            vectorizer = TfidfVectorizer(use_idf=True, stop_words="english")
            tfidf_matriz = vectorizer.fit_transform(txt_data)  # Cria uma matriz com valores de TF-IDF (fit transform) após receber a lista de textos
            
            stop_words = vectorizer.get_stop_words()
            termos = vectorizer.get_feature_names_out()
            idf_pontos = dict(zip(termos, vectorizer.idf_)) #Cria um dicionário, onde as chaves são os termos(str, por causa do get_feature...) e os valores são os idf(ndarray), em formato de tupla(termo, idf)
            
            self.txt_resultado.delete(1.0, tk.END) # Limpa o txt de resultado
            
            self.txt_resultado.insert(tk.END, f"TF-IDF (Matriz por Coluna): {colunas_selecionadas}\n\n")
            tfidf_array = tfidf_matriz.toarray()
            
            if stop_words in termos:
                termos.remove(stop_words)

            for i, linha in enumerate(tfidf_array):
                self.txt_resultado.insert(tk.END, f"Documento {i+1}: \n")
                for term, valor_tfidf in zip(termos, linha):
                    if valor_tfidf > 0:  # Exibe apenas termos relevantes (com TF-IDF > 0)
                        self.txt_resultado.insert(tk.END, f" {term}: {valor_tfidf:.4f}\n")
                self.txt_resultado.insert(tk.END, "\n")

            self.txt_elementos_analisados.config(f"De {N} elementos analisados")

            messagebox.showinfo("Sucesso", "TF-IDF Calculado com Suceso!")
            
        except Exception as e:
            messagebox.showerror("[Erro!]", f"Erro ao Calcular o TF-IDF: {e}")
#endregion

if __name__ == "__main__":
    root = tk.Tk()
    app = IDFApp(root)
    root.mainloop()