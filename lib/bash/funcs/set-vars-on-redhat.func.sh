#!/bin/bash


do_set_vars_on_redhat() {
  # Define RHEL 9-specific variables
  export OS_RELEASE="RHEL 9"
  export PACKAGE_MANAGER="dnf"
  export SYSTEMD_SERVICE_DIR="/etc/systemd/system"
  export DEFAULT_SHELL="/bin/bash"

  # Set any RHEL 9-specific environment variables or defaults
  export PATH="$PATH:/usr/local/bin:/usr/bin:/bin"
  export LD_LIBRARY_PATH="/usr/local/lib:/usr/lib:/lib:$LD_LIBRARY_PATH"

  # Log the RHEL 9 environment setup
  do_log "INFO Setting up environment for $OS_RELEASE"
}
