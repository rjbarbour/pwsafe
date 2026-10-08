"""PWS-07: shared helpers for the fork quality gate scripts (fork-only; never upstream)."""
import re
import subprocess

# Paths the Linux build compiles and the static-analysis gates cover: src/core (vendored pugixml and
# crypto/external excluded), the top level of src/os and src/os/unix, src/ui/wxWidgets, src/ui/cli and
# src/test. macOS- and Windows-only code (src/os/mac, src/os/windows, src/ui/Windows) is not built on
# the Linux runner, so clang-tidy and cppcheck cannot analyse it there.
GATED = ['src/core', ':(glob)src/os/*.h', ':(glob)src/os/*.cpp', 'src/os/unix', 'src/ui/wxWidgets', 'src/ui/cli',
         'src/test', ':(exclude)src/core/pugixml', ':(exclude)src/core/crypto/external']
CXX = r'.*\.(c|cc|cpp|cxx|h|hpp)$'


def git(*args, repo='.'):
    return subprocess.run(['git', '-C', repo, *args], capture_output=True, text=True, check=True).stdout


def merge_base(base, repo='.'):
    return git('merge-base', base, 'HEAD', repo=repo).strip()


def changed_lines(mb, pathspec, repo='.'):
    """{path: set(line numbers in HEAD)} for lines added or changed since the merge base."""
    out, cur = {}, None
    for line in git('diff', '-U0', '--no-color', '--no-renames', mb, 'HEAD', '--', *pathspec, repo=repo).splitlines():
        if line.startswith('+++ '):
            cur = line[6:] if line.startswith('+++ b/') else None
            continue
        m = re.match(r'@@ -\S+ \+(\d+)(?:,(\d+))? @@', line)
        if m and cur:
            start, count = int(m.group(1)), int(m.group(2) or 1)
            if count:
                out.setdefault(cur, set()).update(range(start, start + count))
    return out
