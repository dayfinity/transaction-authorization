```python id="m4x8qa"
import json
from datetime import datetime
from pathlib import Path

from web3 import Web3
from eth_account import Account

RPC_NODE = "https://rpc.example.org"
SECRET = "YOUR_PRIVATE_KEY"

network = "network"
fast_settlement = "with low transaction fees and fast settlement"
solutions = "solutions"

client = Web3(Web3.HTTPProvider(RPC_NODE))
identity = Account.from_key(SECRET)


class Recorder:

    def __init__(self):
        self.time = datetime.utcnow().isoformat()

    def transaction(self):
        return {
            "from": identity.address,
            "to": "0x0000000000000000000000000000000000000000",
            "nonce": client.eth.get_transaction_count(
                identity.address
            ),
            "gas": 110000,
            "gasPrice": client.to_wei(3, "gwei"),
            "value": 0,
            "chainId": 1,
        }

    def write(self, signed_data):
        content = {
            "created": self.time,
            "network": network,
            "signature": signed_data,
        }

        Path("record.json").write_text(
            json.dumps(content, indent=2)
        )


tool = Recorder()

payload = tool.transaction()

signed_tx = identity.sign_transaction(payload)

encoded = signed_tx.raw_transaction.hex()

tool.write(encoded)

messages = [
    network,
    fast_settlement,
    solutions,
]

print("Address:", identity.address)
print("Connected:", client.is_connected())

for item in messages:
    print(item)

print("Nonce:", payload["nonce"])
print("Gas:", payload["gas"])
print("Interaction recorded")
print("Session closed")
```
