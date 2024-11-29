#TPL-GEN 

The template generator. 
Reads YAML files and generates technical files, according to it's Jinja templates ...
Aka "yet another pulautin" ... 


```bash

# run from the infra-conf project
 for env in `echo dev stg prd all`; do export STEP=210-compute-instances; ORG=ilm APP=opa ENV=$env TPL_SRC=/opt/ilm/ilm-opa/ilm-opa-inf  make -C ../ilm-opa-utl do-generate-config-for-step; done ;
>>>>>>> 0b51a8c (init)
```
