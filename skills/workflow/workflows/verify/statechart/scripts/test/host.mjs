// Keep native test subprocesses off the interactive desktop. No result or
// timing behavior is mocked; the real Node/Java/Python commands still run.
import childProcess from "node:child_process";
import { syncBuiltinESMExports } from "node:module";

for (const name of ["spawn", "spawnSync", "execFileSync"]) {
  const original = childProcess[name];
  childProcess[name] = (file, args, options) => {
    if (Array.isArray(args)) return original(file, args, { windowsHide: true, ...options });
    return original(file, { windowsHide: true, ...args });
  };
}
syncBuiltinESMExports();
