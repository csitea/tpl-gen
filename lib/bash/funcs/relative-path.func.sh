do_relative_path() {
    if [[ $# -ne 2 ]]; then
        echo "Usage: relative_path <source_path> <target_path>"
        return 1
    fi

    source_path=$(readlink -f "$1")
    target_path=$(readlink -f "$2")

    if [[ ! -e "$source_path" ]]; then
        echo "Error: Source path does not exist"
        return 1
    fi

    if [[ ! -e "$target_path" ]]; then
        echo "Error: Target path does not exist"
        return 1
    fi

    source_dir=$(dirname "$source_path")

    relative_path=$(python -c "import os.path; print(os.path.relpath('$target_path', '$source_dir'))")
    echo "$relative_path"
}

