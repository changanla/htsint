High-Throughput Sequencing Integrate - htsint
===============================================

A Python library (under initial development) to integrate
high-throughput sequencing data using probabilistic graphical models.

Prerequisites (Ubuntu/Debian)
--------------

General:

  * ncbi-blast+
  * python package - numpy
  * python package - matplotlib 
  * python package - networkx
  * python package - pymc 
  * python package - biopython

Database specific:

  * postgresql (or another relational db)
  * database driver i.e. psycopg2 
  * python package - sqlalchemy

Database
-----------
The non-sequencing data is stored in a database:

  * Taxa
  * Gene names, synonyms
  * Gene accessions
  * Gene Ontology terms and annotations

The data is managed and accessed using SQLAlchemy

  http://www.sqlalchemy.org

BLAST and other sequence analyses 
-----------------------------------

This is a collection of functions to carry out the general analysis of
high-thoughput sequencing data.  These functions make heavy use of
Biopython:

  http://biopython.org/wiki/Main_Page

Statistical Models
----------------------

The statistical models extensively use the PyMC sampling toolkit.

  https://pypi.python.org/pypi/pymc
