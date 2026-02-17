# Duplicate Finder - Browser Website

This project is a website-based duplicate finder and deletion tool for local media files.

## What It Does

- Lets you pick a local folder from the website.
- Creates a required runtime file inside that folder: `dupfinder-runtime.json`.
- Scans media files for duplicates using hash matching.
- Lets you delete selected duplicates or all duplicates while keeping one file per group.
- Exports a JSON report.

## How To Use

1. Open `frontend/launcher.html` in Chrome or Edge.
2. Click `Select Folder` and grant read/write permission.
3. Click `Go Ahead` to scan.
4. Review duplicate groups.
5. Click `Delete Selected` or `Delete All Duplicates`.

## Supported Media Types

- Images: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.heic`, `.heif`
- Videos: `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`, `.mpg`, `.mpeg`

## Deployment

- `vercel.json` routes `/launcher` to `frontend/launcher.html`.
- Deploy to Vercel as a static site.

## Project Structure

```text
.
|-- frontend/
|   `-- launcher.html
|-- vercel.json
|-- .gitignore
`-- README.md
```
