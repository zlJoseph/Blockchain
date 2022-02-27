import hashlib
import json
import requests

def get_hash_last_block():
    url = 'https://blockchain.info/latestblock'
    headers = {'user-agent': 'my-app/0.0.1'}
    response = requests.get(url, headers=headers)#la respuesta _content esta en Bytes
    block=json.loads(response._content.decode('utf-8'))
    return block["hash"]

def get_block_info(hash_block):
    url = 'https://blockchain.info/rawblock/'+hash_block
    headers = {'user-agent': 'my-app/0.0.1'}
    response = requests.get(url, headers=headers)#la respuesta _content esta en Bytes
    block=json.loads(response._content.decode('utf-8'))
    return block

def get_pairs_transactions(array_transactions):
    pairs_transactions=[]
    longitud=len(array_transactions)
    for i in range(0,(longitud/2).__ceil__()):
        temp=[]
        temp.append(array_transactions[i*2])
        if (i*2+1)<longitud:
            temp.append(array_transactions[i*2+1])
        pairs_transactions.append(temp)
    return pairs_transactions

def hex_to_bytes_reverse(hex_string):
    bytes=bytearray.fromhex(hex_string)
    bytes.reverse()
    return bytes

def set_hash_pair(pair_transactions):
    if len(pair_transactions)==1:#se verifica que tenga dos elementos, si no, se repite el primer elemento
        pair_transactions.append(pair_transactions[0])
    pair_text=hex_to_bytes_reverse(pair_transactions[0]).hex()+hex_to_bytes_reverse(pair_transactions[1]).hex()
    temp=hashlib.sha256(hashlib.sha256(bytearray.fromhex(pair_text)).digest()).digest()
    return hex_to_bytes_reverse(temp.hex()).hex()

def get_merkle_tree(array_transactions):
    if len(array_transactions)==1:
        return array_transactions[0]
    else:
        merkle_tree=[]
        pairs_transactions=get_pairs_transactions(array_transactions)
        for i in range(0,len(pairs_transactions)):
            merkle_tree.append(set_hash_pair(pairs_transactions[i]))
        return get_merkle_tree(merkle_tree)

if __name__ == '__main__':
    hash_block = get_hash_last_block()
    block = get_block_info(hash_block)
    txHash=[x["hash"] for x in block["tx"]]#hash de las transacciones en array
    #print(block["mrkl_root"])
    merkle=get_merkle_tree(txHash)
    print(f'merkled valido: {merkle==block["mrkl_root"]}')