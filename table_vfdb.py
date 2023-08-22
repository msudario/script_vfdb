import pandas as pd
import re
import argparse
import os




parser = argparse.ArgumentParser(
    description='Bu')
parser.add_argument('-csv', '--csv', metavar='', type=str, required=True,
                    help='path to the vfdb_gene_count.csv')
parser.add_argument('-fasta', '--fasta', metavar='', type=str, required=True,
                    help='path to the vfdb_core.fasta (from panvita)')
parser.add_argument('-o', '--output', metavar='', type=str, required=True,
                    help='path to the output of the generated csv')


args = parser.parse_args()

folder_input = os.path.expanduser(f'{args.csv}')
folder_input2 = os.path.expanduser(f'{args.fasta}')
folder_output = os.path.expanduser(f'{args.output}') + "vfdb_script_results.csv"

database_vfdb = pd.read_csv(f'{folder_input}', sep = ';')

lista_de_genes = database_vfdb['Genes']


def buscador_de_genes():
    linhas_encontradas = []  # Lista para armazenar as linhas encontradas
    
    for cada_gene in lista_de_genes:
        gene_pattern = re.escape(f'({cada_gene})')
        gene_encontrado = False  # Para controlar se o gene foi encontrado
        
        with open(f'{folder_input2}', "r") as file:
            # Iterar pelas linhas do arquivo
            for line_number, line in enumerate(file, start=1):
                # Verificar se a linha contém a expressão exata
                if re.search(gene_pattern, line):
                    if not gene_encontrado:
                        # Adicionar a linha encontrada à lista
                        linhas_encontradas.append(line)
                        gene_encontrado = True  # Marcar o gene como encontrado
                    # Pule para o próximo gene após encontrar a primeira ocorrência
                    break
        
    return linhas_encontradas  # Retorna a lista de linhas encontradas

# Chamada da função e armazenamento do resultado
linhas_encontradas = buscador_de_genes()

def encontrando_padroes(linhas_encontradas):
    padrao_produto = r'\(.*?\)\s(.*?)\s\[.*?\]'
    padrao_mecanismo = r'\[.*? - (.*?)\]'

    resultados_produto = []
    resultados_mecanismo = []

    for cada_linha in linhas_encontradas:
        match_produto = re.search(padrao_produto, cada_linha)
        match_mecanismo = re.search(padrao_mecanismo, cada_linha)
        
        if match_produto:
            conteudo_entre = match_produto.group(1)
            resultados_produto.append(conteudo_entre)
        
        
        if match_mecanismo:
            conteudo_entre2 = match_mecanismo.group(1)
            resultados_mecanismo.append(conteudo_entre2)
    
    return resultados_produto, resultados_mecanismo


resultados_produto, resultados_mecanismo = encontrando_padroes(linhas_encontradas)

def pegar_gene_e_produto():
    pegar_produto = r'\(.*?\) (.*)'
    pegar_gene = r'\((.*?)\)'
    gene_separado = []
    produto_sem_o_gene = []
    for gene in resultados_produto:
        match_depois_gene = re.search(pegar_produto, gene)
        match_gene = re.search(pegar_gene, gene)

        if match_depois_gene:
            conteudo_apos_parenteses = match_depois_gene.group(1)
            produto_sem_o_gene.append(conteudo_apos_parenteses)
        
        if match_gene:
            conteudo_antes_parenteses = match_gene.group(1)
            gene_separado.append(conteudo_antes_parenteses)

    return gene_separado, produto_sem_o_gene

gene_separado, produto_sem_o_gene = pegar_gene_e_produto()

    
# Criar um DataFrame do pandas para a tabela
data = {
    "Gene": gene_separado,
    "Product": produto_sem_o_gene,
    "Mechanism": resultados_mecanismo
}
df = pd.DataFrame(data)

# Salvar a tabela em um arquivo CSV
df.to_csv(folder_output, index=False)


    





