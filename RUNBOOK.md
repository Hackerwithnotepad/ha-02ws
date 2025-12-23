# RUNBOOK — ha-02ws

## Current API: https://www.02ws.co.il/api/now/0/1/C/1
## Backup branch: backup-main
## Domain: o2ws (internal), Display: 02WS Weather

### Quick install (one-shot)
1. Push these files to `main`.
2. In Home Assistant: HACS → Integrations → Custom repositories → add repo URL as "Integration".
3. Install integration, restart HA.

### Debug
- If HACS errors `No manifest.json found 'manifest.json'`:
  - Ensure `hacs.json` exists at repo ROOT (not in custom_components/) with proper configuration.
  - Ensure `custom_components/o2ws/manifest.json` exists and is valid JSON.
  - Verify `custom_components/o2ws/` directory exists (not `02ws`).
  - Remove integration from HACS and re-add repo.

### Structure
```
ha-02ws/
├── hacs.json                          # HACS config at ROOT
├── README.md                          # Documentation
└── custom_components/
    └── o2ws/                          # Integration directory (domain name)
        ├── __init__.py
        ├── manifest.json
        ├── sensor.py
        ├── const.py
        └── RUNBOOK.md
```

### Key Points
- Domain is `o2ws` (not `02ws`) to comply with Python/HA naming rules
- Display name remains "02WS Weather" for users
- `hacs.json` must be at repository root, not in custom_components/
