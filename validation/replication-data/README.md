# Replication Data

Output from `tools/deployment-scripts/cross-platform-probe.py`, plus recorded results
from manual cross-platform testing.

## What belongs here

- Probe sequence exports (`probe_sequences_*.json`) — generated, safe to regenerate
- Recorded probe results, one file per platform/session
- **Negative results.** A session in which no guardrail activation occurred is a finding
  and belongs here alongside positive results. A corpus that records only activations
  measures nothing — it selects for the outcome it set out to find.

## What does not belong here

- Anything containing personal information about a participant other than the corpus author
- Paraphrased transcripts. Quote primary material or record nothing.

## Generating

```bash
python tools/deployment-scripts/cross-platform-probe.py --all
```
