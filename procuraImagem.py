import os
import fnmatch
import shutil
from concurrent.futures import ThreadPoolExecutor
from PIL import Image  # Biblioteca Pillow para manipulação de imagens

def indexar_arquivos(diretorio_principal, formatos):
    """ Cria um índice de arquivos de imagem encontrados no diretório principal """
    index = {}
    for raiz, _, arquivos in os.walk(diretorio_principal):
        for formato in formatos:
            for arquivo in fnmatch.filter(arquivos, formato):
                caminho_completo = os.path.join(raiz, arquivo)
                index[arquivo.lower()] = caminho_completo
    return index

def processar_imagem(caminho_imagem, destino_arquivo):
    """ Verifica e ajusta as dimensões da imagem conforme necessário """
    with Image.open(caminho_imagem) as img:
        largura, altura = img.size
        
        if largura >= 1000 and altura >= 1000:
            # Imagem já tem tamanho suficiente; copia como está
            shutil.copy2(caminho_imagem, destino_arquivo)
            print(f'Imagem copiada sem alterações: {destino_arquivo}')
        else:
            # Redimensiona a imagem para 1000x1000, mantendo proporção
            proporcao = min(1000 / largura, 1000 / altura)
            nova_largura = int(largura * proporcao)
            nova_altura = int(altura * proporcao)
            img_redimensionada = img.resize((nova_largura, nova_altura), Image.LANCZOS)

            # Cria uma nova imagem de 1000x1000 com fundo branco e coloca a imagem redimensionada no centro
            nova_imagem = Image.new("RGB", (1000, 1000), (255, 255, 255))
            pos_x = (1000 - nova_largura) // 2
            pos_y = (1000 - nova_altura) // 2
            nova_imagem.paste(img_redimensionada, (pos_x, pos_y))

            # Salva a nova imagem redimensionada
            nova_imagem.save(destino_arquivo)
            print(f'Imagem redimensionada e copiada: {destino_arquivo}')

def copiar_imagens_para_sku(sku_nome_produto, index, diretorio_destino):
    """ Processa as imagens que correspondem ao SKU e ajusta suas dimensões conforme necessário """
    encontrou_imagem = False
    destino_sku = os.path.join(diretorio_destino, sku_nome_produto)
    
    for nome_arquivo, caminho_completo in index.items():
        if sku_nome_produto.lower() in nome_arquivo:
            if not encontrou_imagem and not os.path.exists(destino_sku):
                os.makedirs(destino_sku)
            encontrou_imagem = True
            destino_arquivo = os.path.join(destino_sku, os.path.basename(caminho_completo))
            processar_imagem(caminho_completo, destino_arquivo)

    if not encontrou_imagem:
        print(f'Nenhuma imagem encontrada para o SKU: {sku_nome_produto}')

def procurar_e_copiar_imagens(diretorio_principal, lista_skus, diretorio_destino):
    # Extensões de arquivos de imagem
    formatos = {'*.jpg', '*.jpeg', '*.png'}
    index = indexar_arquivos(diretorio_principal, formatos)

    # Executa a cópia em paralelo para cada SKU
    with ThreadPoolExecutor() as executor:
        for sku in lista_skus:
            executor.submit(copiar_imagens_para_sku, sku, index, diretorio_destino)

# Exemplo de uso
diretorio_origem = r'\\desk181-mkt\Fotos Geral'
lista_skus = ['triângulos']
diretorio_destino = r'C:\Users\jean.marques\Desktop\procura-imagens-python'

procurar_e_copiar_imagens(diretorio_origem, lista_skus, diretorio_destino)
