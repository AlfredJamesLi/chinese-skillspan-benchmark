# Chain status 2026-09-08T14:15:06+08:00

- slurm: 
- qwen42 selected: yes
- qwen43 selected: yes
- qwen44 selected: no
- qwen42 gold: no
- qwen43 gold: no
- qwen44 gold: no
- hem scores: 0
- results: no
- gpu 0, 17109 MiB, 99 %
- gpu 1, 17149 MiB, 99 %
- gpu 2, 0 MiB, 0 %
- gpu 3, 0 MiB, 0 %
- gpu 4, 0 MiB, 0 %
- gpu 5, 0 MiB, 0 %
- gpu 6, 3 MiB, 0 %
- gpu 7, 3 MiB, 0 %

## latest train lines
### seed42
{'loss': '0.0815', 'grad_norm': '0.7151', 'learning_rate': '1.358e-06', 'epoch': '5.93'}
{'loss': '0.08741', 'grad_norm': '0.569', 'learning_rate': '1.235e-07', 'epoch': '6'}
100%|██████████| 810/810 [40:01<00:00,  1.37s/it]{"epoch": 6, "typed_exact_f1": 0.15331010452961674, "typed_relaxed_f1": 0.49128919860627174, "alignment_ok": true, "scorer_version": "cnss-lskt-1.2.0", "n_dev": 169, "parse_nonempty_or_empty_ok": 169}
{'train_runtime': '2595', 'train_samples_per_second': '4.971', 'train_steps_per_second': '0.312', 'train_loss': '0.1368', 'epoch': '6'}
{"done": true, "selected_epoch": 6, "dev_A_f1": 0.15331010452961674}
### seed43
{'loss': '0.08089', 'grad_norm': '0.8941', 'learning_rate': '1.358e-06', 'epoch': '5.93'}
{'loss': '0.07124', 'grad_norm': '1.027', 'learning_rate': '1.235e-07', 'epoch': '6'}
100%|██████████| 810/810 [39:30<00:00,  1.39s/it]{"epoch": 6, "typed_exact_f1": 0.147008547008547, "typed_relaxed_f1": 0.46153846153846156, "alignment_ok": true, "scorer_version": "cnss-lskt-1.2.0", "n_dev": 169, "parse_nonempty_or_empty_ok": 169}
{'train_runtime': '2572', 'train_samples_per_second': '5.016', 'train_steps_per_second': '0.315', 'train_loss': '0.1381', 'epoch': '6'}
{"done": true, "selected_epoch": 6, "dev_A_f1": 0.147008547008547}
JOB_GONE
