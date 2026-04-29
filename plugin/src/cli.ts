/**
 * CLI utilities for Gaia
 */

import { spawn } from 'child_process';

export async function runGaiaCli(args: string[]): Promise<number> {
  return new Promise((resolve) => {
    const pythonProcess = spawn('python3', ['cli/main.py', ...args], {
      stdio: 'inherit',
    });

    pythonProcess.on('exit', (code) => {
      resolve(code || 0);
    });

    pythonProcess.on('error', (error) => {
      console.error('Failed to run Gaia CLI:', error.message);
      resolve(1);
    });
  });
}
