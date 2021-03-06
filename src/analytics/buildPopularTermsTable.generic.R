library("xtable")

dataRoot <- "../../data"

books <- commandArgs(trailingOnly = TRUE)

topFrequency = list() 
for (i in 1:length(books))
    topFrequency[i] <- read.csv(paste(dataRoot, "/perbook/",books[i], "/topFrequency.csv", sep=""))
# topFrequencyCraft <- read.csv(paste(dataRoot, "/perbook/", "Craft/topFrequency.csv", sep=""))
# topFrequencyPih <- read.csv(paste(dataRoot, "/perbook/", "PIH/topFrequency.csv", sep=""))
# topFrequencyRwh <- read.csv(paste(dataRoot, "/perbook/", "RWH/topFrequency.csv", sep=""))
# topFrequencyLyah <- read.csv(paste(dataRoot, "/perbook/", "LYAH/topFrequency.csv", sep=""))

frequency = list() 
for (i in 1:length(books))
    frequency[i] <- read.csv(paste(dataRoot, "/perbook/", books[i],"/frequenciesMerged.csv", sep=""), sep=";")
# frequencyCraft <- read.csv(paste(dataRoot, "/perbook/", "Craft/frequenciesMerged.csv", sep=""), sep=";")
# frequencyPih <- read.csv(paste(dataRoot, "/perbook/", "PIH/frequenciesMerged.csv", sep=""), sep=";")
# frequencyRwh <- read.csv(paste(dataRoot, "/perbook/", "RWH/frequenciesMerged.csv", sep=""), sep=";")
# frequencyLyah <- read.csv(paste(dataRoot, "/perbook/", "LYAH/frequenciesMerged.csv", sep=""), sep=";")

for (i in 1:length(books))
    frequency[i] <- subset(frequency[i], subset=TRUE,  select=c(0,3))
# frequencyCraft <- subset(frequencyCraft, select=c(0,3))
# frequencyPih <- subset(frequencyPih, select=c(0,3))
# frequencyRwh <- subset(frequencyRwh, select=c(0,3))
# frequencyLyah <- subset(frequencyLyah, select=c(0,3))

#take union of TOP terms across all books
all <- NULL
for (topF in topFrequency) all <- rbind(all, topF)
rownames(all) <- books
#all <- rbind(topFrequencyCraft, topFrequencyLyah, topFrequencyPih, topFrequencyRwh)
union <- data.frame(sort(unique(all$Term), decreasing = FALSE))
names(union) <- c("Term")
v <- data.frame(vector(mode = "integer",length(union$Term)),stringsAsFactors = FALSE) 

#initialize columns per book with default values
for (i in 1:kength(books)) union <- cbind(union, v)
#union <- cbind(union, v)
#union <- cbind(union, v)
#union <- cbind(union, v)
#union <- cbind(union, v)

names(union) <- c("Term", books)
#names(union) <- c("Term", "Craft", "PIH", "RWH", "LYAH")
row.names(union) <- seq(nrow(union))
union$Term <- as.character(union$Term)
union <- union[with(union, order(union$Term)),]

for (f in frequency)
  for(t in union$Term) if(t %in% as.vector(f$Term)) union[which(union$Term == t),2] <- f[which(f$Term == t),2]
# for(t in union$Term) if(t %in% as.vector(frequencyCraft$Term)) union[which(union$Term == t),2] <- frequencyCraft[which(frequencyCraft$Term == t),2]
# for(t in union$Term) if(t %in% as.vector(frequencyPih$Term)) union[which(union$Term == t),3] <- frequencyPih[which(frequencyPih$Term == t),2]
# for(t in union$Term) if(t %in% as.vector(frequencyRwh$Term)) union[which(union$Term == t),4] <- frequencyRwh[which(frequencyRwh$Term == t),2]
# for(t in union$Term) if(t %in% as.vector(frequencyLyah$Term)) union[which(union$Term == t),5] <- frequencyLyah[which(frequencyLyah$Term == t),2]

write.csv(union, paste(dataRoot, "/allbooks/", "/unionTopFrequencies.csv", sep=""))

#print(xtable(union, label=paste('F:unionTopFrequencies', sep = ""), caption="Union of TOP 30 frequent terms from the books"),
#      file="unionTopFrequencies.tex", scalebox=0.7,
#      include.rownames=FALSE,  
#      rotate.colnames=FALSE)

#- One column per book showing popularity per book in a percentile-based manner:
#* empty cell = no occurrence in the given book
#* dot = frequency is 1
#* small circle = below median but larger than 1
#* big circle = greater or above median
#* biggest circle = in the top-n


qBook = list()
qBookMedian = list() 
for (i in 1:length(books)){
  qBook[i] <- as.vector(quantile(union$(books[i])))
  qBookMedian[i] = qBook[3]
}

# qCraft <- as.vector(quantile(union$Craft))
# qCraftMedian = qCraft[3]
# 
# qRWH   <- as.vector(quantile(union$RWH))
# qRWHMedian <- qRWH[3]
# 
# qPIH   <- as.vector(quantile(union$PIH))
# qPIHMedian <- qPIH[3]
# 
# qLYAH  <- as.vector(quantile(union$LYAH))
# qLYAHMedian <- qLYAH[3]

toTex <- function(column, M){
  r <- vector()
  topN <- sort(as.vector(column), decreasing = TRUE)[5]
  for(v in column){
    c <- as.integer(v)
    if(c == 0){
      r <- c(r, "\\emptyDot{}")
    } else if(c == 1){
      r <- c(r, "\\oneDot{}")
    } else if ((c < M) & (c > 0)){
      r <- c(r, "\\belowMdot{}")
    } else if ((c >= M) & (c < topN)) {
      r <- c(r, "\\greaterMdot")
    } else r <- c(r, "\\topNdot{}")
  }
 r
}

column = list() 
for (i in 1:length(books))
    column <- toTex(union$books[i], qBookMedian[i])
# craftColumn <- toTex(union$Craft, qCraftMedian)
# pihColumn <- toTex(union$PIH, qPIHMedian)
# rwhColumn <- toTex(union$RWH, qRWHMedian)
# lyahColumn <- toTex(union$LYAH, qLYAHMedian)

res <- cbind(union$Term)
for (c in column)
    res <- cbind(res, data.frame(c))
# res <- cbind(union$Term, data.frame(craftColumn))
# res <- cbind(res, data.frame(pihColumn))
# res <- cbind(res, data.frame(rwhColumn))
# res <- cbind(res, data.frame(lyahColumn))

names(res) <- c("Term", books)
#names(res) <- c("Term", "Craft", "PIH", "RWH", "LYAH")

#print(xtable(res, label=paste('F:unionTopFrequenciesVisual', sep = ""), 
#             caption="Union of TOP 30 frequent terms from the books. empty cell - no occurrence in the given book.
#        \\oneDot{} -- frequency is 1.
#        \\belowMdot{} -- below median but larger than 1.
#        \\greaterMdot{} -- greater or above median.
#        \\ensuremath{\\topNdot{}} -- in the top 5.", latex.environment="center"),
#      file="unionTopFrequenciesVisual.tex",
#      sanitize.text.function = function(x){x},
#      scalebox=0.8, include.rownames=FALSE,  
#      rotate.colnames=FALSE)

write.csv(res, paste(dataRoot, "/allbooks/", "unionTopFrequenciesVisual.csv", sep=""), row.names=FALSE)
