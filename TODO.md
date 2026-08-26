# TODO

- Expose conflicting packages and symbols on the website. When two packages claim
  the same symbol (e.g. `pysam` is both the genomics package and `nrel-pysam`'s
  `PySAM` namespace), only one of them wins the redirect and the other one is
  silently unreachable. The losing package should be discoverable, e.g. a
  disambiguation note on the symbol's redirect page, or a list of known conflicts
  next to the package listing.
