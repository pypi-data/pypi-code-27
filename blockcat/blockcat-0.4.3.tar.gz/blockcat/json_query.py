import json
import requests


no = "Not Available from the explorer website"

#############################################
#############################################
#############################################
# 1 These two functions are bitcoin functions
#############################################
#############################################
#############################################


url = "https://blockchain.info/rawtx/"
burl = "https://blockchain.info/rawblock/"

#seek the input and output address of a specified transaction
def tx_addr(tx):
    transaction = json.loads(requests.get(url + tx).text)
    try:
        if transaction["inputs"]:
            prev_out = transaction["inputs"][0]["prev_out"]
            input_addr = prev_out["addr"]
            print("Input address is: " + input_addr)
        else:
            print("Input address is: " + no)
    except KeyError:
        print("Input address is: " + no)
        
    try:
        if transaction["out"]:
            out = transaction["out"][0]
            output_addr = out["addr"]
            print("Output address is: " + output_addr)
        else:
            print("Output address is: " + no)
    except KeyError:
        print("Output address is: " + no)

def block_lookup(blockhash):
    block = json.loads(requests.get(burl + blockhash).text)
    print("Block "+ blockhash + " has following information: ")
    
    try:
        if block["ver"] or block["ver"] == 0:
            print("Version: " + str(block["ver"]))
        else:
            print("Version: " + no)
    except KeyError:
        print("Version: " + no)

    try:
        if block["prev_block"]:
            print("Previous block is : " + block["prev_block"])
        else:
            print("Previous block is : " + no)
    except KeyError:
        print("Previous block is : " + no)


    try:
        if block["time"]:
            print("Time: " + str(block["time"]))
        else:
            print("Time: " + no)
    except KeyError:
        print("Time: " + no)

    try:
        if block["mrkl_root"]:
            print("Merkle Root: " + block["mrkl_root"])
        else:
            print("Merkle Root: " + no)
    except KeyError:
        print("Merkle Root: " + no)

    try:
        if block["bits"]:
            print("Bits: " + str(block["bits"]))
        else:
            print("Bits: " + no)
    except KeyError:
        print("Bits: " + no)

    try:
        if block["nonce"]:
            print("Nonce: " + str(block["nonce"]))
        else:
            print("Nonce: " + no)
    except KeyError:
        print("Nonce: " + no)

    try:
        if block["n_tx"]:
            print("Number of transactions: " + str(block["n_tx"]))
        else:
            print("Number of transactions: " + no)
    except KeyError:
        print("Number of transactions: " + no)

    try:
        if block["size"]:
            print("Size: " + str(block["size"]))
        else:
            print("Size: " + no)
    except KeyError:
        print("Size: " + no)

    try:
        if block["block_index"] or block["block_index"] == 0:
            print("Block index: " + str(block["block_index"]))
        else:
            print("Block index: " + no)
    except KeyError:
        print("Block index: " + no)

    try:
        if block["height"]:
            print("Height: " + str(block["height"]))
        else:
            print("Height: " + no)
    except KeyError:
        print("Height: " + no)

    try:
        if block["received_time"]:
            print("Received time: " + str(block["received_time"]))
        else:
            print("Received time: " + no)
    except KeyError:
        print("Received time: " + no)

    try:
        if block["relayed_by"]:
            print("Relayed_by: " + block["relayed_by"])
        else:
            print("Relayed_by: " + no)
    except KeyError:
        print("Relayed_by: " + no)

    try:
        if block["tx"]:
            print("Transactions:")
            for tx in block["tx"]:
                print(tx["hash"])
    except KeyError:
        return


##########################################
##########################################
##########################################
# 2 These four functions are for the Zcash
##########################################
##########################################
##########################################

