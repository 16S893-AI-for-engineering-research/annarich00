# Anna Ford-Richards Portfolio Site

Static Astro site for the **Agents in a Rendezvous** research project.

## Live URL
https://16s893-ai-for-engineering-research.github.io/annarich00/

## Local development
1. Install dependencies:
   ```bash
   npm install
   ```
2. Start the dev server:
   ```bash
   npm run dev
   ```
3. Build for production:
   ```bash
   npm run build
   ```

## Editing content
- Update page content in `src/pages/`
- Shared layout and navigation live in `src/layouts/` and `src/components/`
- Base-path handling for GitHub Pages lives in `src/lib/paths.ts`
- Source-of-truth content notes live in `docs/content-reference.md`

## Photos
Place personal photos in `public/images/` and reference them with `/annarich00/images/<file>` in production or use `resolvePath()` for internal assets.

## Deployment
Push to `main` and GitHub Actions will build and deploy to GitHub Pages.
