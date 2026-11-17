#!/usr/bin/env node
import { type ChildProcess, spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { parseArgs } from "node:util";
import { messageOf } from "./run.ts";

const USAGE = `Usage: node statechart.ts SPEC.tla [--config FILE] [--view FILE] [--out DIR]
                                      [--timeout SECONDS] [--cancel-file FILE]

Checks SPEC.tla with TLC and draws its state graph as Mermaid. Above 500 states,
only bug paths are drawn; a passing larger model has no chart.mmd.
  --config FILE  Default: SPEC.cfg beside the spec.
  --view FILE    Module exporting state(vars), optionally step, group, colors, title.
  --out DIR      New or empty output folder outside this package. Default: SPEC-chart.
  --timeout SEC  Positive wall-clock budget, at most 86400. Default: 120 seconds.
  --cancel-file  Stop when this task-owned file exists, including without a console.
Requires Python 3.11+ (STATECHART_PYTHON overrides its path), Java 11+, and TLA2TOOLS.
No dependencies are installed automatically. See references/tools.md.
Exit: 0 rules hold; 1 rule breaks; 2 checker/setup error; 124 timeout; 130 cancellation;
143 SIGTERM. Only 0 and 1 publish output. Unchecked rules remain explicit in the report.`;

let stop: NodeJS.Signals | "timeout" | "cancelled" | undefined;
let stopRun: () => void;
const stopped = new Promise<void>((resolve) => {
  stopRun = resolve;
  for (const name of ["SIGINT", "SIGTERM"] as const)
    process.on(name, () => { stop ??= name; resolve(); });
});

let flags;
let specFile;
try {
  const args = parseArgs({
    allowPositionals: true,
    options: {
      config: { type: "string" }, view: { type: "string" }, out: { type: "string" },
      timeout: { type: "string" }, "cancel-file": { type: "string" },
    },
  });
  flags = args.values;
  [specFile] = args.positionals;
  if (args.positionals.length !== 1) throw new Error("Give one SPEC.tla.");
} catch (error) {
  console.error(`${messageOf(error)}\n\n${USAGE}`);
  process.exit(2);
}

const codeOf = (error: unknown) =>
  error instanceof Error && "code" in error ? error.code : undefined;
const packageRoot = (() => {
  for (let dir = import.meta.dirname; ; dir = path.dirname(dir)) {
    if (fs.existsSync(path.join(dir, "plugin.json"))) return fs.realpathSync(dir);
    if (path.dirname(dir) === dir) return fs.realpathSync(path.join(import.meta.dirname, ".."));
  }
})();
const external = (candidate: string) => {
  let ancestor = path.resolve(candidate);
  const tail: string[] = [];
  while (!fs.existsSync(ancestor)) {
    tail.unshift(path.basename(ancestor));
    ancestor = path.dirname(ancestor);
  }
  const resolved = path.join(fs.realpathSync(ancestor), ...tail);
  const relative = path.relative(packageRoot, resolved);
  if (!relative || (!relative.startsWith(`..${path.sep}`) && relative !== ".." && !path.isAbsolute(relative)))
    throw new Error(`Keep output and temporary state outside the immutable plugin package: ${candidate}`);
};

// A Windows venv redirector can create its base interpreter on the interactive
// desktop, and before the owner can assign its Job. The owner uses only stdlib;
// launch the venv's recorded base interpreter directly instead.
const ownerPython = () => {
  const selected = process.env.STATECHART_PYTHON ?? (process.platform === "win32" ? "python" : "python3");
  if (process.platform !== "win32") return selected;
  const candidates = path.isAbsolute(selected) || selected.includes("/") || selected.includes("\\")
    ? [path.resolve(selected)]
    : [process.cwd(), ...(process.env.PATH ?? "").split(path.delimiter)]
      .map((directory) => path.join(directory, selected));
  const executable = candidates.flatMap((file) => [file, `${file}.exe`])
    .find((file) => fs.existsSync(file) && fs.statSync(file).isFile());
  if (!executable) return selected; // spawn reports the missing executable
  const config = path.join(path.dirname(executable), "..", "pyvenv.cfg");
  if (!fs.existsSync(config)) return executable;
  const home = fs.readFileSync(config, "utf8").match(/^home\s*=\s*(.+)$/m)?.[1].trim();
  if (!home) throw new Error(`No base Python home in ${config}. Set STATECHART_PYTHON to a real interpreter.`);
  const base = path.resolve(path.dirname(config), home, "python.exe");
  if (!fs.existsSync(base)) throw new Error(`Cannot find the venv's base Python: ${base}`);
  return base;
};

try {
  const budget = Number(flags.timeout ?? 120);
  if (!Number.isFinite(budget) || budget <= 0 || budget > 86400)
    throw new Error("--timeout must be positive and at most 86400 seconds.");
  const configFile = flags.config ?? specFile.replace(/\.tla$/, ".cfg");
  if (!fs.existsSync(configFile))
    throw new Error(`Cannot find the TLC config ${configFile}. Pass --config FILE.`);
  const out = flags.out ?? specFile.replace(/\.tla$/, "-chart");
  let entries: string[] = [];
  let dest: string;
  try {
    entries = fs.readdirSync(out);
    dest = fs.realpathSync(out);
  } catch (error) {
    if (codeOf(error) !== "ENOENT")
      throw new Error(`${out} cannot be the output folder. ${messageOf(error)}. Pass --out with a new folder.`);
    if (fs.lstatSync(out, { throwIfNoEntry: false }))
      throw new Error(`${out} cannot be the output folder. It is a broken link. Pass --out with a new folder.`);
    dest = path.resolve(out);
  }
  if (entries.length)
    throw new Error(`${out} is not empty. It has ${entries.sort()[0]}. The command writes only to a new or empty folder. Pass --out with a new folder.`);
  external(dest);
  external(os.tmpdir());
  let base = path.dirname(dest);
  while (!fs.existsSync(base)) base = path.dirname(base);
  const stage = fs.mkdtempSync(path.join(base, `.${path.basename(dest)}.statechart-`));
  const done = path.join(stage, "done");
  let tmp: string | undefined;
  let owner: ChildProcess | undefined;
  let ownerExited: Promise<number> | undefined;
  let timer: NodeJS.Timeout | undefined;
  let cancel: NodeJS.Timeout | undefined;
  let exitCode = 2;
  try {
    tmp = fs.mkdtempSync(path.join(os.tmpdir(), "statechart-"));
    const runtime = process.versions.deno
      ? ["run", "--quiet", "--no-prompt", "--allow-read", "--allow-write", "--allow-run", "--allow-env"]
      : process.execArgv;
    owner = spawn(
      ownerPython(),
      ["-B", path.join(import.meta.dirname, "owned-process.py"), stage, tmp,
        process.execPath, ...runtime, path.join(import.meta.dirname, "worker.ts"),
        stage, specFile, configFile, ...(flags.view ? [flags.view] : [])],
      // On Windows, libuv kills non-detached children when this CLI dies. Keep
      // the hidden owner alive to observe EOF, stop its Job, and remove scratch.
      { detached: true, windowsHide: true, stdio: ["pipe", "pipe", "pipe"],
        env: { ...process.env, TMPDIR: tmp, TMP: tmp, TEMP: tmp, STATECHART_COMMAND_PID: String(process.pid) } },
    );
    owner.stderr!.pipe(process.stderr);
    ownerExited = new Promise<number>((resolve) => {
      owner!.on("error", (error) => { console.error(messageOf(error)); resolve(2); });
      owner!.on("close", (code) => resolve(code ?? 2));
    });
    const checked = new Promise<number>((resolve) => {
      let text = "";
      owner!.stdout!.on("data", (data) => {
        text += String(data);
        if (text.includes("\n")) {
          try { resolve(JSON.parse(text.slice(0, text.indexOf("\n"))).exit); }
          catch { resolve(2); }
        }
      });
      ownerExited!.then(() => resolve(2));
    });
    timer = setTimeout(() => { stop = "timeout"; stopRun(); }, budget * 1000);
    if (flags["cancel-file"]) {
      const file = path.resolve(flags["cancel-file"]);
      cancel = setInterval(() => {
        if (fs.existsSync(file)) { stop = "cancelled"; stopRun(); }
      }, 50);
    }
    const verdict = await Promise.race([stopped.then(() => 2), checked]);
    clearTimeout(timer);
    clearInterval(cancel);
    if (stop) {
      console.error(`${stop} stopped the check, so the command wrote nothing.`);
      exitCode = stop === "timeout" ? 124 : stop === "cancelled" ? 130 : 128 + os.constants.signals[stop];
    } else if ((verdict === 0 || verdict === 1) && fs.existsSync(done)) {
      fs.mkdirSync(path.dirname(dest), { recursive: true });
      try {
        if (process.platform === "win32" && fs.existsSync(dest)) fs.rmdirSync(dest);
        fs.renameSync(done, dest);
      } catch (error) {
        if (codeOf(error) !== "ENOTEMPTY" && codeOf(error) !== "EEXIST") throw error;
        throw new Error(`${path.join(out, fs.readdirSync(dest).sort()[0])} appeared while the check ran, so the command wrote nothing. Pass --out with a new folder.`);
      }
      process.stdout.write(fs.readFileSync(path.join(dest, "report.md")));
      console.log(`\nWrote ${out}`);
      exitCode = verdict;
    }
  } finally {
    clearTimeout(timer);
    clearInterval(cancel);
    owner?.stdin?.end();
    if (ownerExited && await ownerExited !== 0) exitCode = 2;
    fs.rmSync(stage, { recursive: true, force: true });
    if (tmp) fs.rmSync(tmp, { recursive: true, force: true });
  }
  process.exit(exitCode);
} catch (error) {
  console.error(messageOf(error));
  process.exit(2);
}
