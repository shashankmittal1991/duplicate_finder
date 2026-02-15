# Frontend deployment (Vercel)

This repository serves a small static frontend from the `frontend` folder. The static launcher is available at `/launcher` when deployed to Vercel.

Quick steps

- Deploy: push this repo to GitHub and add it to Vercel (import repository). Vercel will use the `vercel.json` config to serve the `frontend` directory.
- Launcher URL (after deploy): `https://<your-vercel-app>.vercel.app/launcher`

Local testing (frontend + local server)

1. Start the local server on your machine (the frontend calls the local API at `http://localhost:8888`):

```powershell
cd "C:\Users\shashankmittal\Desktop\New folder (2)"
# use your existing start script or run the FastAPI server directly
.\n+Start-Dupfinder.bat  # or the command you use to start the local server
```

2. Open the frontend locally (for development) by opening `frontend/launcher.html` in your browser, or visit the deployed `/launcher` URL.

Notes
- The launcher calls `http://localhost:8888` for scanning, progress, duplicate listing, and delete operations. Make sure the local server is running and accessible.
- Deletion actions use the server-side delete endpoints; the server attempts to move deleted files to the recycle bin when possible.

Files

- Launcher: [frontend/launcher.html](frontend/launcher.html#L1)
- Vercel config: [vercel.json](vercel.json#L1)
