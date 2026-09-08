from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "contracts" / "management-schemas.json"
TARGET = ROOT / "src" / "owlvigil" / "management_types.py"


def class_name(raw: str) -> str:
    leaf = raw.rsplit(".", 1)[-1]
    words = re.findall(r"[A-Z]+(?=[A-Z][a-z]|\d|$)|[A-Z]?[a-z]+|\d+", leaf)
    name = "".join(word[:1].upper() + word[1:] for word in words) or "ManagementModel"
    return name if name[0].isalpha() else "Model" + name


def main() -> None:
    schemas: dict[str, dict[str, Any]] = json.loads(SCHEMAS.read_text())
    names: dict[str, str] = {}
    used: set[str] = set()
    for raw in schemas:
        name = class_name(raw)
        if name in used:
            name += "Model"
        while name in used:
            name += "2"
        used.add(name)
        names[raw] = name

    def type_expr(schema: dict[str, Any] | None) -> str:
        if not schema:
            return "Any"
        ref = schema.get("$ref")
        if ref:
            return names.get(ref.rsplit("/", 1)[-1], "Any")
        if "enum" in schema:
            values = schema["enum"]
            if values and all(isinstance(value, (str, int, bool)) for value in values):
                return "Literal[" + ", ".join(repr(value) for value in values) + "]"
        if schema.get("type") == "array":
            return "List[" + type_expr(schema.get("items")) + "]"
        if schema.get("type") == "object" or "properties" in schema:
            return "Dict[str, Any]"
        return {"string": "str", "integer": "int", "number": "float", "boolean": "bool"}.get(schema.get("type"), "Any")

    lines = [
        "# Generated from contracts/management-schemas.json; do not edit.",
        "from __future__ import annotations",
        "",
        "from typing import Any, Dict, List, Literal, TypedDict",
        "",
    ]
    for raw, schema in schemas.items():
        name = names[raw]
        lines += [f"class {name}(TypedDict, total=False):"]
        properties = schema.get("properties", {})
        if not properties:
            lines.append("    pass")
        else:
            for field, value in properties.items():
                safe_field = field if field.isidentifier() else repr(field)
                lines.append(f"    {safe_field}: {type_expr(value)}")
        lines.append("")
    lines.append("ManagementSchema = Dict[str, Any]")
    lines.append("")
    lines.append("__all__ = [")
    lines.extend(f"    {name!r}," for name in names.values())
    lines.append("    'ManagementSchema',")
    lines.append("]")
    TARGET.write_text("\n".join(lines))
    print(f"generated {len(schemas)} Management TypedDict schemas")


if __name__ == "__main__":
    main()
