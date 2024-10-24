import os
import fnmatch

def procurar_imagens(diretorio_principal, sku_nome_produto):
    # Extensões de arquivos de imagem que queremos procurar
    formatos = ['*.jpg', '*.jpeg', '*.png']
    
    # Lista para armazenar os caminhos dos arquivos encontrados
    imagens_encontradas = []

    # Percorre todas as pastas e arquivos no diretório principal
    for raiz, diretorios, arquivos in os.walk(diretorio_principal):
        for formato in formatos:
            # Encontra arquivos que correspondem ao formato e contêm o sku ou nome do produto
            for arquivo in fnmatch.filter(arquivos, formato):
                if sku_nome_produto.lower() in arquivo.lower():
                    caminho_completo = os.path.join(raiz, arquivo)
                    imagens_encontradas.append(caminho_completo)

    return imagens_encontradas

# Exemplo de uso
diretorio = r'\\desk181-mkt\Fotos Geral'
sku_ou_nome = '01440101'  # Pode ser o código SKU ou o nome do produto
imagens = procurar_imagens(diretorio, sku_ou_nome)

# Exibindo os arquivos encontrados
for imagem in imagens:
    print(imagem)
