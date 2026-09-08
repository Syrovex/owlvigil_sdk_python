from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "management-contract.json"
SRC = ROOT / "src" / "owlvigil"


def method_name(operation_id: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "_", operation_id).strip("_").lower()


def main() -> None:
    contract = json.loads(CONTRACT.read_text())
    operations = contract["operations"]
    names: dict[str, str] = {}
    for operation_id in operations:
        name = method_name(operation_id)
        if name in names:
            raise RuntimeError(f"method name collision: {name}")
        names[name] = operation_id

    operation_lines = [
        "# Generated from contracts/management-contract.json; do not edit.",
        "from __future__ import annotations",
        "",
        "from dataclasses import dataclass",
        "from typing import Dict, Literal, Mapping, Optional, Union",
        "",
        "",
        "@dataclass(frozen=True)",
        "class ManagementOperation:",
        "    method: str",
        "    path: str",
        "",
        "",
        "MANAGEMENT_OPERATIONS: Dict[str, ManagementOperation] = {",
    ]
    for operation_id, definition in operations.items():
        operation_lines.append(
            f'    {operation_id!r}: ManagementOperation({definition["method"]!r}, {definition["path"]!r}),' 
        )
    operation_lines += ["}", "", "ManagementOperationId = Literal[",]
    operation_lines += [f"    {operation_id!r}," for operation_id in operations]
    operation_lines += ["]", ""]
    (SRC / "management_operations.py").write_text("\n".join(operation_lines))

    method_lines = [
        "# Generated from contracts/management-contract.json; do not edit.",
        "from __future__ import annotations",
        "",
        "from typing import Any, Optional",
        "",
        "from ._core import ApiResponse, ManagementOperationRequest",
        "",
        "",
        "class GeneratedManagementMethods:",
    ]
    for name, operation_id in names.items():
        method_lines += [
            f"    def {name}(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:",
            f"        return self.open_api({operation_id!r}, request)",
            "",
        ]
    method_lines += ["", "class AsyncGeneratedManagementMethods:"]
    for name, operation_id in names.items():
        method_lines += [
            f"    async def {name}(self, request: Optional[ManagementOperationRequest] = None) -> ApiResponse:",
            f"        return await self.open_api({operation_id!r}, request)",
            "",
        ]
    (SRC / "management_methods.py").write_text("\n".join(method_lines))
    print(f"generated {len(operations)} Management operations and methods")


if __name__ == "__main__":
    main()
