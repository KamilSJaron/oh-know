## Let's separate some subgenomes!

While my paper is in prep, here is some pertinent literature:
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

### Let's organize and clean our space.
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
# 03 - Finally, where we dump information to plot on R
```

### Now, we get a copy of the data (00)
```
# Copy the genome to where you are
cp /cluster/projects/nn9458k/oh_know/teachers/jose/scalesia_downscaled.fa ./00_genome/

# Take a brief look at it
less -S 00_genome/scalesia_downscaled.fa

# You see, we have ScDrF4C_12 (chr12), ScDrF4C_18 (chr 18), and so on
```

### Then, we separate fasta files for each chromosome (01)
```
# Let's just get a chr-id file so we can use a while loop
grep ">" 00_genome/scalesia_downscaled.fa | sed "s/>//"  > 01_splittingTheGenome/chromosome.ids.tsv
less 01_splittingTheGenome/chromosome.ids.tsv

# and make a loop which works chr-by-chr to separate files (loop explained below)
while read chr; do echo "Working on $chr" ; grep --no-group-separator -A 1 "$chr" 00_genome/scalesia_downscaled.fa > 01_splittingTheGenome/$chr.fa; done < 01_splittingTheGenome/chromosome.ids.tsv

ls 01_splittingTheGenome
# See? We created a fasta (.fa) file for each chromosome. This was done with the loop.
# Here is the loop dissected
# while read chr; do  - This line opens a while loop (a slow, but useful type of loop that will go line-by-line on a file we provide (provided in the last line)
# echo "Working on $chr"; - This line just prints to our screen so we can follow the progress
# grep --no-group-separator -A 1 "$chr" 00_genome/scalesia_downscaled.fa > 01_splittingTheGenome/$chr.fa; - This line searches for the variable chr, which was defined in the while loop (grep). Then, it saves that line and the line just below (-A 1) into a new file called $chr.fa
# done < 01_splittingTheGenome/chromosome.ids.tsv # We close the loop, and provide guidance to the file it should be looping over.
```

###  Kmer counting (02)

**_Remember that for your own genomes you may want to try different K-mer sizes. I used 13 since there was a lot of divergence (k-mer 25 gave no results)_**

```
# Okay, before we get down to business, we do not want to ruin the cluster. The Norwegian cluster has log-in nodes (where you log-in) and executing nodes (to execute jobs). We will be transfering to the executing nodes for the next steps since we will need computational power.

# This is guaranteed, by the srun
srun --ntasks=1 --mem-per-cpu=5G --time=02:00:00 --qos=devel --account=nn9458k --pty bash -i

# It should take a second. If it worked, it should change the id just before your username on the screen:
# BEFORE srun
# $USER@login-1.SAGA
# AFTER srun
# $USER@c5-59.SAGA

# Do not worry if it does not say 5-59. That's the computer they assigned to me but it may be different for you.

# Now we load Jellyfish. ml = module load. We're essentially asking the computer to make it available for us (software is not readily available for everyone so the computer does not get very slow for you - i.e. this computer is a National infrastructure and all Norwegian scientists are on it - chemists / physisists / philosophers; imagine loading all those software)

ml Jellyfish/2.3.0-GCC-9.3.0

# now we run jellyfish. The code below takes ~5 minutes so grab a coffee

for i in 01_splittingTheGenome/*fa; do echo $i; newname=$(echo ${i#*/} | sed "s/\.fa/.jf/"); jellyfish count -m 13 -s 100M -o 02_jellyfish_counting/$newname -t 1 $i; done

# output will be k-mer counts. I assume you're seasoned now and you know what a k-mer count is.
# loop explained:
# for i in 01_splittingTheGenome/*fa; - we open up the loop, using all fasta files created on 01
# do echo $i; - we print to the screen, much like we did before
# newname=$(echo ${i#*/} | sed "s/\.fa/.jf/"); - Ok, this one is more complicated, but I am essentially cleaning up the names. "i" will have the value of, for example "01_splittingTheGenome/ScDrF4C_8.fa", and "newname" will have "ScDrF4C_8.jf" (we removed "01_splittingTheGenome/", and ".fa").
# jellyfish count -m 13 -s 100M -o 02_jellyfish_counting/$newname -t 1 $i; # we run jellyfish using k-mer size of 13, and a single thread.
# done # We close the loop

# You can see the output in
ls 02_jellyfish_counting/

