# Third-party notices

The original authors' software remains subject to the repository's component-specific licence. Third-party components retain their own licences.

- `original/jobbert_continuation/pytorch-crf/torchcrf/__init__.py`: pytorch-crf 0.7.2, Copyright 2017 Kemal Kurniawan, MIT. The supplied source matches the upstream source fetched on 2026-10-17 after newline normalization (SHA-256 `3dd1a7f8be203ff3e316e945e5856b87fb7ea6cb4b084024e6b2119cd09fd107`). [Upstream source](https://github.com/kmkurn/pytorch-crf/blob/master/torchcrf/__init__.py); [licence](original/jobbert_continuation/pytorch-crf/LICENSE.txt). The incoming ZIP omitted that licence; it is added alongside the unchanged source.
- The retained MaChAmp diff contains third-party source context and proposed changes to `machamp/data/machamp_sampler.py`. [MaChAmp upstream](https://github.com/machamp-nlp/machamp) is Apache-2.0; a copy of its [licence](original/native_patches/LICENSE-MaChAmp.txt) is included. The diff is truncated and is retained as evidence only, not as an applicable patch. No exact upstream revision or complete server-final MaChAmp tree is certified by this addendum.

Upstream references above identify attribution sources, not immutable training-environment bindings. Native upstream repositories, model weights and datasets must be obtained separately under their respective terms. No third-party recruitment text is added.
