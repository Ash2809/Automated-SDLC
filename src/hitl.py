import json
from typing import Dict, Any

class HitlProvider:
    def request(self, gate: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

class CLIHitl(HitlProvider):
    def request(self, gate: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        print("\n===== HITL GATE:", gate, "=====")
        print(json.dumps(payload, indent=2)[:4000])
        while True:
            ans = input("Approve? [y/n/e=edit]: ").strip().lower()
            if ans in {"y", "n", "e"}:
                break
        notes = ""
        if ans == "e":
            print("Enter revised JSON (end with empty line):")
            buf = []
            while True:
                line = input()
                if not line:
                    break
                buf.append(line)
            try:
                payload = json.loads("\n".join(buf))
            except Exception as e:
                print("Invalid JSON, keeping original:", e)
        elif ans == "n":
            notes = input("Reason for rejection? ")
        return {"approved": ans == "y", "payload": payload, "notes": notes, "by": "cli-user"}

hitl_provider: HitlProvider = CLIHitl()
