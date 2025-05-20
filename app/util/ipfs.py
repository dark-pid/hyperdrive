import hashlib
import time
import os
from io import StringIO

# V1
# def add_to_ipfs(data,api,tmp_dir='/tmp/'):
#     data = data.strip('\n')  
#     string_io = StringIO(data)
#     with open("temp.xml", "w", encoding="utf-8") as f:
#         f.write(string_io.getvalue())
#     res, obj = api.add_items("temp.xml")
#     return res, obj

def add_to_ipfs(data, api, tmp_dir='/tmp/'):
    """
    Salva o conteúdo em um arquivo temporário com nome aleatório (sha256 do conteúdo + timestamp),
    adiciona o arquivo ao IPFS usando o método `add_items` da API fornecida e remove o arquivo ao final.

    Parâmetros:
        data (str): Conteúdo a ser salvo e enviado ao IPFS.
        api: Instância da API que possui o método `add_items(filepath)`.
        tmp_dir (str): Diretório temporário onde o arquivo será criado (padrão: '/tmp/').

    Retorna:
        tuple: (res, obj) retornados por `api.add_items`.
    """
    data = data.strip('\n')
    # 
    hash_input = f"{data}{time.time()}".encode("utf-8")
    filename = hashlib.sha256(hash_input).hexdigest() + ".hdtmp"
    filepath = os.path.join(tmp_dir, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(data)
        res, obj = api.add_items(filepath)
    finally:
        # Remove o arquivo temporário, mesmo se der erro
        try:
            os.remove(filepath)
        except Exception:
            pass
    return res, obj

def get_ipfs_url(ipfs_response,ipfs_server='http://127.0.0.1:8080/ipfs/'):
    ipfs_addr = ipfs_response[1]['Hash']
    return ipfs_server + ipfs_addr