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

# Locking Tx
@dataclass
class VestingDatum(PlutusData):
    beneficiary_pkh: bytes
    deadline: int

datum = VestingDatum(
    beneficiary_pkh = addr_bf.payment_part.payload,
    deadline = 1664571348000
)

builder = TransactionBuilder(chain_context)

builder.add_input_address(my_addr)

builder.add_output(
    TransactionOutput(
        address = script_addr,
        amount = 10_000_000,
        datum = datum,
        script = script
    )
)

signed_tx = builder.build_and_sign([skey], change_address=my_addr)
print(signed_tx, end="\n\n")
chain_context.submit_tx(signed_tx.to_cbor())
print("########## Transaction submitted. ##########")
print(f"Transaction id: {signed_tx.id}")
