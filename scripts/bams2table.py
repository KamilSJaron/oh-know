#!/usr/bin/env python3
​
# arguments Y_bam, X_bam, A_bam
​
from sys import stderr
import sys
import pysam
from collections import defaultdict

A_bamfile = sys.argv[1]​
X_bamfile = sys.argv[2]
Y_bamfile = sys.argv[3]
​seq_table_file = sys.argv[4]

stderr.write('Input files:\n')
stderr.write('	A bamfile: ' + A_bamfile + '\n')
stderr.write('	X bamfile: ' + X_bamfile + '\n')
stderr.write('	Y bamfile: ' + Y_bamfile + '\n')
​
stderr.write('Checking indexes\n')
for bamfile in [Y_bamfile, X_bamfile, A_bamfile]:
	with pysam.AlignmentFile(bamfile, "rb") as bam:
		try:
			bam.check_index()
			bam.close()
			stderr.write('\t' + bamfile + ' is already indexed\n')
		except ValueError:
			bam.close()
			stderr.write('\tIndexing ' + bamfile + '\n')
			pysam.index(bamfile)
​
class mapped_kmers(object):
    def __init__(self):
        self.Y = 0
        self.X = 0
        self.A = 0
    def __repr__(self):
        return '{}\t{}\t{}'.format(self.A, self.X, self.Y)
    def __str__(self):
        return '{}\t{}\t{}'.format(self.A, self.X, self.Y)
    def addY(self):
        self.Y += 1
    def addX(self):
        self.X += 1
    def addA(self):
        self.A += 1
​
stderr.write('Processing mapping files\n')
seq_table = defaultdict(mapped_kmers)

with pysam.AlignmentFile(A_bamfile, "rb") as A_bam:
	for seq in A_bam.fetch():
		seq_table[seq.reference_name].addA()
stderr.write('\tA bamfile done\n')
​​
with pysam.AlignmentFile(X_bamfile, "rb") as X_bam:
	for seq in X_bam.fetch():
		seq_table[seq.reference_name].addX()
stderr.write('\tX bamfile done\n')

with pysam.AlignmentFile(Y_bamfile, "rb") as Y_bam:
	for seq in Y_bam.fetch():
		seq_table[seq.reference_name].addY()
stderr.write('\tY bamfile done\n')

# seq_table_file = "table_of_mapped_kmers.tsv"
stderr.write('Writing output in +' + seq_table_file + '\n')
​
with open(seq_table_file, 'w') as outtab:
	outtab.write('id\tA\tX\tY\n')
	for seq in seq_table.keys():
		seq_mapped_kmers = seq_table[seq]
		outtab.write('{}\t{}\t{}\t{}\n'.format(seq, seq_mapped_kmers.A, seq_mapped_kmers.X, seq_mapped_kmers.Y))
​
stderr.write('Everything is done now\n')
