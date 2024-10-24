import os
import fnmatch
import shutil

def procurar_e_copiar_imagens(diretorio_principal, sku_nome_produto, diretorio_destino):
    # Extensões de arquivos de imagem que queremos procurar
    formatos = ['*.jpg', '*.jpeg', '*.png']
    
    # Criar a pasta de destino com o nome do SKU (caso não exista)
    destino_sku = os.path.join(diretorio_destino, sku_nome_produto)
    if not os.path.exists(destino_sku):
        os.makedirs(destino_sku)

    # Percorre todas as pastas e arquivos no diretório principal
    for raiz, diretorios, arquivos in os.walk(diretorio_principal):
        for formato in formatos:
            # Encontra arquivos que correspondem ao formato e contêm o sku ou nome do produto
            for arquivo in fnmatch.filter(arquivos, formato):
                if sku_nome_produto.lower() in arquivo.lower():
                    caminho_completo = os.path.join(raiz, arquivo)
                    # Copia a imagem para o diretório de destino
                    destino_arquivo = os.path.join(destino_sku, arquivo)
                    shutil.copy2(caminho_completo, destino_arquivo)
                    print(f'Imagem copiada: {destino_arquivo}')

# Exemplo de uso
diretorio_origem = r'\\desk181-mkt\Fotos Geral'  # Diretório na rede onde estão as imagens
sku_ou_nome = '01440101'  # Pode ser o código SKU ou o nome do produto
diretorio_destino = r'C:\Users\jean.marques\Desktop\procura-imagens-python'  # Diretório onde as imagens serão copiadas

procurar_e_copiar_imagens(diretorio_origem, sku_ou_nome, diretorio_destino)
