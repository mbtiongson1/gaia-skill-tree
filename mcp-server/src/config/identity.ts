import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";
import type { GaiaConfig } from "../graph/types.js";

export function resolveIdentity(): string | null {
  if (process.env.GAIA_USER) {
    return process.env.GAIA_USER;
  }

  const localConfig = join(process.cwd(), ".gaia", "config.json");
  if (existsSync(localConfig)) {
    try {
      const config: GaiaConfig = JSON.parse(readFileSync(localConfig, "utf-8"));
      if (config.gaiaUser) return config.gaiaUser;
    } catch {}
  }

  const globalConfig = join(homedir(), ".gaia", "config.json");
  if (existsSync(globalConfig)) {
    try {
      const config: GaiaConfig = JSON.parse(readFileSync(globalConfig, "utf-8"));
      if (config.gaiaUser) return config.gaiaUser;
    } catch {}
  }

  return null;
}

export function resolveRegistryUrl(): string | null {
  const localConfig = join(process.cwd(), ".gaia", "config.json");
  if (existsSync(localConfig)) {
    try {
      const config: GaiaConfig = JSON.parse(readFileSync(localConfig, "utf-8"));
      if (config.gaiaRegistryRef) return config.gaiaRegistryRef;
    } catch {}
  }
  return null;
}
