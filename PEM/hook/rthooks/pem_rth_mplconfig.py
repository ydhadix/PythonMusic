# PEM's matplotlib runtime hook -- replaces PyInstaller's pyi_rth_mplconfig.py.
#
# PyInstaller's stock hook redirects MPLCONFIGDIR to a fresh temp directory on
# every launch, which forces matplotlib to rebuild its font cache from scratch
# each time PEM starts. On a typical macOS install this adds 5+ seconds before
# the first plot can render. The stock hook exists to dodge a onefile pitfall
# where fontList.cache caches font paths inside the previous _MEIxxxxx temp
# directory, which is deleted on shutdown.
#
# That pitfall does not apply here:
#   * matplotlib's current cache (fontlist-vNNN.json) stores bundled font paths
#     as relative paths (e.g. "fonts/ttf/DejaVuSans.ttf") that resolve against
#     mpl-data at runtime, plus absolute paths only for system fonts (which
#     are stable across runs);
#   * matplotlib also self-heals stale entries via _findfont_cached, rebuilding
#     the cache only when an entry actually points at a missing file.
#
# Doing nothing here lets matplotlib use its default config dir (~/.matplotlib
# on macOS, %USERPROFILE%/.matplotlib on Windows). The cache then persists
# across PEM launches and is shared with the user's system matplotlib install.
