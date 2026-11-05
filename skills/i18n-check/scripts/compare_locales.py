#!/usr/bin/env python3
"""Compare explicit JSON locale files; no project scan or file mutation."""

import argparse
import json
from pathlib import Path
import sys


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"invalid JSON constant: {value}")


def load_locale(path):
    value = json.loads(path.read_text(encoding="utf-8-sig"),
                       object_pairs_hook=unique_object, parse_constant=reject_constant)
    if not isinstance(value, dict):
        raise ValueError("locale root must be an object")
    return value


def leaves(value, pointer=""):
    if isinstance(value, dict) and value:
        result = {}
        for key, child in value.items():
            escaped = key.replace("~", "~0").replace("/", "~1")
            result.update(leaves(child, f"{pointer}/{escaped}"))
        return result
    if isinstance(value, list) and value:
        result = {}
        for index, child in enumerate(value):
            result.update(leaves(child, f"{pointer}/{index}"))
        return result
    if value is None:
        kind = "null"
    elif isinstance(value, bool):
        kind = "boolean"
    elif isinstance(value, (int, float)):
        kind = "number"
    elif isinstance(value, str):
        kind = "string"
    elif isinstance(value, dict):
        kind = "object"
    else:
        kind = "array"
    return {pointer: kind}


def compare(base, target, limit):
    missing = sorted(base.keys() - target.keys())
    extra = sorted(target.keys() - base.keys())
    mismatches = [{"path": key, "base_type": base[key], "locale_type": target[key]}
                  for key in sorted(base.keys() & target.keys()) if base[key] != target[key]]
    return {"missing": {"count": len(missing), "items": missing[:limit]},
            "extra": {"count": len(extra), "items": extra[:limit]},
            "type_mismatches": {"count": len(mismatches), "items": mismatches[:limit]}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, type=Path)
    parser.add_argument("--locale", required=True, action="append", type=Path)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be >= 1")
    current = args.base
    try:
        base = leaves(load_locale(args.base))
        reports = []
        different = False
        for current in args.locale:
            result = compare(base, leaves(load_locale(current)), args.limit)
            different = different or any(group["count"] for group in result.values())
            reports.append({"locale": str(current), **result})
        print(json.dumps({"base": str(args.base), "limit": args.limit, "reports": reports},
                         ensure_ascii=False, indent=2))
        return int(different)
    except (OSError, ValueError, RecursionError) as error:
        print(json.dumps({"file": str(current), "error": str(error)}, ensure_ascii=False),
              file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
