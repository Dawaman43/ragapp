# ragapp monorepo

This repository is configured as a pnpm workspace containing the `frontend` and `backend` packages.

Quick commands:

    pnpm install

Run development for all packages:

    pnpm dev

Run a script in all workspaces (parallel):

    pnpm -w -r run build

Notes:

- `frontend` already contains a `package.json` configured for Vite.
- Add or customize `backend/index.js` (or change backend scripts) to run your server.
