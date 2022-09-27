# Requirements
`poetry` Python dependency manager

# Installation
`poetry install`\
`poetry config virtualenvs.in-project true`\
`poetry env use python3.10`\
`source .venv/bin/activate`

Generate two keys which will be stored in the `keys` directory: `python3 utils/generate_keys.py 2`

# Use
`lock.py` locks a UTxO with beneficiary datum at the script address. `claim.py` claims the utxo sitting at this
address. `python3 utils/utxos.py` to query utxos.
