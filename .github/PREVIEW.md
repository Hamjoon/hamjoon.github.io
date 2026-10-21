# Pull request previews

Cloudflare Pages provides previews for this repository. Production remains on
GitHub Pages at `https://garibong.dev`; no DNS migration is needed.

## Review flow

1. Open a pull request from a branch in this repository.
2. Wait for the Cloudflare Pages check and preview comment on the pull request.
3. Open the preview URL to review the site on desktop or mobile.
4. Push additional commits to update the preview automatically.

Cloudflare does not provide these Git-integrated previews for fork pull requests.
The existing `Site integrity` check remains required independently of previews.

## Project settings

- Project: `garibong-dev-pr-preview`
- Source: `Hamjoon/hamjoon.github.io`
- Production branch: `main`; automatic production deployments: **disabled**
- Preview branches: **all**
- Pull request comments: **enabled**
- Root directory: repository root
- Output directory: `preview-dist`
- Build command:

  ```sh
  mkdir -p preview-dist && cp index.html style.css 404.html ads.txt app-ads.txt preview-dist/ && cp -R assets cube-serpent preview-dist/
  ```

Only the homepage, supporting assets, ad declarations, error page, and bundled
Cube Serpent game are staged for previews. Legacy standalone chart pages and
historical backups are not included. Repository metadata, CI files, and local
credentials are not staged. No Functions or runtime secrets are configured.

Cloudflare adds a `noindex` response header to preview deployments. Preview URLs
are publicly reachable; `noindex` is not access control.

## Maintenance

Manage these settings in Cloudflare Workers & Pages, not in GitHub Pages or DNS.
The GitHub integration performs deployment without an agent's laptop or a
Cloudflare credential stored in GitHub Actions.

If a new public path is introduced, update the staging command above and the
Cloudflare project build command together. Keep production deployment disabled.

Official references:
- https://developers.cloudflare.com/pages/configuration/git-integration/github-integration/
- https://developers.cloudflare.com/pages/configuration/preview-deployments/
