# ESCOXLM-R transformer_model patch

Official configs hard-code `~/escoxlmr/xlm-experiment-combined-1e-5-128-30k/checkpoint-30000/`.
That local MLM+ERP checkpoint is not on this server.

Replacement: Hugging Face `jjzha/esco-xlm-roberta-large` revision `8093cc37ac619a25c5166355acba7be878eb6402`.
Do not treat `xlmr-mlm` as MLM+ERP.

Copied patched configs: patches/escoxlmr_configs/
