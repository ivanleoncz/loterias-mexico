![Action](https://github.com/ivanleoncz/loterias-mexico/actions/workflows/tests.yml/badge.svg)
# Mexlona
Command line tool for scrapping Mexico's Loterial Nacional data, providing statistical data and visualization.

### Description
Eventually, I play the lottery. Instead of going on Mexico's Loteria Nacional website and download datasets in order
to see if my numbers were drawn, I thought it would be nice to have a CLI, where I can download the datasets, import
to a database and with some options, I could quickly review the latest results, or even have some statistical analysis,
in order to determine how random the results can be.

Pandas could be a great fit for this project (it was used before), but I rather have pure SQL commands to generate
database queries, making the project not so dependent of external libraries.

This project wasn't intended to be a professional thing. It was made just for fun, getting lottery results without
accessing web pages and having some SQL database do play with, again, for fun.

Hope it might inspire you to do something serious.

Regards,<br>
Ivan Leon

### Stack
- Python 3.8
- Beautiful Soup
- Sqlite3
- Matplotlib

### Supported Products
- Tris
- Melate Retro

### Status
- Web Scrapping: **OK**
- Database Storage: **OK**
- CLI results: *WIP*
- CLI visualization: *WIP*