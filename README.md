# Shutdown Tray App (simple)

## Created using ChatGPT

### Usage

1. Change HOST / PORT / API_TOKEN in shutdown_tray.py
2. Build with bat file

PowerShell example:

```powershell
Invoke-RestMethod `
    -Method POST `
    -Uri "http://127.0.0.1:8765/shutdown" `
    -Headers @{ "X-API-Token" = "SecretToken" }
```
