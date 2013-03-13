library("xtable")

rank <- read.csv("../../data/general/rank.csv", header=F)
names(rank) <- c("Term", "Rank")

print(xtable(rank[0:30,], label = 'ranks',, 
             caption='Top 30 word ranks'), 
             include.rownames=FALSE, 
             size="small", scalebox=0.7,
             file=paste('ranks.tex', sep = ""))