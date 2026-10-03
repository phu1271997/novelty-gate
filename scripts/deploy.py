#!/usr/bin/env python3
"""Deploy NoveltyGate to GenLayer studionet.

    source ~/.genlayer/env.sh
    python3 scripts/deploy.py
"""
import json, os, sys
from pathlib import Path
from genlayer_py import create_account, create_client
from genlayer_py.chains import studionet

ROOT = Path(__file__).resolve().parent.parent
NAME = "NoveltyGate"
CONTRACT = ROOT / "contracts" / "novelty_gate.py"


def addr_from_receipt(r):
    if not r:
        return None
    if isinstance(r, dict):
        return (r.get("data", {}).get("contract_address") or r.get("contract_address")
                or r.get("contractAddress") or r.get("tx_data_decoded", {}).get("contract_address"))
    return getattr(r, "contract_address", None) or getattr(r, "contractAddress", None)


def main():
    key = os.environ.get("GENLAYER_PRIVATE_KEY")
    if not key or "REPLACE_ME" in key:
        print("ERROR: run `source ~/.genlayer/env.sh` first", file=sys.stderr)
        return 1
    account = create_account(key)
    client = create_client(chain=studionet, account=account)
    code = CONTRACT.read_text()
    print(f"Deployer: {account.address}  chain={studionet.name} (id={studionet.id})")
    client.get_contract_schema_for_code(code.encode())
    print(f"[+] {NAME}: schema OK, deploying...")
    tx = client.deploy_contract(code=code, account=account)
    rcpt = client.wait_for_transaction_receipt(
        transaction_hash=tx, status="FINALIZED", interval=3000, retries=100)
    addr = addr_from_receipt(rcpt)
    if not addr:
        raise RuntimeError("no address in receipt")
    print(f"[v] {NAME} deployed at: {addr}")
    (ROOT / "deployments.json").write_text(json.dumps({
        "network": "studionet", "chainId": studionet.id, "deployer": account.address,
        "contract": NAME, "file": "contracts/novelty_gate.py", "address": addr, "tx": str(tx),
        "explorer": f"https://genlayer-explorer.vercel.app/address/{addr}",
    }, indent=2))
    print("[v] wrote deployments.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
