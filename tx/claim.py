from pycardano import *
from dataclasses import dataclass
import json
import cbor2


NETWORK = Network.TESTNET
chain_context = BlockFrostChainContext(
    project_id = "preview84Fg7cI0ShCtFl5ZmQaCSEJADLOFGbzh",
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
script_addr = Address(plutus_script_hash(script), network=Network.TESTNET)

# Claiming Tx
beneficiary_utxo = [
    utxo for utxo in chain_context.utxos(str(script_addr)) if utxo.input.transaction_id.payload.hex() ==
    "fd1239bf58075e3503b594865289eb3a398745e04ab9a23edf1972a413aa5e23" #change this
].pop()

@dataclass
class VestingRedeemer(PlutusData):
    CONSTR_ID = 0

redeemer = Redeemer(RedeemerTag.SPEND, VestingRedeemer()) #empty redeemer

#tx builder
builder = TransactionBuilder(chain_context)

builder.collaterals.append(
    [
        utxo for utxo in chain_context.utxos(str(addr_bf)) if utxo.input.transaction_id.payload.hex() ==
        "dfcc2e391a104e0c01bf3a68baa265c2b91f34629fe8b257b8b4ad83f2e24a24"
    ].pop()
)

builder.add_script_input(beneficiary_utxo, redeemer=redeemer)

builder.validity_start = chain_context.last_block_slot
builder.required_signers = [vkey_bf.hash()]

signed_tx = builder.build_and_sign([skey_bf], change_address=addr_bf)
print(signed_tx.transaction_body, end="\n\n")
chain_context.submit_tx(signed_tx.to_cbor())
print("########## Transaction submitted. ##########")
print(f"Transaction id: {signed_tx.id}")
