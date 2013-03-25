library("xtable")
library("foreach")
library("igraph")
library("reshape")

a <- Sys.getlocale("LC_COLLATE")
print(a)
on.exit(Sys.setlocale("LC_COLLATE", a))
Sys.setlocale("LC_COLLATE", "en_US")

args <- commandArgs(trailingOnly = TRUE)
print(args)

folder <- args[1]
print(folder)

dataRoot <- "../../data"

frequencies <- read.csv(paste(dataRoot, "/perbook/", folder, "/frequenciesMerged.csv", sep=""), sep=";")
print(frequencies)
sorterFreq = frequencies[with(frequencies, order(-frequencies$Frequency)),]

#png(file='top30.png')
#mp <- barplot(sorterFreq$Frequency[0:30], main = "TOP 30 most frequent terms from the book", space = 0) 
#text(mp, 
#     par("usr")[3] - 0.025, 
#     srt = 45, 
#     adj = 1, 
#     labels = sorterFreq$Term[0:30], 
#     xpd = TRUE, 
#     font = 2)

#png(file=paste(folder, '/frequency.png', sep = ""))
#mp <- barplot(sorterFreq$Frequency, main = "Terms frequency distribution", space = 0) 
#text(mp, 
#     par("usr")[3] - 0.025, 
#     srt = 45, 
#     adj = 1, 
#     labels = NULL, 
#     xpd = TRUE, 
#     font = 2)
#dev.off()

#print(xtable(sorterFreq), include.rownames=FALSE, type='html', file=paste(folder, '/frequency.html', sep = ""))

top30 <-  subset(sorterFreq[0:30,], select=c(1,4))
row.names(top30) <- seq(nrow(top30))
top30 <- top30[order(top30$Term),]
#print(xtable(top30, label=paste('F:', folder, 'topFrequency', sep = ""), caption=paste("Top 30 terms from ", folder, sep = "")), include.rownames=FALSE, 
#      size="small", scalebox=0.7,
#      file=paste(folder, '/topFrequency.tex', sep = ""))

write.csv(top30, paste(dataRoot, "/perbook/", folder, '/topFrequency.csv', sep = ""))

print(folder)
frequenciesDistribution <- read.csv(paste(dataRoot, "/perbook/", folder, "/frequenciesDistributionMerged.csv", sep=""), sep=";", quote="\"")

#the following line should be uncommented if R studio is used
#frequenciesDistribution <- read.csv("~/projects/101nonpublic/tools/icfp2012/books/Craft/frequenciesDistributionmerged.csv",sep=";", quote="\"", head=TRUE)
#Z1 <- frequenciesDistribution[, 2:ncol(frequenciesDistribution)]

# getting scattered terms
getScatterPercent <- function(row) { 
  as.integer(round(sum((length(row[row != 0])) / length(row)*100))) 
}
res <- foreach(i=1:nrow(frequenciesDistribution), .combine=rbind) %do%
  getScatterPercent(frequenciesDistribution[i,4:ncol(frequenciesDistribution)])
row.names(res) <- seq(nrow(res))

terms <- data.frame(frequenciesDistribution$Term)
variations <- data.frame(frequenciesDistribution$Variations)
res <- cbind(terms, res)
res <- cbind(variations, res)
r <- data.frame(res)
sorterRes = r[with(r, order(-r$res)),]
row.names(sorterRes) <- seq(nrow(sorterRes))
#names(sorterRes) <- c("Variations", "Term", "Chapters (%)")


#attach(sorterRes)
#png(file=paste(folder, '/scattered.png', sep = ""))
#p <- plot(1:nrow(sorterRes), sorterRes$res, main="Scattered Terms", 
#     xlab="Terms", ylab="% of chapters", pch=19)
#dev.off()

#count those terms which are scattered more than 80%
#folder <- "Craft"
top20percent <- sorterRes[which(sorterRes$res >= 80),]  
row.names(top20percent) <- seq(nrow(top20percent))
top20percent <- subset(top20percent, select=c(2,3))
names(top20percent) <- c("Term", "Chapters (%)")

scattered <- subset(sorterRes, select=c(2,3))
names(scattered) <- c("Term", "Chapters")

#print(xtable(top20percent, label=paste('F:', folder, 'topScattered', sep = ""), caption=paste(folder,": terms scattered across more than 80\\% chapters", sep = "")),
#      file=paste(folder, '/topScattered.tex', sep = ""),
#      scalebox=0.7, include.rownames=FALSE)

names(top20percent) <- c("Term", "Chapters")
row.names(top20percent) <- seq(nrow(top20percent))
write.csv(top20percent, paste(dataRoot, "/perbook/", folder, '/topScattered.csv', sep = ""))
write.csv(scattered, paste(dataRoot, "/perbook/", folder, '/scattered.csv', sep = ""))
# end

rows.in.a1.that.are.not.in.a2  <- function(a1,a2){
  a1.vec <- apply(a1, 1, paste, collapse = "")
  a2.vec <- apply(a2, 1, paste, collapse = "")
  a1.without.a2.rows <- a1[!a1.vec %in% a2.vec,]
  return(a1.without.a2.rows)
}

#now we need to exclude those local terms which are already the most scattered (<80%)
frequenciesDistributionFiltered <-frequenciesDistribution[!frequenciesDistribution$Term %in% top20percent$Term,]
row.names(frequenciesDistributionFiltered) <- seq(nrow(frequenciesDistributionFiltered))

