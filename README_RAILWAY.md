Railway deployment notes

- This repository contains a frontend app in the `sc-datav` subfolder (Vite + React).
- To ensure Railway detects Node and runs the correct build, there is a top-level `package.json`.

Recommended Railway settings:

- Build command: `npm run build`
- Start command: `npm start`
- Environment: Node 18 (or auto)

If Railway still attempts a Python build, remove any Python runtime file from repo root (e.g. `runtime.txt`, `requirements.txt`) or configure the build manually in Railway console.