# find the block information
def block_lookup_zcash(blockhash):
    url = "https://api.zcha.in/v2/mainnet/blocks/"
    block = json.loads(requests.get(url + blockhash).text)
    print("Block "+ blockhash + " has following information: ")
    
    try:
        if block["version"] or block["version"] == 0:
            print("Version: " + str(block["version"]))
        else:
            print("Version: " + no )
    except KeyError:
        print("Version: " + no )


    try:
        if block["size"]:
            print("Size: " + str(block["size"]))
        else:
            print("Size: " + no)
    except KeyError:
        print("Size: " + no)

    try:
        if block["height"]:
            print("Height: " + str(block["height"]))
        else:
            print("Height: " + no)
    except KeyError:
            print("Height: " + no)

    try:
        if block["nonce"]:
            print("Nonce: " + str(block["nonce"]))
        else:
            print("Nonce: " + no)
    except KeyError:
        print("Nonce: " + no)

    try:
        if block["time"]:
            print("Time: " + str(block["time"]))
        else:
            print("Time: " + no)
    except KeyError:
        print("Time: " + no)


    try:
        if block["timestamp"]:
            print("Timestamp: " + str(block["timestamp"]))
        else:
            print("Timestamp: " + no)
    except KeyError:
        print("Timestamp: " + no)


    try:
        if block["merkleRoot"]:
            print("Merkle Root: " + block["merkleRoot"])
        else:
            print("Merkle Root: " + no)
    except KeyError:
        print("Merkle Root: " + no)

    try:
        if block["bits"]:
            print("Bits: " + str(block["bits"]))
        else:
            print("Bits: " + no)
    except KeyError:
        print("Bits: " + no)

    try:
        if block["miner"]:
            print("Miner is: " + block["miner"])
        else:
            print("Miner is: " + no)
    except KeyError:
        print("Miner is: " + no)

    try:
        if block["chainWork"]:
            print("Chain work is: " + block["chainWork"])
        else:
            print("Chain work is: " + no)
    except KeyError:
        print("Chain work is: " + no)

    try:
        if block["prevHash"]:
            print("Previous block is: " + block["prevHash"])
        else:
            print("Previous block is: " + no)
    except KeyError:
        print("Previous block is: " + no)

    try:
        if block["nextHash"]:
            print("Next block is: " + block["nextHash"])
        else:
            print("Next block is: " + no)
    except KeyError:
        print("Next block is: " + no)

    try:
        if block["solution"]:
            print("Solution: " + block["solution"])
        else:
            print("Solution: " + no)
    except KeyError:
        print("Solution: " + no)

    try:
        if block["transactions"]:
            print("Number of transactions: " + str(block["transactions"]))
        else:
            print("Number of transactions: " + no)
    except KeyError:
        print("Number of transactions: " + no)


    turl = "https://api.zcha.in/v2/mainnet/blocks/" + blockhash + "/transactions?limit=10&offset=0&sort=index&direction=ascending"
    tx = json.loads(requests.get(turl).text)
    print("Transactions: (Display 10) ")
    for i in range(len(tx)):
        try:
            if tx[i]["hash"]:
                print(tx[i]["hash"])
        except KeyError:
            return



def real_time_zcash():
    url = "https://api.zcha.in/v2/mainnet/network"
    real = json.loads(requests.get(url).text)
    print("The real time information of Zcash: ")
    
    try:
        if real["accounts"] or real["accounts"] == 0:
            print("Count of unique seen accounts (addresses): " + str(real["accounts"]))
        else:
            print("Count of unique seen accounts (addresses): " + no)
    except KeyError:
            print("Count of unique seen accounts (addresses): " + no)

    try:
        if real["blockHash"]:
            print("Current block (chain head) hash: " + real["blockHash"])
        else:
            print("Current block (chain head) hash: " + no)
    except KeyError:
        print("Current block (chain head) hash: " + no)

    try:
        if real["hashrate"]:
            print("Current estimated network hashrate over the past 120 blocks: " + str(real["hashrate"]))
        else:
            print("Current estimated network hashrate over the past 120 blocks: " + no)
    except KeyError:
        print("Current estimated network hashrate over the past 120 blocks: " + no)

    try:
        if real["meanBlockTime"]:
            print("Mean block time over the past 120 blocks (seconds): " + str(real["meanBlockTime"]))
        else:
            print("Mean block time over the past 120 blocks (seconds): " + no)
    except KeyError:
        print("Mean block time over the past 120 blocks (seconds): " + no)

    try:
        if real["relayFee"]:
            print("Current transaction relay fee: " + str(real["relayFee"]))
        else:
            print("Current transaction relay fee: " + no)
    except KeyError:
        print("Current transaction relay fee: " + no)

    try:
        if real["peerCount"] or real["peerCount"] == 0:
            print("Count of connected peers: " + str(real["peerCount"]))
        else:
            print("Count of connected peers: " + no)
    except KeyError:
        print("Count of connected peers: " + no)

    try:
        if real["totalAmount"]:
            print("Total amount of ZEC in circulation: " + str(real["totalAmount"]))
        else:
            print("Total amount of ZEC in circulation: " + no)
    except KeyError:
        print("Total amount of ZEC in circulation: " + no)

    try:
        if real["transactions"]:
            print("All-time transaction count: " + str(real["transactions"]))
        else:
            print("All-time transaction count: " + no)
    except KeyError:
        print("All-time transaction count: " + no)


