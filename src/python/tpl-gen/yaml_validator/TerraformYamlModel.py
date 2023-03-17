from typing import List, Optional
from pydantic_yaml import YamlModel


class Aws(YamlModel):
    AWS_SHARED_CREDENTIALS_FILE: str
    AWS_CONFIG_FILE: str
    AWS_PROFILE: str
    AWS_REGION: str


class DNS(YamlModel):
    tld_domain: str
    aws_subdomain: Optional[str]
    fqn_aws_subdomain: str
    env_subdomain: str
    fqn_env_subdomain: str


class App(YamlModel):
    domain: str
    subdomain: Optional[str]
    url: str


class RDS(YamlModel):
    dbs: List[str]


class Versions(YamlModel):
    infra_version: str
    terraform_version: str


class Env(YamlModel):
    ENV: str
    ORG: str
    APP: str
    app: App
    DNS: DNS
    RDS: RDS
    github_owner_org: str
    github_repository: str
    versions: Versions
    aws: Aws
    steps: dict


class TerraformYamlModel(YamlModel):
    env: Env
