#!/usr/bin/env python3
"""Generate config.py from YAML + Jinja2 template (CI-compatible, no Docker).

Replicates tpl-gen's context merging: loads YAML, extracts the 'env' section,
and renders the Jinja2 template with StrictUndefined.
"""
import argparse
import pathlib

import jinja2
import yaml


def main():
    parser = argparse.ArgumentParser(
        description="Generate config.py from YAML + Jinja2 template"
    )
    parser.add_argument("--yaml-path", required=True, help="Path to env YAML file")
    parser.add_argument("--tpl-path", required=True, help="Path to Jinja2 template")
    parser.add_argument("--out-path", required=True, help="Output file path")
    args = parser.parse_args()

    with open(args.yaml_path) as f:
        data = yaml.safe_load(f)

    # Extract env context — same as tpl-gen with DATA_KEY_PATH='.'
    ctx = data.get("env", {})

    tpl_text = pathlib.Path(args.tpl_path).read_text()
    env = jinja2.Environment(undefined=jinja2.StrictUndefined)
    tpl = env.from_string(tpl_text)
    output = tpl.render(**ctx)

    pathlib.Path(args.out_path).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(args.out_path).write_text(output)
    print(f"Generated {args.out_path}")


if __name__ == "__main__":
    main()
