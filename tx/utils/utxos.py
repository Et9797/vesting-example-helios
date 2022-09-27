from pycardano import *
from blockfrost import ApiError
import json
import cbor2


NETWORK = Network.TESTNET
chain_context = BlockFrostChainContext(
    project_id = "previewAsoqYq9d11fAfa9fzZr6hFCFlTbSiSFI",
    network = NETWORK,
    base_url = "https://cardano-preview.blockfrost.io/api"
)

# Addresses
skey = PaymentSigningKey.load("keys/usr1.skey")
vkey = PaymentVerificationKey.from_signing_key(skey)
my_addr = Address(vkey.hash(), network=NETWORK)

skey_bf = PaymentSigningKey.load("keys/usr2.skey")
vkey_bf = PaymentVerificationKey.from_signing_key(skey_bf)
addr_bf = Address(vkey_bf.hash(), network=NETWORK)

with open("../contract/contract.json", "r") as f:
    cbor_hex = json.load(f)["cborHex"]
script = PlutusV2Script(cbor2.loads(bytes.fromhex(cbor_hex)))
script_addr = Address(plutus_script_hash(script), network=NETWORK)


def show_balance(addr: str) -> None:
    print(f"Address: {addr}")
    print("TxHash \t\t\t\t\t\t\t\t  Idx  Coin")
    print(
        "-----------------------------------------------------------------"
        "-----------------"
    )
    try:
        utxos = chain_context.utxos(addr)
    except ApiError:
        pass
    else:
        total = 0
        for utxo in utxos:
            print(
                f"{utxo.input.transaction_id}   {utxo.input.index} "
                f"  {utxo.output.amount.coin/1_000_000:.2f} "
                f"{'+ ' + str(utxo.output.amount.multi_asset) if utxo.output.amount.multi_asset else ''}"
            )
            total += utxo.output.amount.coin
        print(f"Total balance: {total/1_000_000:.2f}")


show_balance(str(my_addr))
print()
show_balance(str(addr_bf))
print()
show_balance(str(script_addr))
