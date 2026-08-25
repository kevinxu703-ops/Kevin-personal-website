from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]


class ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key not in {"href", "src", "data"} or not value:
                continue
            if value.startswith(("#", "http:", "https:", "mailto:")):
                continue
            self.references.append(value.split("#", 1)[0])


def main() -> None:
    missing: list[tuple[Path, str]] = []
    pages = sorted(ROOT.rglob("*.html"))

    for page in pages:
        parser = ReferenceParser()
        parser.feed(page.read_text(encoding="utf-8"))
        for reference in parser.references:
            target = (page.parent / unquote(reference)).resolve()
            if reference and not target.exists():
                missing.append((page.relative_to(ROOT), reference))

    if missing:
        for page, reference in missing:
            print(f"Missing: {page} -> {reference}")
        raise SystemExit(1)

    print(f"Checked {len(pages)} HTML pages: all local references exist.")


if __name__ == "__main__":
    main()
