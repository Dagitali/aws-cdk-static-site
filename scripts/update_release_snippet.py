"""
:mod:`scripts.update_release_snippet` module.

Render, update, or verify the README installation snippet associated with a
semantic release tag.
"""

from pathlib import Path

from ._support import normalize_release

# SECTION: CONSTANTS


END_MARKER = '<!-- release-install:end -->'
START_MARKER = '<!-- release-install:start -->'


# !SECTION


# SECTION: FUNCTIONS


def render(
    release: str,
) -> str:
    """
    Render the complete marked installation snippet for a release.

    Parameters
    ----------
    release : str
        Semantic version with an optional leading ``v``.

    Returns
    -------
    str
        Markdown marker pair and installation command for the normalized tag.

    Raises
    ------
    ValueError
        If *release* is not a semantic ``major.minor.patch`` version.
    """
    tag = f'v{normalize_release(release)}'
    return (
        f'{START_MARKER}\n'
        '```bash\n'
        'python -m pip install \\\n'
        '  "aws-cdk-static-site @ '
        'git+https://github.com/Dagitali/aws-cdk-static-site.git@'
        f'{tag}"\n'
        '```\n'
        f'{END_MARKER}'
    )


def update(
    readme: Path,
    release: str,
    *,
    check: bool = False,
) -> list[str]:
    """
    Update the marked snippet or return validation failures in check mode.

    Parameters
    ----------
    readme : pathlib.Path
        README containing one release-installation marker pair.
    release : str
        Semantic version with an optional leading ``v``.
    check : bool, optional
        Validate existing content without writing when ``True``.

    Returns
    -------
    list[str]
        Human-readable failures; empty after a successful update or check.

    Raises
    ------
    ValueError
        If *release* is not a semantic ``major.minor.patch`` version.
    """
    if not readme.is_file():
        return [f'readme does not exist: {readme}']

    content = readme.read_text(encoding='utf-8')
    if content.count(START_MARKER) != 1 or content.count(END_MARKER) != 1:
        return [f'{readme.name} must contain one release installation marker pair']

    start = content.index(START_MARKER)
    marker_end = content.find(END_MARKER, start)
    if marker_end < 0:
        return [f'{readme.name} must place its end marker after its start marker']
    end = marker_end + len(END_MARKER)
    expected = render(release)
    if content[start:end] == expected:
        return []
    if check:
        tag = release if release.startswith('v') else f'v{release}'
        return [f'{readme.name} installation snippet does not reference {tag}']

    readme.write_text(
        f'{content[:start]}{expected}{content[end:]}',
        encoding='utf-8',
    )
    return []


# !SECTION
