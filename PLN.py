import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import math

class IDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de TF-IDF (Dados Binários)")
        self.root.geometry("600x700")
        
        self.label = tk.Label(root, text="Escoha o Arquivo CSV:")
        self.label.pack(pady=10)
        
        self.btn_upload = tk.Button(root, text="Escolher CSV", command=self.upload_file)
        self.btn_upload.pack(pady=10)
        
        self.lbl_busca = tk.Label(root, text="Busque por colunas para calcular o IDF:")
        self.lbl_busca.pack(pady=10)
        
        self.txt_search = tk.Entry(root)
        self.txt_search.pack(pady=5)
        self.txt_search.bind("<KeyRelease>", self.filter_columns) 
        
        self.lbl_colunas = tk.Label(root, text="Selecione as Colunas Binárias:") 
        self.lbl_colunas.pack(pady=10)
        self.lbx_colunas = tk.Listbox(root, selectmode=tk.MULTIPLE, width=50) 
        self.lbx_colunas.pack(pady=10) 
        
        self.btn_calcIDF = tk.Button(root, text="Calcule o TF-IDF", command=self.calcular_idf) #, command=self.calcular_idf
        self.btn_calcIDF.pack(pady=10)
        
        self.lbl_resultado = tk.Label(root, text="Resultado:")
        self.lbl_resultado.pack(pady=10) 
        self.txt_resultado = tk.Text(root, height=10, width=60) 
        self.txt_resultado.pack(pady=10) 
        
        self.txt_elementos_analisados = tk.Label(root, text=f"") 
        self.txt_elementos_analisados.pack(pady=10)
        
        self.all_columns = []  # Armazena todas as colunas do arquivo CSV

    
    
    def gera_colunas_listbox(self):
        self.all_columns = list(self.data.columns)  # columns Propriedade DataFrame Pandas
        self.filter_columns() 
    
    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                self.data = pd.read_csv(file_path, encoding='utf-8') # Tenta abrir como UTF-8
                self.gera_colunas_listbox()
                messagebox.showinfo("Sucesso",  "Arquivo carregado com sucesso!")
                
            except UnicodeDecodeError: # Corrige o erro se o arquivo não estiver em utf-8
                try:
                    self.data = pd.read_csv(file_path, encoding='ISO-8859-1')  # Tenta abrir com ISO-8859-1
                    self.gera_colunas_listbox()
                    messagebox.showinfo("Sucesso",  "Arquivo carregado com sucesso!")
                except Exception as e:
                    messagebox.showerror("[Erro!]", f"Falha ao Carregar o Arquivo. [Erro!] : {e}")
                
    def filter_columns(self, event=None):
        search_term = self.txt_search.get().lower()  
        self.lbx_colunas.delete(0, tk.END)  # Garante que a lista esteja vazia

        for col in self.all_columns:   # Percorre as colunas do dataframe
            if search_term in col.lower():   # Verifica se a palavra está na coluna
                self.lbx_colunas.insert(tk.END, col)   # Insere a coluna na lista


                
    def calcular_idf(self):
        coluna_selecionada = [self.lbx_colunas.get(i) for i in self.lbx_colunas.curselection()]
        if not coluna_selecionada:
            messagebox.showerror("[Erro!]", "Selecione Uma ou Mais Colunas")
            return
        
        try:
            
            N = 1
            tf_pontuacao = {}
            idf_pontuacao = {}
            tfidf_pontuacao = {}
            
            self.txt_resultado.delete(1.0, tk.END)
            
            num_colunas = len(coluna_selecionada)
            
            for coluna in coluna_selecionada:
                linhas = self.data[coluna].count()  # Conta o número de linhas não nulas
                N += linhas
            
            # N = sum(len(self.data[coluna]) for coluna in coluna_selecionada)/num_colunas  # Tamanho total de todas as colunas selecionadas dividido pelo número de colunas selecionadas (Média fixa), conta linhas vazias (bad)

            for col in coluna_selecionada:
                df = self.data[col].sum()  # Número de documentos que contêm o termo (onde o valor é 1)
                
                tf = self.data[col].mean() # tf usando média dos valores, ja que tf =  (número de ocorrências do termo no documento) / (número total de termos)
                idf = math.log(N / (df + 1))  # Cálculo de IDF, adicionamos +1 para evitar divisão por zero FÓRMULA DO IDF (INVERSE DOCUMENT FREQUENCY)
                tfidf = tf * idf
            
                tf_pontuacao[col] = tf
                idf_pontuacao[col] = idf
                tfidf_pontuacao[col] =  tfidf
            
            sorted_tfidf = sorted(tfidf_pontuacao.items(), key=lambda x: x[1], reverse=True) # selcionado para tf-idf
            for coluna, pontuacao in sorted_tfidf:
                self.txt_resultado.insert(tk.END, f"{coluna}: {pontuacao}\n")
            messagebox.showinfo("Sucesso", "TF-IDF Calculado com Suceso!")

            self.txt_elementos_analisados.config(text=f"{N} elementos analisados de {num_colunas} colunas selecionadas") 

        except Exception as e:
            messagebox.showerror("[Erro!]", f"Erro ao Calcular o TF-IDF: {e}")                
                
                
if __name__ == "__main__":
    root = tk.Tk()
    app = IDFApp(root)
    root.mainloop()