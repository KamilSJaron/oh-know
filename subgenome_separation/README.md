## Let's separate some subgenomes!

Here is some pertinent literature:
[Genome evolution in the allotetraploid frog Xenopus laevis](https://www.nature.com/articles/nature19840), and 
[Genome biology of the paleotetraploid perennial biomass crop Miscanthus](https://www.nature.com/articles/s41467-020-18923-6).

## But first
The whole pipeline would look like this:
First, you get a chromosome-resolved genome. Second, you use UCEs (ultra-conserved elements) to obtain chromosome pairs. Third, you assign one chromosome from each pair to either subgenome (e.g. A / B).

Unfortunately I will not be covering steps 1 and two from above. I will be explaining how to do step number 2 in my lecture, and **_I will be happy to provide code by e-mail_**. In any case, I will record this lecture and host it on YouTube.

## So, what is on the menu for today?

We will be working with a subset of the **_Scalesia atractyloides_** genome, where we have subgenome A and B. We have a chr-resolved assembly (step 1), and we know the pairs (step 2):
pair_01: chr25 pairs with chr12
pair_02: chr6 pairs with chr7
pair_03: chr18 pairs with chr8

This is a simplified example since the assembly has 17 pairs of chromosomes (32 in total).

## Let's get down to business

Let's organize and clean our space.
```
# First, we move to our working area:
cd $USERWORK

# Then, create a folder, and move inside:
mkdir subgenomeSeparation; cd subgenomeSeparation/

# I personally like to label folders numerically. Why? It's easier to follow, and once you finish a whole set of analyses and come back to it a few months later, you're able to remember the order. Let's make four folders:
mkdir 00_genome 01_splittingTheGenome 02_jellyfish_counting 03_jellyfish_dumping
# 00 - One folder just for the genome
# 01 - Another where we split the chromosomes into different files (so we run jellyfish in parallel and without issues)
# 02 - Another where we save the k-mer counting of jellyfish
# 03 - Finally, where we dump the information :)
```