def tx_addr_zcash(tx):
    url = "https://api.zcha.in/v2/mainnet/transactions/"
    transaction = json.loads(requests.get(url + tx).text)
    print("Transaction "+ tx + " has following information: ")

    try:
        if transaction["index"] or transaction["index"] == 0:
            print("Index: " + str(transaction["index"]))
        else:
            print("Index: " + no)
    except KeyError:
            print("Index: " + no)

    try:
        if transaction["version"] or transaction["version"] == 0:
            print("Version: " + str(transaction["version"]))
        else:
            print("Version: " + no)
    except KeyError:
            print("Version: " + no)

    try:
        if transaction["blockHeight"]:
            print("Inculded in Block: " + str(transaction["blockHeight"]))
        else:
            print("Inculded in Block: " + no)
    except KeyError:
            print("Inculded in Block: " + no)

    try:
        if transaction["blockHash"]:
            print("Block Hash: " + transaction["blockHash"])
        else:
            print("Block Hash: " + no)
    except KeyError:
            print("Block Hash: " + no)

    try:
        if transaction["timestamp"]:
            print("Timestamp: " + str(transaction["timestamp"]))
        else:
             print("Timestamp: " + no)
    except KeyError:
        print("Timestamp: " + no)

    try:
        if transaction["time"]:
            print("Time: " + str(transaction["time"]))
        else:
            print("Time: " + no)
    except KeyError:
        print("Time: " + no)

    try:
        if transaction["vin"]:
            if(transaction["vin"][0]["retrievedVout"]["scriptPubKey"]["addresses"] == None):
                print("Inputs: Newly Generated Coins")
            else:
                print("Inputs: " + str(transaction["vin"][0]["retrievedVout"]["scriptPubKey"]["addresses"]))
        else:
            print("Inputs: " + no)
    except KeyError:
        print("Inputs: " + no)

    try:
        if transaction["vout"]:
            for i in range(len(transaction["vout"])):
                print("Outputs: " + str(transaction["vout"][i]["scriptPubKey"]["addresses"]))
        else:
            print("Outputs: " + no)
    except KeyError:
        print("Outputs: " + no)


def addr_zcash(addr):
    url = "https://api.zcha.in/v2/mainnet/accounts/"
    address =  json.loads(requests.get(url + addr).text)
    print("Account "+ addr + " has following information: ")

    try :
        if address["balance"]:
            print("Transparent Balance: " + str(address["balance"]) + " ZEC")
        else:
            print("Transparent Balance: " + no)
    except KeyError:
        print("Transparent Balance: " + no)


    try:
        if address["firstSeen"]:
            print("First seen: " + str(address["firstSeen"]))
        else:
            print("First seen: " + no)
    except KeyError:
        print("First seen: " + no)

    try:
        if address["lastSeen"]:
            print("Last seen: " + str(address["lastSeen"]))
        else:
            print("Last seen: " + no)
    except KeyError:
            print("Last seen: " + no)

    try:
        if address["minedCount"] or address["minedCount"] == 0:
            print("Blocks mined: " + str(address["minedCount"]))
        else:
            print("Block mined: " + no)
    except KeyError:
            print("Block mined: " + no)

    try:
        if address["sentCount"] or address["sentCount"] == 0:
            print("Txns sent: " + str(address["sentCount"]))
        else:
            print("Block mined: " + no)
    except KeyError:
        print("Block mined: " + no)

    try:
        if address["recvCount"] or address["recvCount"] == 0:
            print("Txns Received: " + str(address["recvCount"]) + " ZEC")
        else:
            print("Txns Received: " + no)
    except KeyError:
            print("Txns Received: " + no)

    try:
        if address["totalSent"] or address["totalSent"] == 0:
            print("Total sent: " + str(address["totalSent"] ) + " ZEC")
        else:
            print("Total sent: " + no)
    except KeyError:
            print("Total sent: " + no)

    try:
        if address["totalRecv"] or address["totalRecv"] == 0:
            print("Total Received: " + str(address["totalRecv"]) + " ZEC")
        else:
            print("Total Received: "  + no)
    except KeyError:
            print("Total Received: "  + no)






#addr_zcash("t3M4jN7hYE2e27yLsuQPPjuVek81WV3VbBj")
#tx_addr_zcash("209549a5b8b673806cc31e1bf4b6c597c80670b1322cc81fa42be970f41fa770")
#real_time_zcash()
#block_lookup_zcash("000000000afb9d14dee1e64ce481c2b2c20ccece41724d0dc35912f1922ee2c7")
#block_lookup("0000000000000bae09a7a393a8acded75aa67e46cb81f7acaa5ad94f9eacd103")
#tx_addr("60a44c4da9e63632a970a44adbf50f930b1114530d0af829fc7e26eee78189d8")
