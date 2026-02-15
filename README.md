# Duplicate Finder - Local + Web Launcher

A tool to find and delete duplicate files (images & videos) from your local machine, controlled via a web-based interface that can run remotely on Vercel while operating on your local files.

## Architecture

- **Backend**: FastAPI server (Python) running locally on `http://localhost:8888`
- **Frontend**: Static HTML/CSS/JavaScript hosted on Vercel
- **Safety**: Deleted files go to the recycle bin using `send2trash`

## Quick Start

### Prerequisites
- Python 3.9+ (with Anaconda)
- Git
- Local network access (frontend calls backend at `http://localhost:8888`)

### 1. Start Local Server

```powershell
cd "C:\Users\shashankmittal\Desktop\New folder (2)"
"C:\Users\shashankmittal\anaconda3\Scripts\conda.exe" run -p "C:\Users\shashankmittal\anaconda3" --no-capture-output python -m uvicorn server.app:app --host 127.0.0.1 --port 8888
```

The server will start at `http://127.0.0.1:8888` and listen for API requests.

### 2. Use Frontend (Option A: Local Testing)

Open `frontend/launcher.html` in your browser to test locally.

### 3. Use Frontend (Option B: Vercel Hosted)

Visit your Vercel deployment (URL will be provided after deployment):
```
https://<your-project>.vercel.app/launcher
```

> **Note:** The Vercel-hosted frontend calls `http://localhost:8888` — your local server must be running and accessible.

## API Endpoints

All endpoints are on the local server at `http://127.0.0.1:8888`:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/change-folder` | Set the folder to scan |
| GET | `/api/progress` | Get current scan progress |
| GET | `/api/summary` | Get summary: file count, groups, recoverable space |
| GET | `/api/duplicates` | List all duplicate groups with file hashes |
| POST | `/api/delete-paths` | Delete specific file paths (to recycle bin) |
| POST | `/api/delete-all` | Delete all duplicates (keeps one per group) |

## File Structure

```
.
├── server/
│   └── app.py              # FastAPI backend (scanning, hashing, deletion)
├── frontend/
│   └── launcher.html       # Static web UI
├── requirements.txt        # Python dependencies
├── vercel.json             # Vercel deployment config
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Deployment

### Vercel (Frontend)

1. Go to [https://vercel.com/dashboard](https://vercel.com/dashboard)
2. Click "Add New Project"
3. Import the GitHub repo: `https://github.com/shashankmittal1991/duplicate_finder`
4. Vercel will auto-detect `vercel.json` and deploy `frontend/` to the root
5. Your site will be available at `https://<project>.vercel.app/launcher`

### Local Server

No deployment needed — run locally on your machine. The server listens on `http://127.0.0.1:8888` and responds to requests from the web frontend.

## Development

### Install Dependencies

```powershell
"C:\Users\shashankmittal\anaconda3\Scripts\conda.exe" run -p "C:\Users\shashankmittal\anaconda3" pip install -r requirements.txt
```

### Run Locally

```powershell
cd "C:\Users\shashankmittal\Desktop\New folder (2)"
"C:\Users\shashankmittal\anaconda3\Scripts\conda.exe" run -p "C:\Users\shashankmittal\anaconda3" python -m uvicorn server.app:app --host 127.0.0.1 --port 8888
```

### Test Endpoints

```cmd
curl http://127.0.0.1:8888/api/progress
curl http://127.0.0.1:8888/api/summary
curl http://127.0.0.1:8888/api/duplicates
```

## How It Works

1. **Select a folder** via the web UI (input path or browse locally)
2. **Scan folder** — server computes MD5 hashes of all images/videos
3. **View duplicates** — grouped by hash with counts and sizes
4. **Delete duplicates** — select groups to delete (keeps one per group) or delete all
   - Files are moved to recycle bin (`send2trash`) when possible
5. **Export report** — download JSON summary of duplicates found

## Supported Media Types

- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.heic`, `.heif`
- **Videos**: `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`, `.mpg`, `.mpeg`

## Security & Privacy

- **CORS enabled** for Vercel frontend to call local API
- **Path guards** prevent access to files outside the selected folder
- **Recycle bin** ensures deletions are recoverable
- **No data upload** — all processing happens locally on your machine

## Troubleshooting

### Frontend shows 404 / Connection refused
- Ensure the **local server is running** on `http://127.0.0.1:8888`
- Check firewall / antivirus isn't blocking port 8888
- Reload the frontend page

### Server won't start (missing module)
- Ensure dependencies are installed: `pip install -r requirements.txt`
- If using Anaconda, run commands via `conda run -p <env>`

### Files won't delete
- Check file permissions (ensure you have write access to the folder)
- Some files may be locked by other processes — try again after closing the app
- Verify the recycle bin has space

## GitHub

Repository: [https://github.com/shashankmittal1991/duplicate_finder](https://github.com/shashankmittal1991/duplicate_finder)

## License

Private project. For personal use only.

