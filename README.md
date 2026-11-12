# Fusion

Fusion is the superproject that tracks two component repositories as Git submodules:

- [TransFormers-Fusion](https://github.com/origin-labs-ai/transformers) — the C++20 engine.
- [CodeFusion](https://github.com/origin-labs-ai/code) — the Launcher Desktop workspace.

This repository primarily records the selected component revisions. Most source changes should be made in the relevant component repository, then the updated submodule pointer can be committed here.

## Clone

```bash
git clone --recurse-submodules https://github.com/origin-labs-ai/fusion.git
cd fusion
git submodule update --init --recursive
```

If you already cloned without submodules, run the update command from the repository root.

## Contributing

- For engine code, tests and quantization work, contribute in [TransFormers-Fusion](https://github.com/origin-labs-ai/transformers-fusion).
- For launcher or component-registry work, read the contribution scope in [CodeFusion](https://github.com/origin-labs-ai/code-fusion) first.
- For changes to the set of component revisions, open an issue here explaining why the submodule update is needed.

## Licensing

This superproject has no separate top-level license declaration. The component repositories and any third-party material within them may have different licensing terms. Review each component's license and provenance before using or redistributing its contents.
