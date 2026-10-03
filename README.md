# NoveltyGate — AI Originality Gate for Grant & Research Programs

NoveltyGate stops the same research work from being counted twice across a funding
program. Deterministic contract logic enforces the policy; GenLayer's AI consensus
supplies the **semantic** judgement a plain hash can't — validators agree on a
relation **label**, never on the model's prose (project rule D3: sandboxed
`gl.vm.run_nondet` preferred).

- **Network:** studionet · chain id **61999** · RPC `https://studio.genlayer.com/api`
- **Contract:** `0x982f48e27dcc38712B84E4584ff2CEF07B3C908e`
  ([explorer](https://genlayer-explorer.vercel.app/address/0x982f48e27dcc38712B84E4584ff2CEF07B3C908e))
- **Deployer:** `0x8b563A8c9eeF530300e92E26457D1AB001daEcC7`
- **Source:** [`contracts/novelty_gate.py`](contracts/novelty_gate.py)

## How it works

A program owner opens a **program**, defines **tracks** (each with an originality
**policy** and a number of **slots**), and whitelists **submitters**. Researchers
`file_contribution` once — immutable, with a caller-supplied SHA-256 fingerprint —
then `claim_slot` against a track.

On a claim the contract gathers the prior accepted contributions whose slot the
candidate must respect, then asks the AI jury to label each relationship as one of:

| Label | Meaning |
|---|---|
| `DUPLICATE` | Substantially the same contribution (retitled / reworded / trimmed). |
| `DERIVATIVE` | Produced from / repackaging prior work, no independent inquiry. |
| `OVERLAPPING` | Shares material data/experiments but also has independent work. |
| `ORIGINAL` | Rests on materially independent inquiry, data, or method. |
| `UNCERTAIN` | Descriptors too thin to classify. |

Only an **all-`ORIGINAL`** verdict is granted. Any `UNCERTAIN` returns
`INCONCLUSIVE` for human review. An identical fingerprint is rejected
deterministically before the model is ever consulted.

**Policies:** `OPEN_REUSE` (1) · `LOCK_ORIGINAL` (2, reserves the work
program-wide) · `DISTINCT_SET` (3, every slot in a cohort stays mutually original).

## Key calls

`open_program` · `define_track` · `allow_submitter` · `lock_program` ·
`file_contribution` · `claim_slot` ·
views `get_program` / `get_track` / `get_contribution` / `get_ruling` /
`slots_remaining` / `track_full`.

## Deploy / re-deploy

```bash
source ~/.genlayer/env.sh
python3 scripts/deploy.py          # schema-checks then deploys, writes deployments.json
```

Size caps (bounded peer comparisons per claim) keep consensus cost predictable.
