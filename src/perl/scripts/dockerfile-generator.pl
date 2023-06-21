#!/usr/bin/perl

use strict;
use warnings;

# Get the list of function names and the module name from command-line arguments
my $module_name = shift @ARGV;
my @func_names = @ARGV;

# Directory where Dockerfiles are located
my $docker_dir = 'lib/docker/tpl-gen/x86_64/';

# Output directory for the final Dockerfile
my $output_dir = 'src/docker/' . $module_name . '/';

# Create the output directory if it doesn't exist
mkdir $output_dir unless -d $output_dir;

# Output file name for the final Dockerfile
my $output_file = $output_dir . 'Dockerfile';

# Open the output file in write mode
open(my $fh, '>', $output_file) or die "Could not open file '$output_file' $!";

# Iterate over each function name
foreach my $func_name (@func_names) {
    my $dockerfile = $docker_dir . $func_name ;

    # Check if the Dockerfile exists for the given function name
    if (-e $dockerfile) {
        # Read the contents of the Dockerfile
        open(my $dfh, '<', $dockerfile) or die "Could not open file '$dockerfile' $!";
        my @contents = <$dfh>;
        close($dfh);

        # Remove the first line unless it has "01" in its name
        if ($dockerfile !~ /01/) {
            shift @contents;
        }

        # Write the contents to the output file
        print $fh @contents;
        print $fh "\n\n";
    } else {
        print "Dockerfile not found for function: $func_name\n";
    }
}

# Close the output file
close($fh);

# Print a message with the location of the final Dockerfile
print "Final Dockerfile created: $output_file\n";
