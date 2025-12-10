# RUNBOOK — ha-02ws

## Current API: https://www.02ws.co.il/api/now/0/1/C/1
## Backup branch: backup-main

### Quick install (one-shot)
1. Push these files to `main`.
2. In Home Assistant: HACS → Integrations → Custom repositories → add repo URL as "Integration".
3. Install integration, restart HA.

### Debug
- If HACS errors `No manifest.json found 'manifest.json'`:
  - Ensure `hacs.json` exists at repo root with `"content_in_root": true`.
  - Ensure `custom_components/02ws/manifest.json` exists and is valid JSON.
  - Remove integration from HACS and re-add repo.
