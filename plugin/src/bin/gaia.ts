#!/usr/bin/env node

import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';
import { existsSync } from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Path to the Python CLI entry point
const pythonCliPath = resolve(__dirname, '../../cli/main.py');

// Check if Python CLI exists
if (!existsSync(pythonCliPath)) {
  console.error(`Error: Gaia Python CLI not found at ${pythonCliPath}`);
  process.exit(1);
}

// Find Python executable
let pythonExecutable = 'python3';

// Try to detect Python availability
const detectPython = (): string => {
  const { spawnSync } = require('child_process');
  
  for (const python of ['python3', 'python']) {
    const result = spawnSync(python, ['--version'], { 
      stdio: 'pipe',
      shell: true 
    });
    if (result.status === 0) {
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

// Spawn Python process with forwarded arguments
const pythonProcess = spawn(pythonExecutable, [pythonCliPath, ...process.argv.slice(2)], {
  stdio: 'inherit',
  shell: true
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
