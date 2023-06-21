#!/bin/bash

# This itself is handy to be on your bashrc, but theres room for improvement 
# and extra functions in here
function oae() {
    for org_option in $(find cnf/env -maxdepth 1 -type d); do
        org=$(basename ${org_option})

        if [[ "${org}" != "env" && "${org}" != "sample-org" ]]; then
            for app_option in $(find cnf/env/${org} -maxdepth 1 -type d); do
                app=$(basename ${app_option})
                
                if [[ "${app}" != "${org}" ]]; then
                    for env_option in $(find cnf/env/${org}/${app} -maxdepth 1 -type d); do
                        env=$(basename ${env_option})

                        if [[ "${env}" != "${app}" ]]; then
                            echo "ORG=${org} APP=${app} ENV=${env} make"
                        fi
                    done;
                fi
            done
        fi
    done
}