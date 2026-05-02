import { getCached, getEtag, putCache } from "../config/cache.js";
import type { GaiaGraph } from "./types.js";

const REGISTRY_URL =
  "https://raw.githubusercontent.com/mbtiongson1/gaia-skill-tree/main/registry/gaia.json";

const USERNAME_RE = /^[a-zA-Z0-9][a-zA-Z0-9-]{0,37}[a-zA-Z0-9]$|^[a-zA-Z0-9]$/;

let cachedGraph: GaiaGraph | null = null;

export async function loadGraph(registryUrl?: string): Promise<GaiaGraph> {
  const url = registryUrl ?? REGISTRY_URL;
  const cacheKey = "gaia_graph";

  const cached = getCached(cacheKey);
  if (cached && !cached.stale) {
    if (!cachedGraph) {
      cachedGraph = JSON.parse(cached.data);
    }
    return cachedGraph!;
  }

  const headers: Record<string, string> = {
    Accept: "application/json",
  };

  const etag = getEtag(cacheKey);
  if (etag) {
    headers["If-None-Match"] = etag;
  }

  try {
    const res = await fetch(url, { headers });

    if (res.status === 304 && cached) {
      cachedGraph = JSON.parse(cached.data);
      return cachedGraph!;
    }

    if (!res.ok) {
      if (cached) {
        cachedGraph = JSON.parse(cached.data);
        return cachedGraph!;
      }
      throw new Error(`Failed to fetch registry: ${res.status}`);
    }

    const data = await res.text();
    const newEtag = res.headers.get("etag") ?? "";
    putCache(cacheKey, data, newEtag);
    cachedGraph = JSON.parse(data);
    return cachedGraph!;
  } catch (err) {
    if (cached) {
      cachedGraph = JSON.parse(cached.data);
      return cachedGraph!;
    }
    throw err;
  }
}

export async function loadUserTree(
  username: string,
  registryUrl?: string
): Promise<Record<string, unknown> | null> {
  if (!USERNAME_RE.test(username)) return null;
  const baseUrl = registryUrl ?? REGISTRY_URL.replace("/registry/gaia.json", "");
  const url = `${baseUrl}/skill-trees/${encodeURIComponent(username)}/skill-tree.json`;

  try {
    const res = await fetch(url);
    if (!res.ok) return null;
    return (await res.json()) as Record<string, unknown>;
  } catch {
    return null;
  }
}
