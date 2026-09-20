# Aegis

[![tests](https://github.com/novesteria/lunas/actions/workflows/test.yml/badge.svg)](https://github.com/novesteria/lunas/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/aegis-validator)](https://pypi.org/project/aegis-validator/)
[![Python](https://img.shields.io/pypi/pyversions/aegis-validator)](https://pypi.org/project/aegis-validator/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](./LICENSE)

A deterministic validator for AI-generated code. Apache 2.0.

## What it does

`aegis check ./path` runs a 21-layer pipeline against a directory of
code and reports whether the validation passes. Layers cover AST
parsing, import resolution, cross-file consistency, package install,
type check, test execution, design-brief fidelity, and feature
coverage. 19 layers are deterministic (no model call); 2 are hybrid
(an LLM verdict with a deterministic override): `design_fidelity` and
`feature_coverage`.

## Install

```
pip install aegis-validator
```

The Anthropic SDK is an optional extra for the LLM-using layers:

```
pip install "aegis-validator[anthropic]"
```

Or from source:

```
git clone https://github.com/novesteria/lunas.git
cd aegis
pip install -e .
```

## Quick start

```
aegis check ./my-code                          # deterministic + LLM
aegis check ./my-code --no-llm                 # deterministic only
aegis check ./my-code --brief brief.json       # include design / feature layers
aegis check ./my-code --json report.json       # machine-readable report
aegis check ./my-code --exit-on-fail           # exit 1 on FAIL
```

The LLM-using layers (`design_fidelity`, `feature_coverage`) skip
unless an `ANTHROPIC_API_KEY` is set and a `brief.json` is supplied.

## What a run looks like

A static page whose JavaScript wires a `#clear` button that does not
exist in the HTML. Five applicable layers pass, one fails, the rest
skip because they target other stacks:

```
$ aegis check ./notes --no-llm --verbose
FAIL · 5 passed · 1 failed · 15 skipped · 0.0s · first failure: html_js_id_parity — 1 JS id reference(s) have no matching id in any HTML file
  · python_imports                      stack mismatch: ['static_html']
  ✓ css_completeness                    All 1 CSS file(s) contain real rules, directives, or custom properties
  ✓ ast_brace_balance                   All 1 JS/TS file(s) have balanced brackets
  ✓ static_imports                      All relative imports / script srcs resolve (2 file(s) scanned)
  ✗ html_js_id_parity                   1 JS id reference(s) have no matching id in any HTML file
  ✓ interactivity                       1 interactive element(s) in HTML, 2 event binding(s) in JS/HTML
  ✓ js_syntax                           node --check passed for 1 file(s)
  · npm_install                         stack mismatch: ['static_html']
  · design_fidelity                     No design brief (or empty brief) — nothing to judge
  · feature_coverage                    No design brief — no feature contract to verify
```

Every applicable layer reports its own verdict; the final result is the
conjunction. `--json report.json` writes the same information as
machine-readable output. Exit code is 0 unless `--exit-on-fail` is set.

## Layers

See [`docs/LAYER_INDEX.md`](./docs/LAYER_INDEX.md) for the full list
of layers, their kinds (deterministic / hybrid), and the
file under `aegis/checks/` that implements each one.

## Benchmark

`aegis-bench/` contains a cohort of reproducible cases. Each case has
a `brief.json`, an `input/` directory, an `expected.json` describing
the validator output, and a short technical README.

```
python -m aegis_cli check aegis-bench/cohort/<case>/input \
    --brief aegis-bench/cohort/<case>/brief.json \
    --no-llm
```

See [`aegis-bench/METHODOLOGY.md`](./aegis-bench/METHODOLOGY.md) for
case structure and reproducibility rules.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

[Apache License 2.0](./LICENSE).

## Maintainer

Aegis is maintained by [Novesteria](https://novesteria.com).
Contact: [hello@novesteria.com](mailto:hello@novesteria.com).
