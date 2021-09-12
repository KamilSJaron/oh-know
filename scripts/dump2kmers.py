from pandas import read_table
import numpy as np

# merged_dump_file = sys.argv[1]
merged_dump_file = 'testing_merged_dump.tsv'
# sample_threshold_file = sys.argv[2]
sample_threshold_file = 'testing_thesholds.tsv'
# output_name_prefix = sys.argv[3]
output_name_prefix = 'testing_kmers'

A_file = output_name_prefix + '_A.fasta'
X_file = output_name_prefix + '_X.fasta'
Y_file = output_name_prefix + '_Y.fasta'

thresholds = read_table(sample_threshold_file)
dump_tab = read_table(merged_dump_file)

females = [i == 'F' for i in thresholds['sex']]

for i, sample in enumerate(dump_tab.columns):
    # print (i, sample)
    sample_ploidy = np.full(len(dump_tab[sample]), 3)
    sample_ploidy[dump_tab[sample] < thresholds.at[i, 'monoploid_min']] = 0
    sample_ploidy[np.logical_and(dump_tab[sample] > thresholds.at[i, 'monoploid_min'], dump_tab[sample] < thresholds.at[i, 'monoploid_max'])] = 1
    sample_ploidy[np.logical_and(dump_tab[sample] > thresholds.at[i, 'diploid_min'], dump_tab[sample] < thresholds.at[i, 'diploid_max'])] = 2
    dump_tab[sample] = sample_ploidy

A_kmers = 0
X_kmers = 0
Y_kmers = 0

with open(X_file, 'w') as X, open(A_file, 'w') as A, open(Y_file, 'w') as Y:
    for index, kmer in dump_tab.iterrows():
        # print(kmer)
        females_absent = sum([ploidy == 0 for i, ploidy in enumerate(kmer) if females[i]])
        females_diploid = sum([ploidy == 2 for i, ploidy in enumerate(kmer) if females[i]])
        males_monoploid = sum([ploidy == 1 for i, ploidy in enumerate(kmer) if not females[i]])
        males_diploid = sum([ploidy == 2 for i, ploidy in enumerate(kmer) if not females[i]])
        if females_diploid >= 3 and males_diploid >= 3:
            A_kmers += 1
            kmer_fasta_record = '>A_' + str(A_kmers) + '\n' + kmer.name + '\n'
            A.write(kmer_fasta_record)
            continue
        if males_monoploid >= 3 and females_diploid >= 3:
            X_kmers += 1
            kmer_fasta_record = '>X_' + str(X_kmers) + '\n' + kmer.name + '\n'
            X.write(kmer_fasta_record)
            continue
        if females_absent >= 3 and males_monoploid >= 3:
            Y_kmers += 1
            kmer_fasta_record = '>Y_' + str(Y_kmers) + '\n' + kmer.name + '\n'
            Y.write(kmer_fasta_record)
            continue

# now dump_tab contains ploidy level per sample