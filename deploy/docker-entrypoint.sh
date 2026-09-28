#!/bin/sh
set -e

# Fix data directory permissions when running as root.
# Docker named volumes / host bind-mounts may be owned by root,
# preventing the non-root bps-sub2api user from writing files.
if [ "$(id -u)" = "0" ]; then
    mkdir -p /app/data
    # Use || true to avoid failure on read-only mounted files (e.g. config.yaml:ro)
    chown -R bps-sub2api:bps-sub2api /app/data 2>/dev/null || true
    # Re-invoke this script as bps-sub2api so the flag-detection below
    # also runs under the correct user.
    exec su-exec bps-sub2api "$0" "$@"
fi

# Compatibility: if the first arg looks like a flag (e.g. --help),
# prepend the default binary so it behaves the same as the old
# ENTRYPOINT ["/app/bps-sub2api"] style.
if [ "${1#-}" != "$1" ]; then
    set -- /app/bps-sub2api "$@"
fi

exec "$@"
