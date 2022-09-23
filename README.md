# tpl-gen

## INTRO & RATIONALE
One of the crucial factors in the success of your IT project is the level of segregation between your source code and your configuration. 

Ideally you would : 
- have a clear undertanding on your operational environments - local , development, testing , quality assurance production etc.
- have a clean and lean naming convention, not only for your environments, but for the majority of objects in them ...
- have the configuration in a central directory, with each environment in it's own units

Ideally you would NOT: 
- mix configuration entries in your source code - this is ALWAYS disaster and advances silosing in your projects
- input manually confgiration for each run-time for each environments, have your configuration ALL OVER the places ...
- 

## TPL-GEN - WHAT IS THIS ?!
A template generator following the OAE IT Systems configurability model. OAE stands for : 
- Organisation
- Application
- Environment

The model defines and operating IT environment, based on those 3 attributes. It is a simple, but powerful realization of the fact that each IT environment belongs to : 
- at least 1 Organisation ( and preferably there should be 1 Organisation being responsible for it )
- 1..1 Application from an IT System / Architecture / Operational Perspective
- 1..1 Environment - as by definition and IT Best Practices the environments must be segregated



## SETUP & INSTALL
Read Carefully and follow these instructions - there is a single one-liner to setup the project, BUT should yo
## Pre-requesites
You should have the following binaries natively - bash, make, perl, jq, docker, sed. 

``` ATTENTION !!! ```bash
It IS REALLY IMPORTANT to ensure that the directly where you clone the  `tpl-gen` is: 
- the same dir where your project having the templates residues
- owned and read/writable by your native OS user and group 
- configured in your Docker configuration to be a shared volume !!!

Should ANY of those ^^^ you might not be able to use the `tpl-gen` for other projects !!!
Thus bellow is the recommended way of deploying the `tpl-gen`:

## GET THE SOURCE
You MUST clone this project on base directory containing your target project containing the `*.tpl` files to generate the configuration from. To avoid any file permissions errors use a conventional dir to clone the project into.
```bash
# ~/opt/ is just a convention, but does match the ^^^ requirements !!! 
# So make sure you add it to your Docker volumes 
mkdir -p ~/opt/ ; cd $_ 
git clone git@github.com:csitea/tpl-gen.git
cd ~/opt/tpl-gen
find . | sort | less
```

## CHECK THE USAGE
The make is usually used for oneliners to deploy / install project components
```bash
make
```

The `./run` is usually used for oneliners to run quick actions
```bash
./run --help



```

### SETUP DOCKER ENVIRONMENT
The tpl-gen docker has all the needed binaries create configuration files from templates.
```bash
# always go to the project root dir - aka the product dir
cd ~/opt/tpl-gen

make clean-install-tpl-gen                                   # install without reusing layers
make install-tpl-gen                                         # install from cached layers (faster)
make install                                                 # install without reusing layers
```

### CONFIGURE THE TGT PROJECT
You call the tpl-gen "against" another projects by just passing the name of the target project root directrory. It IS obligatory for both project the tgl-gen and the target project to generate the templates for to be in the same directory (usually $HOME/opt )

```bash 
# generate the templates 
ORG=org APP=app ENV=dev make do-tpl-gen                      # renders from /var/infra/src/tpl/cnf  into directory replacing wildcards %var%
ORG=org APP=app ENV=dev TGT=tmp make do-tpl-gen              # renders from /var/infra/src/tpl/cnf  into /var/tmp
ORG=org APP=app ENV=dev SRC=csitea TGT=tmp make do-tpl-gen   # renders from /var/csitea/src/tpl/cnf into /var/tmp
```

Typical ORG-APP-ENV set of files would look like this:
```bash

~/opt/<<target-project>>/cnf/env/<<org>>/<app>>/all.env.yaml
~/opt/<<target-project>/cnf/env/<<org>>/<app>>/dev.env.yaml
~/opt/<<target-project>/cnf/env/<<org>>/<app>>/prd.env.yaml
~/opt/<<target-project>/cnf/env/<<org>>/<app>>/tst.env.yaml

```
for example:

```bash

~/opt/infra/cnf/env/spe/nba/all.env.yaml
~/opt/infra/cnf/env/spe/nba/dev.env.yaml
~/opt/infra/cnf/env/spe/nba/prd.env.yaml
~/opt/infra/cnf/env/spe/nba/stg.env.yaml
~/opt/infra/cnf/env/spe/nba/tst.env.yaml

```
The configuration files are plain yaml files - check the tpl-gen own configuration files ( they are just copy paste example )

### USAGE
You call the tpl-gen `"against"` another projects by just passing the name of the target project root directrory. It IS obligatory for both project the tgl-gen and the target project to generate the templates for to be in the same directory (usually $HOME/opt )

```bash

# call the tpl-gen against the infra project for the csi organisation, htr application and dev environment
ORG=csi APP=htr ENV=dev TGT=infra make do-tpl-gen

# specify where to get the configuration from ( the default is "infra")
# specify where to generate the configuration files, produced from the templates
```bash
ORG=csi APP=htr ENV=dev SRC=infra TGT=htr-api make do-tpl-gen;
```

# call the tpl-gen against the infra project for all the environments
for env in `echo dev tst stg prd all`; do ORG=csi APP=htr ENV=$env SRC=infra TGT=infra make do-tpl-gen; done
for env in `echo dev tst stg prd all`; do ORG=csi APP=htr ENV=$env SRC=infra TGT=htr-api make do-tpl-gen; done
```


