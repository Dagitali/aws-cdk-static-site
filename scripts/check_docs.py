"""
:mod:`scripts.check_docs` module.

Validate repository-local Markdown links and heading anchors without requiring
network access.
"""

import re
from collections.abc import Iterator
from pathlib import Path
from urllib.parse import unquote, urlsplit

# SECTION: CONSTANTS


LINK_PATTERN = re.compile(r'(?<!!)\[[^\]]*\]\(([^)]+)\)')
REFERENCE_PATTERN = re.compile(r'^\s*\[[^\]]+\]:\s*(\S+)')
HEADING_PATTERN = re.compile(r'^#{1,6}\s+(.+?)\s*#*\s*$')
EXPLICIT_ANCHOR_PATTERN = re.compile(
    r'<a\s+(?:name|id)=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
FENCE_PATTERN = re.compile(r'^ {0,3}(?P<marker>`{3,}|~{3,})')
IGNORED_DIRECTORIES = frozenset({'cdk.out', 'node_modules'})


# !SECTION


# SECTION: PROTECTED FUNCTIONS


def _content_lines(path: Path) -> Iterator[tuple[int, str]]:
    """Yield numbered Markdown lines outside fenced code blocks."""
    fence: str | None = None
    for line_number, line in enumerate(
        path.read_text(encoding='utf-8').splitlines(),
        start=1,
    ):
        marker = FENCE_PATTERN.match(line)
        if marker is not None:
            candidate = marker.group('marker')
            if fence is None:
                fence = candidate
                continue
            if (
                candidate[0] == fence[0]
                and len(candidate) >= len(fence)
                and not line.removeprefix(marker.group()).strip()
            ):
                fence = None
                continue
        if fence is None:
            yield line_number, line


def _slugify(heading: str) -> str:
    """Approximate GitHub's stable heading-anchor algorithm."""
    heading = re.sub(r'<[^>]+>', '', heading)
    heading = re.sub(r'[`*_~]', '', heading).strip().lower()
    heading = re.sub(r'[^\w\- ]', '', heading, flags=re.UNICODE)
    return re.sub(r'\s+', '-', heading)


def _anchors(path: Path) -> set[str]:
    """Return explicit and heading-derived anchors in a Markdown file."""
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for _, line in _content_lines(path):
        anchors.update(EXPLICIT_ANCHOR_PATTERN.findall(line))
        match = HEADING_PATTERN.match(line)
        if match is None:
            continue
        base = _slugify(match.group(1))
        count = counts.get(base, 0)
        counts[base] = count + 1
        anchors.add(base if count == 0 else f'{base}-{count}')
    return anchors


def _is_ignored(path: Path, root: Path) -> bool:
    """Return whether a Markdown path is generated, vendored, or hidden."""
    relative_parts = path.relative_to(root).parts
    return any(
        part in IGNORED_DIRECTORIES or (part.startswith('.') and part != '.github')
        for part in relative_parts
    )


# !SECTION


# SECTION: FUNCTIONS


def validate(root: Path) -> list[str]:
    """
    Return actionable failures for broken repository-local Markdown links.

    Parameters
    ----------
    root : pathlib.Path
        Repository tree containing Markdown files.

    Returns
    -------
    list[str]
        Missing targets, missing anchors, and links that escape the repository.
    """
    if not root.is_dir():
        return [f'repository root does not exist: {root}']
    root = root.resolve()

    failures: list[str] = []
    anchor_cache: dict[Path, set[str]] = {}
    for path in sorted(root.rglob('*.md')):
        if _is_ignored(path, root):
            continue
        for line_number, line in _content_lines(path):
            targets = LINK_PATTERN.findall(line)
            reference = REFERENCE_PATTERN.match(line)
            if reference is not None:
                targets.append(reference.group(1))
            for raw_target in targets:
                target = raw_target.strip().split(maxsplit=1)[0].strip('<>')
                if not target:
                    continue
                parsed_target = urlsplit(target)
                if parsed_target.scheme or parsed_target.netloc:
                    continue
                if not parsed_target.path and not parsed_target.fragment:
                    continue
                linked_path = (
                    path
                    if not parsed_target.path
                    else (path.parent / unquote(parsed_target.path)).resolve()
                )
                try:
                    linked_path.relative_to(root)
                except ValueError:
                    failures.append(
                        f'{path.relative_to(root)}:{line_number}: '
                        f'link escapes repository: {target}',
                    )
                    continue
                if not linked_path.exists():
                    failures.append(
                        f'{path.relative_to(root)}:{line_number}: '
                        f'missing link target: {target}',
                    )
                    continue
                if (
                    parsed_target.fragment
                    and linked_path.is_file()
                    and linked_path.suffix.lower() == '.md'
                ):
                    anchors = anchor_cache.get(linked_path)
                    if anchors is None:
                        anchors = anchor_cache[linked_path] = _anchors(linked_path)
                    if unquote(parsed_target.fragment).lower() not in anchors:
                        failures.append(
                            f'{path.relative_to(root)}:{line_number}: '
                            f'missing anchor: {target}',
                        )
    return failures


# !SECTION
