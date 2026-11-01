/** Resolve every public resource against Vite's deployment base (including Pages subpaths). */
export function assetUrl(path: string): string {
  return import.meta.env.BASE_URL + path.replace(/^\/+/, '')
}
