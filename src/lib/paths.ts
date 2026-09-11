const BASE_PATH = import.meta.env.BASE_URL ?? '/';

export function resolvePath(path: string) {
  const base = BASE_PATH.endsWith('/') ? BASE_PATH.slice(0, -1) : BASE_PATH;
  const clean = path.startsWith('/') ? path : `/${path}`;
  const joined = `${base}${clean}`.replace(/\/+/g, '/');
  return joined === '' ? '/' : joined;
}
