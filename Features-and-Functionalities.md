# Features and Functionalities - tpl-gen

This document outlines the core features and functionalities of the `tpl-gen` (Template Generator) project.

## Core Template Engine
- **Jinja2 Rendering:** Utilizes the powerful Jinja2 templating engine to transform abstract configurations into concrete technical files.
- **Python-Based Logic:** A robust Python package (`tpl_gen`) handles the heavy lifting of data loading, template discovery, and rendering.
- **Poetry Integration:** Manages Python dependencies (jinja2, pyyaml, jq, rich) using Poetry for consistent and reproducible execution environments.

## Configuration & Data Handling
- **YAML Source Parsing:** Loads complex YAML configuration files and makes the data available as a context for template rendering.
- **YAML to JSON Conversion:** Automated utility to convert YAML configuration files into JSON format for use by other tools or systems.
- **Data Discovery:** Dynamically discovers `.tpl` files within source directories based on environment and step-specific paths.

## Advanced Templating Features
- **Dynamic Filenaming:** Supports `%placeholder%` keys within template filenames, which are replaced during the generation process to create uniquely named output files.
- **Context Injection:** Injects environment variables (ENV, ORG, APP, STEP) and full configuration data into the Jinja2 context.
- **Flexible Output Mapping:** Renders templates from a source directory (`TPL_SRC`) and writes them to a specific target directory (`TGT`).

## Automated Workflow & Shell Actions
- **Dependency Management:** Integrated shell actions to ensure Poetry and all required Python modules are installed and up-to-date.
- **Module Morphing:** Tools to clone and customize modules with automated search-and-replace capabilities.
- **Packaging Utilities:** `do_zip_me_as_module` for creating distributable ZIP packages of the generated outputs.
- **Scan & List:** Automatically generates include/exclude lists for complex morphing or packaging tasks.

## Orchestration Role
- **Pipeline Integration:** Functions as a critical middle layer in the configuration pipeline: `bnc-cpt-cnf (YAML Source) → tpl-gen (Transformation) → bnc-cpt-inf (Terraform Execution)`.
- **Make-Driven Execution:** Typically invoked via a Makefile in `bnc-cpt-utl` to generate environment-specific configurations on the fly.
