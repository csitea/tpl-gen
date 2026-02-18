# CLAUDE.md - tpl-gen

Jinja2 template generator — renders YAML configuration into technical output files (tfvars, JSON, etc.).

## MANDATORY: Shell Actions First

**This project has a `src/bash/run/run.sh` and `*.func.sh` files — "shell actions" (bash functions that automate tasks).** Before starting ANY task, you MUST:

1. **Check if a shell action already exists** by running:
   ```bash
   SRCH=<keyword> ./run -a do_help_with
   ```

2. **If a shell action exists — USE IT.** Do not reinvent the wheel. Do not run raw commands when a shell action already wraps that operation.

3. **If no shell action exists** for what you need to do, proceed manually — but consider whether a new shell action should be created for it.

The shell action framework is how this project automates everything. By always using shell actions, the codebase gets continuously tested and enlarged. Each `*.func.sh` file contains a `do_*` function invoked via `./run -a do_action_name`. Use `SRCH=<keyword> ./run -a do_help_with` to search for relevant actions by keyword.

## MANDATORY: Run as ysg User

**Claude Code runs as `claude-user`, but ALL shell actions, tests, and project commands MUST be executed as `ysg` user.** The project is set up for `ysg` first — `claude-user` is a secondary automation user.

Always use `sudo -u ysg` to run commands:
```bash
# Shell actions
sudo -u ysg bash -c 'cd /opt/csi/csi-web/csi-web-utl && ./run -a do_action_name'

# npm / node commands
sudo -u ysg bash -c 'cd /opt/csi/csi-web/csi-web-wui/src/nodejs/the-bot && ORG=csi APP=web ENV=dev npm test'

# Git operations
sudo -u ysg git -c safe.directory=/opt/csi/csi-web/<repo> -C /opt/csi/csi-web/<repo> status
```

**Why:** File ownership is `ysg:ysg`, Chrome/Puppeteer cache is under `/home/ysg`, KeePassXC credentials are at `/home/ysg/.ssh/.csi/`, and GCP keys are at `/home/ysg/.gcp/.csi/`. Running as `ysg` ensures all paths resolve correctly.

## Team / *nix Users

This project is used by multiple developers. Use `$USER` instead of hardcoded usernames:
- **ysg** — Yordan Stanchev Georgiev
- **petri** — Petri

## Directory Structure

```
tpl-gen/
├── run -> src/bash/run/run.sh       # Entrypoint symlink
├── src/
│   ├── bash/run/                    # 15 shell action files (*.func.sh)
│   └── python/tpl-gen/              # Main Python package
│       ├── tpl_gen/
│       │   ├── tpl_gen.py           # Main entry point
│       │   ├── run_env.py           # Environment config singleton
│       │   ├── config_data_loader.py
│       │   ├── convert_yaml_to_json.py
│       │   └── libs/utils/          # Utility modules
│       ├── pyproject.toml           # Poetry dependencies
│       └── poetry.lock
├── lib/bash/funcs/                  # 23 utility library functions
├── cnf/lst/                         # Include/exclude lists
└── Makefile
```

## Template Processing Flow

```
YAML config (CNF_SRC)  →  Jinja2 templates (TPL_SRC)  →  Output files (TGT)
  dev.env.yaml              *.vars.tfvars.tpl              dev/tf/*.vars.tfvars
```

The Python engine:
1. Loads YAML configuration from `CNF_SRC`
2. Discovers `.tpl` template files from `TPL_SRC`
3. Renders templates via Jinja2 with config as context
4. Replaces `%placeholder%` keys in filenames
5. Writes output to `TGT` directory
6. Also converts YAML configs to JSON format

## Key Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `ENV` | Target environment | `dev`, `tst`, `prd` |
| `ORG` | Organization code | `csi` |
| `APP` | Application code | `web` |
| `TPL_SRC` | Template source directory | `/opt/csi/csi-web/csi-web-inf` |
| `CNF_SRC` | Configuration source | `/opt/csi/csi-web/csi-web-cnf/csi-web` |
| `TGT` | Output target directory | `/opt/csi/csi-web/csi-web-cnf/csi-web` |
| `STEP` | Terraform step name | `029-create-gcp-secrets` |

## Shell Actions

```bash
./run -a do_check_install_py_modules   # Install Python deps via Poetry
./run -a do_check_install_poetry       # Ensure Poetry is installed
./run -a do_morph_module               # Clone and customize a module
./run -a do_scan_to_list_file          # Generate include/exclude lists
./run -a do_zip_me_as_module           # Package as distributable zip
./run -a do_help_with                  # Search actions (SRCH=keyword)
```

## Python Dependencies

Key packages (managed by Poetry in `src/python/tpl-gen/`):
- **jinja2** — Template rendering
- **pyyaml** — YAML parsing
- **jq** — JSON query/transformation
- **rich** — Terminal output formatting

## Typical Usage

Template generation is usually triggered from `csi-web-utl` via Make:

```bash
cd /opt/csi/csi-web/csi-web-utl
make do-generate-config-for-step ENV=dev STEP=029-create-gcp-secrets
```

## Related Paths

- CNF (config source): `/opt/csi/csi-web/csi-web-cnf`
- INF (template source): `/opt/csi/csi-web/csi-web-inf`
- UTL (orchestrator): `/opt/csi/csi-web/csi-web-utl`
