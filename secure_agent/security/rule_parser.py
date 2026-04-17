import json
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List
from rich.console import Console
from rich.panel import Panel

console = Console()

# Default path to the global rules configuration file
DEFAULT_RULES_PATH = Path(__file__).parent / "global_rules.json"

# Default configuration used when the file is missing or cannot be parsed
_DEFAULT_CONFIG = {
    "untrusted_provenance_keywords": ["environment", "untrusted", "web", "email"],
    "global_deny_tools_for_untrusted": ["send_money", "execute_script", "system_command"],
    "always_deny_tools": [],
}


class GlobalRules(BaseModel):
    """Strongly-typed representation of the declarative security rules."""

    untrusted_provenance_keywords: List[str] = Field(
        default_factory=lambda: list(_DEFAULT_CONFIG["untrusted_provenance_keywords"]),
        description="Keywords in a source_hypothesis that mark an instruction as untrusted.",
    )
    global_deny_tools_for_untrusted: List[str] = Field(
        default_factory=lambda: list(_DEFAULT_CONFIG["global_deny_tools_for_untrusted"]),
        description="Tools that must NEVER be executed when the instruction provenance is untrusted.",
    )
    always_deny_tools: List[str] = Field(
        default_factory=list,
        description="Tools that are unconditionally blocked regardless of provenance.",
    )


def load_global_rules(path: Path | str | None = None) -> GlobalRules:
    """
    Load the global security rules from a JSON configuration file.

    If the file does not exist it will be created with safe defaults so that
    security engineers always have a concrete file to edit.
    """
    rules_path = Path(path) if path else DEFAULT_RULES_PATH

    if not rules_path.exists():
        # Bootstrap: write a default config so the user has something to edit
        rules_path.parent.mkdir(parents=True, exist_ok=True)
        rules_path.write_text(json.dumps(_DEFAULT_CONFIG, indent=2) + "\n")
        console.print(
            Panel(
                f"[bold yellow]Created default security rules at {rules_path}[/bold yellow]",
                title="Rule Parser",
            )
        )

    try:
        raw = json.loads(rules_path.read_text())
        rules = GlobalRules(**raw)
    except (json.JSONDecodeError, Exception) as exc:
        console.print(
            f"[bold red]Failed to parse {rules_path}: {exc}. Falling back to defaults.[/bold red]"
        )
        rules = GlobalRules()

    console.print(
        Panel(
            f"[bold cyan]Loaded {len(rules.untrusted_provenance_keywords)} provenance keywords, "
            f"{len(rules.global_deny_tools_for_untrusted)} deny-for-untrusted tools, "
            f"{len(rules.always_deny_tools)} always-deny tools[/bold cyan]",
            title="Rule Parser",
        )
    )
    return rules