# getting local terms
getLocals <- function(col){
  sorted <- as.vector(sort(col, decreasing = TRUE))
  #pick the top-q most popular terms per chapter. Q = 3
  #top25 <- as.vector(quantile(col,.75,names = TRUE))
  sorted[5]
}

#terms <- fequenciesDistribution[1:nrow(frequenciesDistribution),1]
foo <- function(x, max){
  #print(max)
  #print(frequenciesDistribution$Term)
  y <- cbind(data.frame(frequenciesDistributionFiltered$Term), x)
  names(y) <- c("Term", "Frequency")
  z <- y[which((y$Frequency >max) & (y$Frequency > 0)),]  
  if(as.vector(dim(z))[1] > 0){
      row.names(z) <- seq(nrow(z))
      names(z) <- c("Term", "Frequency")
      z
  }
  else FALSE
}

bar <- function(i){
  print("Chapter #")
  print(i)
  v <- as.vector(frequenciesDistributionFiltered[1:nrow(frequenciesDistributionFiltered),i])
  #print(length(v))
  ns <- names(frequenciesDistributionFiltered)
  r <- foo(frequenciesDistributionFiltered[1:nrow(frequenciesDistributionFiltered),i], 
           getLocals(frequenciesDistributionFiltered[,i]))
  data.frame(x = names(frequenciesDistributionFiltered)[i],
             y = r)
}

res <- foreach(i=4:ncol(frequenciesDistributionFiltered), .combine=rbind) %do% #
  bar(i)

names(res) <- c("Chapter", "Term", "Frequency")  

#now we need to exclude those local terms which are already the most scattered (<90%)
localTerms <- res#res[!res$Term %in% top10percent$Term,]
#row.names(localTerms) <- seq(nrow(localTerms))
  
#x <- res[order(localTerms$Frequency),] # sort by Frequency
#x$chapter <- factor(x$Chapter) # it must be a factor  
#dotchart(x$Frequency,labels=x$Term,cex=.7,groups= x$Chapter,
#         main="Local terms per chapter",
#         xlab="Frequency", gcolor="red", color="black")

print(localTerms)

pv <- cast(localTerms, Term ~ Chapter)
pivot <- pv[order(pv$Term),]

#print(xtable(pivot))
#print(xtable(pivot, label=paste('F:', folder, 'chaptersProfile', sep = ""), caption=paste(folder,": chapter profiles. Top 5 terms per chapter (excluding TOP scattered terms)", sep = "")),
#      file=paste(folder, '/', folder, '.numbers', sep = ""),
#      include.rownames=FALSE, size="small", scalebox=0.3,
#      rotate.colnames=TRUE) #floating.environment='sidewaystable'


compareNA <- function(v1,v2) {
  # This function returns TRUE wherever elements are the same, including NA's,
  # and false everywhere else.
  same <- (v1 == v2)  |  (is.na(v1) & is.na(v2))
  same[is.na(same)] <- FALSE
  return(same)
}

toTex <- function(row, M, top5){
  r <- vector()
  for(v in row){
    if(compareNA(v,NA)){
      r <- c(r,NA)
    }else{
      c <- as.integer(v)
      print(c)
      if(c == 0){
        r <- c(r, "\\emptyDot{}")
      } else if(c == 1){
        r <- c(r, "\\oneDot{}")
      } else if ((c < M) & (c > 0)){
        r <- c(r, "\\belowMdot{}")
      } else if ((c >= M) & (c < top5) ) {
        r <- c(r, "\\greaterMdot{}")
      } else r <- c(r, "\\topNdot{}")
    }
  }
  r
}

pivot1 <- xtable(pivot)
pivot2 <- data.frame(pivot1)
pivot3 <- subset(pivot2, select=c(seq(2,ncol(pivot2))))
pivot4 <- data.matrix(pivot3)
pivot5 <- as.vector(pivot4)

top5 <- sort(as.vector(pivot5), decreasing = TRUE)[5]
m <- quantile(pivot5, na.rm = TRUE)[3]
print(m)

res <- NULL

for (index in 1:nrow(pivot3)) { 
  row = pivot3[index, ];
  tRow <- toTex(row, m, top5)
  #Some code that generates new row
  rbind(res,tRow)->res
} 
row.names(res) <- seq(nrow(res))
cn <- as.vector(names(pivot3))
res1 <- cbind(as.vector(pivot2$Term), res)
cn1 <- append(cn, "Term", after=0)
colnames(res1) <- cn1


#print(xtable(res1, label=paste('F:', folder, 'chaptersProfileVisual', sep = ""), caption=paste(folder,": chapter profiles. Top 5 terms per chapter (excluding TOP scattered terms)", sep = "")),
#      file=paste(folder, '/', folder, '.visual', sep = ""),
#      sanitize.text.function = function(x){x},
#      include.rownames=FALSE, size="small", scalebox=0.3,
#      rotate.colnames=TRUE)

#replacing NA with SPACE
pivot[is.na(pivot)] <- ' '
write.csv(pivot, paste(dataRoot, "/perbook/", folder, '/chapterProfile.numbers.csv', sep = ""))

#replacing NA with SPACE
res1[is.na(res1)] <- ' '
write.csv(res1, paste(dataRoot, "/perbook/", folder, '/chapterProfile.visual.csv', sep = ""))

#g <- graph.empty()

#median <- as.vector(quantile(union$Craft))[3]

# ------------