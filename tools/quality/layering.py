#!/usr/bin/env python3
"""PWS-07: include layering check for src/core and src/os (fork-only; never part of an upstream PR).

Rules are those of backlog/decisions/decision-01 (PWS-04):
  * src/core or src/os must not include a header under src/ui;
  * src/core or src/os must not include a wx/ header;
  * src/os must not include a header under src/core (the existing edges are an accepted cycle);
  * every edge that breaks one of these rules must be listed in the edge-list file
    (tools/quality/layering-edges.txt), which lists exactly the 39 edges of decision-01.

An edge is "<including file> -> <header as written in the #include>". Includes are resolved the way
the CMake build resolves them (the including file's directory for quoted includes, then the global
include path from the top-level CMakeLists.txt), but against the files git tracks (`git ls-files`),
never the file system, so a generated header (for example version.h, which Makefile.macos writes
into src/ui/wxWidgets) is never counted as an edge on any build. A case-insensitive match is tried
last, because the Windows build resolves includes that way. An include that resolves to no tracked
file (a system or generated header) is not an edge, unless it is a wx/ header.

The allow list (tools/quality/layering-allow.txt, one "<file> -> <header>" per line) names includes
that are never counted as edges whatever they resolve to. Its only entry is the generated version.h
included by src/core/PWSversion.cpp (PWS-07 AC 10, RAID R-02), so the include stays out of the edge
count even if a generated copy were ever committed under src/ui.

Usage: layering.py [--repo DIR] [--edges FILE] [--allow FILE]
Prints a Markdown report and exits 1 on any NEW edge (or a duplicate line in the edge list).
Listed edges that are no longer present are reported as GONE but do not fail the check.
"""
import argparse
import os
import re
import subprocess
import sys

INCLUDE = re.compile(r'^\s*#\s*include\s*([<"])([^>"]+)[>"]')
# Global include path, in order, from the top-level CMakeLists.txt (include_directories);
# the build directory also sits on the path but holds only generated files, which git does not track.
SEARCH = ['src/os', 'src/core', 'src', 'src/ui/wxWidgets']
SOURCES = ('src/core/', 'src/os/')
EXTENSIONS = ('.c', '.cc', '.cpp', '.cxx', '.h', '.hpp', '.inl', '.m', '.mm')


def layer(path):
    for prefix, name in (('src/core/', 'core'), ('src/os/', 'os'), ('src/ui/', 'ui')):
        if path.startswith(prefix):
            return name
    return None


def read_pairs(path):
    """Read '<file> -> <header>' lines; '#' starts a comment."""
    pairs = []
    with open(path, encoding='utf-8') as fh:
        for raw in fh:
            line = raw.split('#', 1)[0].strip()
            if not line:
                continue
            src, sep, inc = line.partition(' -> ')
            if not sep:
                sys.exit(f'{path}: malformed line: {raw.rstrip()}')
            pairs.append((src.strip(), inc.strip()))
    return pairs


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n', 1)[0])
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument('--repo', default='.')
    ap.add_argument('--edges', default=os.path.join(here, 'layering-edges.txt'))
    ap.add_argument('--allow', default=os.path.join(here, 'layering-allow.txt'))
    a = ap.parse_args()

    tracked = subprocess.run(['git', '-C', a.repo, 'ls-files', '-z', '--', 'src'],
                             capture_output=True, text=True, check=True).stdout.split('\0')
    tracked = [t for t in tracked if t]
    exact = set(tracked)
    folded = {}
    for t in tracked:
        folded.setdefault(t.lower(), t)

    def resolve(src, inc, quoted):
        dirs = ([os.path.dirname(src)] if quoted else []) + SEARCH
        cands = [os.path.normpath(os.path.join(d, inc)) for d in dirs]
        for c in cands:
            if c in exact:
                return c
        for c in cands:
            if c.lower() in folded:
                return folded[c.lower()]
        return None

    allowed = read_pairs(a.allow)
    allowed_set = set(allowed)
    edges, seen_allowed, unresolved = {}, {}, 0
    sources = sorted(t for t in tracked if t.startswith(SOURCES) and t.endswith(EXTENSIONS))
    for src in sources:
        with open(os.path.join(a.repo, src), encoding='utf-8', errors='replace') as fh:
            for lineno, text in enumerate(fh, 1):
                m = INCLUDE.match(text)
                if not m:
                    continue
                quoted, inc = m.group(1) == '"', m.group(2).strip()
                target = resolve(src, inc, quoted)
                if (src, inc) in allowed_set:
                    seen_allowed.setdefault((src, inc), (lineno, target))
                    continue
                if target is None:
                    if not inc.startswith('wx/'):
                        unresolved += 1
                        continue
                    to = 'wx'
                else:
                    to = layer(target)
                frm = layer(src)
                if to in ('ui', 'wx') or (frm == 'os' and to == 'core'):
                    edges.setdefault((src, inc), (lineno, target or inc, f'{frm} to {to}'))

    listed = read_pairs(a.edges)
    listed_set = set(listed)
    problems = 0
    print(f'Scanned {len(sources)} tracked files under src/core and src/os: {len(edges)} layer-crossing '
          f'include edge(s); the edge list has {len(listed_set)}; the allow list has {len(allowed_set)} '
          f'entry(ies); {unresolved} include(s) resolve to no tracked file (system or generated headers).\n')
    for dup in sorted({p for p in listed if listed.count(p) > 1}):
        print(f'- DUPLICATE in edge list: `{dup[0]} -> {dup[1]}`')
        problems += 1
    for key, (lineno, target, kind) in sorted(edges.items()):
        if key in listed_set:
            continue
        print(f'- NEW edge ({kind}): `{key[0]}:{lineno}` includes `{key[1]}` (resolves to `{target}`); '
              'not in the edge list, so a design change for the architect or Fred Brooks (decision-01)')
        problems += 1
    for key, (lineno, target) in sorted(seen_allowed.items()):
        where = f'resolves to `{target}`' if target else 'resolves to no tracked file'
        print(f'- allowed (allow list, not an edge): `{key[0]}:{lineno}` includes `{key[1]}` ({where})')
    for key in sorted(allowed_set - set(seen_allowed)):
        print(f'- allow-list entry not used: `{key[0]} -> {key[1]}` (report only)')
    for key in sorted(listed_set - set(edges)):
        print(f'- GONE: listed edge `{key[0]} -> {key[1]}` is no longer present; update the edge list '
              'with design-change review (report only)')
    print(f"\n**Layering: {'FAIL' if problems else 'PASS'}** ({problems} problem(s))")
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
