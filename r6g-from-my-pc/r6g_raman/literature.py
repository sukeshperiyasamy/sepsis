"""Verified external literature references for Rhodamine 6G Raman/SERS/DFT
studies, used for the literature-comparison discussion.

Every entry below was individually confirmed via a live bibliographic
search/fetch in this session (title, authors, journal, volume, pages,
year, and DOI all checked against the publisher or an indexing service,
not taken from unverified training memory). This is external cited
literature metadata, not a computed result -- storing it as static data is
appropriate (the workflow's "no hardcoded results" rule applies to
*calculated quantities*, not to bibliographic citations of prior published
work).

A previously used citation ("Canamares et al. 2008, J. Phys. Chem. C 112,
20295") was DROPPED after verification showed it is actually a paper on
crystal violet SERS, not rhodamine 6G -- it has been removed from every
table/citation in this project.
"""

REFERENCES = [
    dict(
        key="Hildebrandt1984",
        authors="Hildebrandt, P.; Stockburger, M.",
        year=1984,
        title="Surface-enhanced resonance Raman spectroscopy of Rhodamine 6G adsorbed on colloidal silver",
        journal="J. Phys. Chem.",
        volume=88, pages="5935-5944",
        doi="10.1021/j150668a038",
        relevance="Foundational SERRS study of R6G on colloidal Ag; xanthene ring assignments, enhancement mechanism.",
    ),
    dict(
        key="Kneipp1995",
        authors="Kneipp, K.; Wang, Y.; Dasari, R. R.; Feld, M. S.",
        year=1995,
        title="Approach to Single Molecule Detection Using Surface-Enhanced Resonance Raman Scattering (SERRS): A Study Using Rhodamine 6G on Colloidal Silver",
        journal="Appl. Spectrosc.",
        volume=49, issue=6, pages="780-784",
        doi="10.1366/0003702953964480",
        relevance="Early single-molecule SERS demonstration on R6G; electromagnetic enhancement / hot-spot context.",
    ),
    dict(
        key="Watanabe2005",
        authors="Watanabe, H.; Hayazawa, N.; Inouye, Y.; Kawata, S.",
        year=2005,
        title="DFT Vibrational Calculations of Rhodamine 6G Adsorbed on Silver: Analysis of Tip-Enhanced Raman Spectroscopy",
        journal="J. Phys. Chem. B",
        volume=109, pages="5012-5020",
        doi="10.1021/jp045771u",
        relevance="DFT (B3LYP/6-311++G(d,p)) vibrational assignment of R6G, directly comparable level of theory to this work.",
    ),
    dict(
        key="Jensen2006",
        authors="Jensen, L.; Schatz, G. C.",
        year=2006,
        title="Resonance Raman Scattering of Rhodamine 6G as Calculated Using Time-Dependent Density Functional Theory",
        journal="J. Phys. Chem. A",
        volume=110, pages="5973-5977",
        doi="10.1021/jp0610867",
        relevance="TDDFT resonance Raman benchmark for R6G; frequency and relative-intensity comparison.",
    ),
    dict(
        key="Liu2008",
        authors="Liu, S.; Wan, S.; Chen, M.; Sun, M.",
        year=2008,
        title="Theoretical study on SERRS of rhodamine 6G adsorbed on Ag2 cluster: chemical mechanism via intermolecular or intramolecular charge transfer",
        journal="J. Raman Spectrosc.",
        volume=39, pages="1170-1177",
        doi="10.1002/jrs.1958",
        relevance="DFT charge-transfer (chemical enhancement) mechanism for R6G-Ag SERRS; directly informs the SERS discussion.",
    ),
]


def format_reference(ref: dict) -> str:
    issue = f"({ref['issue']})" if "issue" in ref else ""
    return (f"{ref['authors']} {ref['title']}. {ref['journal']} {ref['year']}, "
            f"{ref['volume']}{issue}, {ref['pages']}. DOI: {ref['doi']}")
