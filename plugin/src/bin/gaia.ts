#!/usr/bin/env node

import { spawn, spawnSync } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';
import { existsSync } from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Path to the Python CLI entry point and repo root
const packageRoot = resolve(__dirname, '../..');
const repoRoot = resolve(packageRoot, '..');
const packagedPythonCliPath = resolve(packageRoot, 'cli/main.py');
const repoPythonCliPath = resolve(repoRoot, 'plugin/cli/main.py');
const pythonCliPath = existsSync(packagedPythonCliPath)
  ? packagedPythonCliPath
  : repoPythonCliPath;

// Check if Python CLI exists
if (!existsSync(pythonCliPath)) {
  console.error(`Error: Gaia Python CLI not found at ${pythonCliPath}`);
  process.exit(1);
}

// Find Python executable
let pythonExecutable = 'python3';

// Try to detect Python availability
const detectPython = (): string => {
  for (const python of ['python3', 'python']) {
    const result = spawnSync(python, ['-V'], { 
      stdio: 'pipe',
      shell: false,
    });
    if (result.status === 0 || result.stderr?.toString().includes('Python')) {
      return python;
    }
  }
  
  throw new Error(
    'Python 3 not found. Please install Python 3.8+ to use the Gaia CLI.\n' +
    'Visit: https://www.python.org/downloads/'
  );
};

try {
  pythonExecutable = detectPython();
} catch (error) {
  console.error((error as Error).message);
  process.exit(1);
}

// Prepare environment variables
const env = {
  ...process.env,
  PYTHONPATH: [repoRoot, packageRoot, process.env.PYTHONPATH].filter(Boolean).join(':'),
};

// Spawn Python process with forwarded arguments (no shell for security)
const pythonProcess = spawn(pythonExecutable, [pythonCliPath, ...process.argv.slice(2)], {
  stdio: 'inherit',
  env,
});

// Forward exit code
pythonProcess.on('exit', (code) => {
  process.exit(code || 0);
});

// Handle errors
pythonProcess.on('error', (error) => {
  console.error('Failed to start Gaia CLI:', error.message);
  process.exit(1);
});
