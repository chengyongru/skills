# Nanobot Gate Report Template

~~~~markdown
## Nanobot Gate Report

**Overall**: PASS/WARN/FAIL/BLOCKED
**Requested terminal state**: local readiness | pre-PR readiness | merge readiness | release readiness
**Change**: <one-line summary>
**PR**: <URL or none>
**Base**: <ref and resolved SHA>
**Candidate ID**: <content fingerprint>
**Local HEAD**: <SHA>
**Remote reviewed head**: <SHA or not applicable>

| Gate | Required | Status | Candidate/remote SHA | Action and evidence | Judgment |
|---|---:|---|---|---|---|
| simplify | yes/no | PASS/WARN/FAIL/BLOCKED/NOT_RUN/STALE | <candidate ID> | <cleanup and evidence> | <contract judgment> |
| verify | yes/no | PASS/WARN/FAIL/BLOCKED/NOT_RUN/STALE | <candidate ID> | <public action, exit/status, evidence> | <pass-rule mapping> |
| candidate-review | yes/no | PASS/WARN/FAIL/BLOCKED/NOT_RUN/STALE | <candidate ID> | <reachability, value, findings> | <local review judgment> |
| pr-review | yes/no | PASS/WARN/FAIL/BLOCKED/NOT_RUN/STALE | <candidate ID + PR SHA> | <metadata, detached worktree, findings> | <review judgment> |
| remote-ci | yes/no | PASS/WARN/FAIL/BLOCKED/NOT_RUN/STALE | <candidate ID + PR SHA> | <required checks and evidence> | <remote readiness judgment> |

### Candidate state

- Snapshot manifest: `<evidence>/gate-state.json`
- Candidate review: <result; explicitly distinguish it from formal PR review>
- Carried results: <gate, previous candidate, new candidate, reason; or none>
- Stale results excluded: <gate and candidate; or none>

### Verification plan

~~~yaml
change_summary: <summary>
terminal_state: <requested terminal state>
required_gates:
  - <gate>
changed_user_surfaces:
  - <surface>
supported_path:
  entrypoint: <public entrypoint>
  changed_boundary: <boundary>
  consequence: <observable consequence>
risks:
  - <risk>
test_tiers:
  focused:
    run_when: always
  public_black_box:
    run_when: changed behavior is user reachable
  broader_local:
    run_when: <risk/policy/escalation condition>
  remote_ci:
    run_when: <publication/terminal-state condition>
tests:
  - id: <stable id>
    concern: <what could break>
    interface: web-ui | api | cli | library | service | other
    action: <exact command or visible action>
    expected_evidence: <observable output/state>
    pass_rule: <explicit rule>
    evidence_target: <path>
    destructive: false
limitations:
  - <limitation or none>
~~~

### Verification Report

- <test/action>: <candidate ID>, <exit/status>, <observable evidence>, <pass rule>, <judgment>

### Differential baseline

| Failed/ambiguous check | Candidate result | Baseline ref/result | Classification | Evidence |
|---|---|---|---|---|
| <check or none> | <result> | <result> | regression/baseline limitation/blocked | <paths> |

### Review

- Value and reachability: <supported path and net value>
- Candidate review: <confirmed findings or none>
- Formal PR review: <reviewed SHA, clean detached worktree, findings or NOT_RUN>

### Confirmed findings

- <impact and location, ordered by severity; or None remaining>

### Risks, questions, and limitations

- <material non-finding or none>

### Publication and CI

- Publication: <none, or each locally ready commit/push/PR handoff>
- GitHub mutations: <complete list, or none>
- Required checks at remote SHA: <states and evidence>

### Cleanup

- <browser/process/port/runtime cleanup and retained artifacts>

### Conclusion

PASS/WARN/FAIL/BLOCKED — <short evidence-backed conclusion for required gates only>

Evidence directory retained at `<path>`. Ask whether it should be deleted.
~~~~
