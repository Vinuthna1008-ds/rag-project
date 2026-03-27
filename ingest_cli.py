"""
ingest_cli.py — standalone script to ingest files/directories from the command line.

Usage:
    python ingest_cli.py /path/to/dir_or_file [/another/path ...]

This is useful for pre-loading documents before starting the app.
Note: the vectorstore is in-memory, so the app must be kept running.
For persistent ingest, set persist_directory in rag.py.
"""

import sys
import os

# Ensure project root is in Python path
sys.path.insert(0, os.path.dirname(__file__))

from backend.rag import ingest

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ingest_cli.py <path1> [path2 ...]")
        sys.exit(1)

    paths = sys.argv[1:]
    print(f"Ingesting {len(paths)} path(s): {paths}")
    try:
        n = ingest(paths)
        print(f"✅ Done — {n} chunks added to vectorstore.")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)