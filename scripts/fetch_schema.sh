#!/usr/bin/env bash

set -euo pipefail

REGION=us-east-1
ZIP_FILENAME=CloudformationSchema.zip
SOURCE_URL="https://schema.cloudformation.${REGION}.amazonaws.com/${ZIP_FILENAME}"
TEMP_DIR="$PWD/schemas"

main() {
    mkdir -p "$TEMP_DIR"
    trap "rm -rf $TEMP_DIR" EXIT

    if [ ! -f "$TEMP_DIR/$ZIP_FILENAME" ]; then
        curl -sLo "$TEMP_DIR/$ZIP_FILENAME" "$SOURCE_URL"
    fi

    # unpack
    (cd "$TEMP_DIR" && unzip -qo "$ZIP_FILENAME")

    # concat into single file
    printf "%s\0" "$TEMP_DIR"/*.json | xargs -0 cat | jq -s 'sort_by(.typeName)' > cfn-schema.json
}

main
