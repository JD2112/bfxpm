---
hide:
  - navigation
---

# References

This page lists the scientific and technical references discussed in the BfxPM documentation and development plan, including international standards for reproducible research and data management.

## International Guidelines & Standards

- [The Turing Way](https://the-turing-way.netlify.app/index.html) - The leading international handbook for reproducible, ethical, and collaborative data science.
- [ELIXIR Research Data Management (RDM)](https://elixir-europe.org/platforms/data/rdm) - Best practices for life science data management, emphasizing the separation of raw data and results.
- [Software Carpentry (Project Organization)](https://swcarpentry.github.io/python-novice-gapminder/19-project-organization/index.html) - Foundations of structured computational research.
- [nf-core Project Structure](https://nf-co.re/docs/guidelines/external_workflows/introduction) - Guidelines for scalable, reproducible bioinformatics pipelines.
- [Snakemake Best Practices](https://snakemake.readthedocs.io/en/stable/snakefiles/best_practices.html) - Structural recommendations for modular workflow management.
- [FAIR Research Software (FAIR4RS)](https://www.rd-alliance.org/groups/fair-research-software-fair4rs-wg) - International standards for making software Findable, Accessible, Interoperable, and Reusable.
- [Wilkinson et al. (2016)](https://doi.org/10.1038/sdata.2016.18) - The foundational paper on the FAIR Guiding Principles for scientific data management and stewardship.
- [Gentleman et al. (2004) - Bioconductor](https://doi.org/10.1186/gb-2004-5-10-r80) - Foundational concepts for open source software in bioinformatics.

## CLI & Software Design Philosophy

- [Command Line Interface Guidelines](https://clig.dev/) - An open-source guide to help you write better command-line programs.
- [Rich Documentation](https://rich.readthedocs.io/) - The library powering BfxPM's visual terminal experience.
- [Typer Documentation](https://typer.tiangolo.com/) - The framework enabling our modular and type-safe CLI structure.

## Sequence Data Compression

1. [Academic 0up (Lossless Genomic Compression)](https://academic.oup.com/bfg/article/doi/10.1093/bfgp/elae050/7945366) - General overview of essential lossless strategies.
2. [PMC6662292 (Specialized Compressors)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6662292/) - Performance comparisons of specialized genomic compressors vs. Gzip.
3. [IEEE Spectrum (The Desperate Quest for Genomic Compression)](https://spectrum.ieee.org/the-desperate-quest-for-genomic-compression-algorithms) - Rationale for domain-specific algorithms.
4. [Nature Scientific Reports (Lossless Compression of FASTQ Files)](https://www.nature.com/articles/s41598-024-79258-6)
5. [NanoSpring (Long-read FASTQ Compression)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9902536/) - Specialized tool for Nanopore and PacBio data.
6. [EBI Sequence File Formats](https://www.ebi.ac.uk/fg/annotare/help/accepted_sequencing_file_formats.html)
7. [Biostars Thread (FASTQ vs CRAM vs Genozip)](https://www.biostars.org/p/163645/)
8. [Illumina FASTQ ORA Format](https://www.illumina.com/informatics/sequencing-data-analysis/sequence-file-formats.html)

## Aligned Data (BAM/CRAM)

11. [Bioinformatics Stack Exchange (Best Archive Practices)](https://bioinformatics.stackexchange.com/questions/20858/good-recommended-way-to-archive-fastq-and-bam-files)
12. [CRAM Specification (GA4GH Standard)](https://www.ga4gh.org/news_item/guest-post-seven-myths-about-cram-the-community-standard-for-genomic-data-compression/)
13. [HTSeq Read Mapping Documentation](https://htseq.readthedocs.io/en/latest/tutorials/bam_reader.html)

## Raw Signal Data (FAST5/POD5/SLOW5)

16. [Oxford Nanopore Beginner's Guide to Formats](https://nanoporetech.com/blog/analysing-oxford-nanopore-data-a-beginners-guide-to-file-formats)
17. [SLOW5 & blow5 Documentation](https://pmc.ncbi.nlm.nih.gov/articles/PMC12212073/) - Open-source lossless alternative for raw signal recording.
18. [VBZ Compression Plugin](https://epi2me.nanoporetech.com/notebooks/Introduction_to_Fast5_files.html) - Lossless squiggle signal compression within HDF5.
