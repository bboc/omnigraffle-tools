#!/bin/bash
# bash wrapper around JavaScript

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"

OSA_LIBRARY_PATH="${DIR}/Resources"$OSA_LIBRARY_PATH
#OSA_LIBRARY_PATH="${DIR}/Resources:"$OSA_LIBRARY_PATH
export OSA_LIBRARY_PATH
echo $OSA_LIBRARY_PATH
./test.js

