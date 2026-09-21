#!/bin/bash
set -e

VERSION_FILE="version.txt"

if [ ! -f "$VERSION_FILE" ]; then
  echo "Error: $VERSION_FILE not found."
  exit 1
fi

# Read the current version (e.g., 1.0.0+5)
CURRENT_VERSION=$(cat "$VERSION_FILE")

# Split the version into base (1.0.0) and build number (5) using + as delimiter
BASE_VERSION="${CURRENT_VERSION%+*}"
BUILD_NUMBER="${CURRENT_VERSION#*+}"

# Ensure build number is valid
if [[ ! "$BUILD_NUMBER" =~ ^[0-9]+$ ]]; then
   echo "Error: Build number '$BUILD_NUMBER' is not a valid integer."
   exit 1
fi

# Increment the build number
NEW_BUILD_NUMBER=$((BUILD_NUMBER + 1))

# Create the new version string
NEW_VERSION="${BASE_VERSION}+${NEW_BUILD_NUMBER}"

# Update the version file
echo "$NEW_VERSION" > "$VERSION_FILE"

echo "Incremented version from $CURRENT_VERSION to $NEW_VERSION"