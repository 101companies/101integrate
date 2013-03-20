library("xtable")

dataRoot <- "../../data"

rank <- read.csv(paste(dataRoot, "/allbooks/cache/", "rank.csv", sep=""), header=F)
names(rank) <- c("Term", "Rank")

#print(xtable(rank[0:30,], label = 'ranks',, 
#             caption='Top 30 word ranks'), 
#             include.rownames=FALSE, 
#             size="small", scalebox=0.7,
#             file=paste('ranks.tex', sep = ""))

write.csv(rank[0:30,], paste(dataRoot, "/allbooks/cache/", "rank.csv", sep=""))
