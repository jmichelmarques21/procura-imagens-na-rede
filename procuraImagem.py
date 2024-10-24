import os
import fnmatch
import shutil

def procurar_e_copiar_imagens(diretorio_principal, lista_skus, diretorio_destino):
    # Extensões de arquivos de imagem que queremos procurar
    formatos = ['*.jpg', '*.jpeg', '*.png']

    # Para cada SKU na lista de SKUs
    for sku_nome_produto in lista_skus:
        encontrou_imagem = False  # Variável para verificar se encontramos uma imagem para o SKU

        # Percorre todas as pastas e arquivos no diretório principal
        for raiz, diretorios, arquivos in os.walk(diretorio_principal):
            for formato in formatos:
                # Encontra arquivos que correspondem ao formato e contêm o SKU ou nome do produto
                for arquivo in fnmatch.filter(arquivos, formato):
                    if sku_nome_produto.lower() in arquivo.lower():
                        if not encontrou_imagem:
                            # Cria a pasta de destino com o nome do SKU, se ainda não foi criada
                            destino_sku = os.path.join(diretorio_destino, sku_nome_produto)
                            if not os.path.exists(destino_sku):
                                os.makedirs(destino_sku)
                            encontrou_imagem = True  # Marca que encontramos pelo menos uma imagem

                        # Copia a imagem para o diretório de destino
                        caminho_completo = os.path.join(raiz, arquivo)
                        destino_arquivo = os.path.join(destino_sku, arquivo)
                        shutil.copy2(caminho_completo, destino_arquivo)
                        print(f'Imagem copiada para SKU {sku_nome_produto}: {destino_arquivo}')

        if not encontrou_imagem:
            print(f'Nenhuma imagem encontrada para o SKU: {sku_nome_produto}')

# Exemplo de uso
diretorio_origem = r'\\desk181-mkt\Fotos Geral'  # Diretório na rede onde estão as imagens
lista_skus = ['']  # Lista de SKUs ou nomes de produtos
diretorio_destino = r'C:\Users\jean.marques\Desktop\procura-imagens-python'  # Diretório onde as imagens serão copiadas

procurar_e_copiar_imagens(diretorio_origem, lista_skus, diretorio_destino)
