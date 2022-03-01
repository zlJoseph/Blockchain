import hashlib
import json
import random
import requests

def get_hash_last_block():
    url = 'https://blockchain.info/latestblock'
    headers = {'user-agent': 'blockchain/0.0.1'}
    response = requests.get(url, headers=headers)#la respuesta _content esta en Bytes
    block=json.loads(response._content.decode('utf-8'))
    return block["hash"]

def get_block_info(hash_block):
    url = 'https://blockchain.info/rawblock/'+hash_block
    headers = {'user-agent': 'blockchain/0.0.1'}
    response = requests.get(url, headers=headers)#la respuesta _content esta en Bytes
    block=json.loads(response._content.decode('utf-8'))
    return block

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

def merkle_transactions_evaluate(transactions,txEvaluate,merkle_evaluate=[]):
    if len(transactions)==1:
        return merkle_evaluate
    else:
        merkle_tree=[]
        pairs_transactions=get_pairs_transactions(transactions)
        for i in range(0,len(pairs_transactions)):
            pair_temp=pairs_transactions[i]
            hash_merkle=set_hash_pair(pair_temp)
            merkle_tree.append(hash_merkle)
            if pair_temp[0]==txEvaluate or pair_temp[1]==txEvaluate:
                indexEvaluate=0 if pair_temp[0]==txEvaluate else 1
                merkle_evaluate.append([indexEvaluate,pair_temp[0 if indexEvaluate else 1]])
                txEvaluate=hash_merkle


        return merkle_transactions_evaluate(merkle_tree,txEvaluate,merkle_evaluate)

def validate_transaction(merkle_evaluate,transaction_evaluate):
    hash_current=transaction_evaluate
    for i in range(0,len(merkle_evaluate)):
        if merkle_evaluate[i][0]==0:
            hash_current=set_hash_pair([hash_current,merkle_evaluate[i][1]])
        else:
            hash_current=set_hash_pair([merkle_evaluate[i][1],hash_current])
    return hash_current

if __name__ == '__main__':
    print("Progam started")
    hash_block = get_hash_last_block()
    block = get_block_info(hash_block)
    txHash=[x["hash"] for x in block["tx"]]#hash de las transacciones en array
    txEva=txHash[random.randint(0,len(txHash)-1)]#se elige una transaccion al azar
    #txEva="A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6"
    merkleEva=merkle_transactions_evaluate(txHash,txEva)
    merkleRootEva=validate_transaction(merkleEva,txEva)
    print(f'¿Transacción valida?: {merkleRootEva==block["mrkl_root"]}')