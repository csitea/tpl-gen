#!/bin/bash

do_list_dockers(){
  clear;
  docker stats --no-stream --format "table {{.Container}}\t{{.Name}}\t{{.MemUsage}}" | awk 'BEGIN {OFS="\t"} NR==1 {$3="RAM (GB)"; print} NR>1 {split($3, a, "/"); $3=sprintf("%.2f GB", a[1]/(1024*1024*1024)); print}'|tail -n +2 |sort -k 2 |column -t
  export exit_code=$?
}