# You can also see that the files created are truncated
less 02_jellyfish_counting/*jf

```

###  Kmer dumping (03)
```
# Let's retrieve some human-readable (also R-readable) data from jellyfish using its "dump" function.
for i in 02_jellyfish_counting/*jf; do echo $i; jellyfish dump -c -L 100 $i > 03_jellyfish_dumping/${i#*/}.dumps.larger100.col; done

# loop explained:
# for i in 02_jellyfish_counting/*jf; do - we open the loop 
# echo $i; - print to the screen
# jellyfish dump -c -L 100 $i > 03_jellyfish_dumping/${i#*/}.dumps.larger100.col; - dump to the 03 folder, specifying column format (-c) and only k-mers with more than 100 (-L). We want k-mers with big representations so we catch "fossile TEs". I'll explain this below.
# done - closing the loop

# inspect the files with less
less 03_jellyfish_dumping/*
```

### Moving to your own computer
```
# Open a terminal on your own computer. Navigate to a folder where you want to operate (this I can't decide for you). Notice you need to change your username below.
scp _YOURUSERNAME_@saga.sigma2.no:/cluster/work/users/_YOURUSERNAME_/subgenomeSeparation/03_jellyfish_dumping/*col 
```

### Now we plot things in R

**_Open R studio_**

```
getwd()
setwd("/Users/josepc/Desktop/tmp/kmers") # Navigate to the folder where you have the col data.

install.packages("tidyverse") # Only needed if you don't have it already
library(tidyverse) # Load up your library


##### PAIR 01
s12<-read.table("./ScDrF4C_12.jf.dumps.larger100.col",sep="\t", header=T) %>%
  rename(s12=frequency)
s25<-read.table("./ScDrF4C_25.jf.dumps.larger100.col",sep="\t",header=T) %>%
  rename(s25=frequency)

# This code will object a variable called s12 and s25 based on the files (ScDrF4C_12.jf.dumps.larger100.col")). We specify it is separated by tabs , and header is true. The weird symbol (%>%) is a pipe (|) provided by tidyverse, and then we rename the column

pair01<-full_join(s12, s25, by="kmer")
head(pair01)

# We merge both datasets on an object called pair01

filtered_pair01<- pair01 %>% filter(s12 > 2*s25 | s25 > 2*s12)
nrow(filtered_pair01)

# We filter for k-mers that are either twice-represented on a member of the pair. E.g.:
# where s12 = 10, and s25 = 30 (keep)
# where s12 = 10, and s25 = 12 (remove)
# where s12 = 500, and s25 = 201 (keep)
# where s12 = 600, and s25 = 1004 (remove)

# Same for each pair

##### PAIR 02
s8<-read.table("./ScDrF4C_8.jf.dumps.larger100.col",sep="\t", header=T) %>%
  rename(s8=frequency)
s18<-read.table("./ScDrF4C_18.jf.dumps.larger100.col",sep="\t",header=T) %>%
  rename(s18=frequency)

pair02<-full_join(s8, s18, by="kmer")
head(pair02)

filtered_pair02<- pair02 %>% filter(s8 > 2*s18 | s18 > 2*s8)
nrow(filtered_pair02)

##### PAIR 03
s6<-read.table("./ScDrF4C_6.jf.dumps.larger100.col",sep="\t", header=T) %>%
  rename(s6=frequency)
s7<-read.table("./ScDrF4C_7.jf.dumps.larger100.col",sep="\t",header=T) %>%
  rename(s7=frequency)

pair03<-full_join(s6, s7, by="kmer")
head(pair03)

filtered_pair03<- pair03 %>% filter(s7 > 2*s6 | s6 > 2*s7)
nrow(filtered_pair03)




####

df<-full_join(filtered_pair01, filtered_pair02, by="kmer") %>%
  full_join(filtered_pair03, by="kmer")

par(mfrow=c(1,1))

cleaned_df<-df[complete.cases(df), ]

rownames(cleaned_df)<-cleaned_df$kmer

squeaky_cleaned_df<-cleaned_df[,-1]

transversed_squeaky_cleaned_df<-t(squeaky_cleaned_df)

dist_transversed_squeaky_cleaned_df <- dist(transversed_squeaky_cleaned_df)
hclust_avg <- hclust(dist_transversed_squeaky_cleaned_df)
plot(hclust_avg, main="13bp kmers at least 100x per chromossome, no NA; scalesia")
```
