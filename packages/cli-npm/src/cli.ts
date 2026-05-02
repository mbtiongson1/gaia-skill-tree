/**
 * CLI utilities for Gaia
 */

import { spawn } from 'child_process';
import { existsSync } from 'fs';
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';

export async function runGaiaCli(args: string[]): Promise<number> {
  return new Promise((resolveExitCode) => {
    const __filename = fileURLToPath(import.meta.url);
    const __dirname = dirname(__filename);
    const packageRoot = resolve(__dirname, '..');
    const repoRoot = resolve(packageRoot, '../..');
    const pythonCliPath = existsSync(resolve(packageRoot, 'cli/main.py'))
      ? resolve(packageRoot, 'cli/main.py')
      : resolve(repoRoot, 'packages/cli-npm/cli/main.py');

    const env = {
      ...process.env,
      PYTHONPATH: [resolve(packageRoot, 'src'), resolve(repoRoot, 'src'), repoRoot, packageRoot, process.env.PYTHONPATH].filter(Boolean).join(':'),
    };

    const pythonProcess = spawn('python3', [pythonCliPath, ...args], {
      stdio: 'inherit',
      env,
    });

    pythonProcess.on('exit', (code) => {
      resolveExitCode(code || 0);
    });

    pythonProcess.on('error', (error) => {
      console.error('Failed to run Gaia CLI:', error.message);
      resolveExitCode(1);
    });
  });
}
