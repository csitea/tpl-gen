

```bash

# run from the infra-conf project
export STEP=121-hts-gcp-wpp-vm; ORG=hts APP=wpp ENV=dev TPL_SRC=/opt/hts/hts-wpp-infra-app/ SRC=/opt/hts/hts-wpp-infra-conf TGT=/opt/hts/hts-wpp-infra-app/ make do-generate-conf-for-step

```