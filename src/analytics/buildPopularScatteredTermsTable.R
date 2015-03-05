library("xtable")

dataRoot <- "../../data"

books <- commandArgs(trailingOnly = TRUE)

topScattered = list()  
for (i in 1:length(books))
    topScattered <- read.csv(paste(dataRoot, "/perbook/", books[i] , "/topScattered.csv", sep=""))
#topScatteredCraft <- read.csv(paste(dataRoot, "/perbook/", "Craft/topScattered.csv", sep=""))
#topScatteredPih <- read.csv(paste(dataRoot, "/perbook/", "PIH/topScattered.csv", sep=""))
#topScatteredRhw <- read.csv(paste(dataRoot, "/perbook/", "RWH/topScattered.csv", sep=""))
#topScatteredLyah <- read.csv(paste(dataRoot, "/perbook/", "LYAH/topScattered.csv", sep=""))

scattered = list() 
for (i in 1:length(books))
    scattered <- read.csv(paste(dataRoot, "/perbook/", books[i],"/scattered.csv", sep=""), sep=",")
#scatteredCraft <- read.csv(paste(dataRoot, "/perbook/", "Craft/scattered.csv", sep=""), sep=",")
#scatteredPih <- read.csv(paste(dataRoot, "/perbook/", "PIH/scattered.csv", sep=""), sep=",")
#scatteredRwh <- read.csv(paste(dataRoot, "/perbook/", "RWH/scattered.csv", sep=""), sep=",")
#scatteredLyah <- read.csv(paste(dataRoot, "/perbook/", "LYAH/scattered.csv", sep=""), sep=",")

unionTopFrequencies <- read.csv(paste(dataRoot, "/allbooks/", "unionTopFrequencies.csv", sep=""), sep=",", stringsAsFactors=FALSE)
topFrequentTerms <- as.vector(unionTopFrequencies$Term)

for (s in scattered)
  s subset(s, subset=TRUE, select=c(1,2))
#scatteredCraft <- subset(scatteredCraft, select=c(1,2))
#scatteredPih <- subset(scatteredPih, select=c(1,2))
#scatteredRwh <- subset(scatteredRwh, select=c(1,2))
#scatteredLyah <- subset(scatteredLyah, select=c(1,2))

#take union of scattered terms across all books
all <- NULL
for (top in topScattered)
all <- rbind (all, top)
#all <- rbind(topScatteredCraft, topScatteredPih, topScatteredRhw, topScatteredLyah)
union <- data.frame(sort(unique(all$Term), decreasing = FALSE))
names(union) <- c("Term")
v <- data.frame(vector(mode = "integer",length(union$Term)))

#initialize columns per book with default values
union <- cbind(union, v)
union <- cbind(union, v)
union <- cbind(union, v)
union <- cbind(union, v)

names(union) <- c("Term", books)
#names(union) <- c("Term", "Craft", "PIH", "RWH", "LYAH")

for (s in scattered)
    for(t in union$Term) if(t %in% as.vector(s$Term)) union[which(union$Term == t),2] <- s[which(s$Term == t),2]
#for(t in union$Term) if(t %in% as.vector(scatteredCraft$Term)) union[which(union$Term == t),2] <- scatteredCraft[which(scatteredCraft$Term == t),2]
#for(t in union$Term) if(t %in% as.vector(scatteredPih$Term)) union[which(union$Term == t),3] <- scatteredPih[which(scatteredPih$Term == t),2]
#for(t in union$Term) if(t %in% as.vector(scatteredRwh$Term)) union[which(union$Term == t),4] <- scatteredRwh[which(scatteredRwh$Term == t),2]
#for(t in union$Term) if(t %in% as.vector(scatteredLyah$Term)) union[which(union$Term == t),5] <- scatteredLyah[which(scatteredLyah$Term == t),2]

write.csv(union, paste(dataRoot, "/allbooks/", "unionTopScatterness.csv", sep=""))

#print(xtable(union, caption="Union of the terms scattered more than over 80\\% of the chapters"),
#      file="unionTopScatterness.tex",
#      include.rownames=FALSE,  
#      rotate.colnames=FALSE)

#- One column per book showing popularity per book in a percentile-based manner:
#* empty cell = no occurrence in the given book
#* dot = frequency is 1
#* small circle = below median but larger than 1
#* big circle = greater or above median
#* biggest circle = in the top-n

qBook = list() 
qBookMedian <- book
for (i in 1:length(books)){
qBook[i] <- as.vector(quantile(union$(books[i])))
qBookMedian[i] = qBook[i][3]
}

#qCraft <- as.vector(quantile(union$Craft))
#qCraftMedian = qCraft[3]

#qRWH   <- as.vector(quantile(union$RWH))
#qRWHMedian <- qRWH[3]

#qPIH   <- as.vector(quantile(union$PIH))
#qPIHMedian <- qPIH[3]

#qLYAH  <- as.vector(quantile(union$LYAH))
#qLYAHMedian <- qLYAH[3]

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

checkTerms <- function(column, topFrequentTerms){
  v <- vector()
  for(t in as.vector(column)){
    if(t %in% topFrequentTerms){
      v <- c(v, paste("\\textbf{", t, "}", sep=""))
    } else {
      v <- c(v, t)
    }
  } 
  v
}

Y <- checkTerms(union$Term, topFrequentTerms)

column = list() 
for (i in 1:length(books))
  column[i] <- toTex(union$(books[i]), qBookMedian[i])
#craftColumn <- toTex(union$Craft, qCraftMedian)
#pihColumn <- toTex(union$PIH, qPIHMedian)
#rwhColumn <- toTex(union$RWH, qRWHMedian)
#lyahColumn <- toTex(union$LYAH, qLYAHMedian)

res <- cbind(Y)
for (c in column)
  res <- cbind(res, data.frame(c))
#res <- cbind(Y, data.frame(craftColumn))
#res <- cbind(res, data.frame(pihColumn))
#res <- cbind(res, data.frame(rwhColumn))
#res <- cbind(res, data.frame(lyahColumn))

names(res) <- c("Term", books)
#names(res) <- c("Term", "Craft", "PIH", "RWH", "LYAH")

#print(xtable(res, label=paste('F:unionTopScatternessVisual', sep = ""), 
#             caption="Union of TOP 30 scattered terms from the books. empty cell - no occurrence in the given book.
#        \\oneDot{} -- frequency is 1.
#             \\belowMdot{} -- below median but larger than 1.
#             \\greaterMdot{} -- greater or above median.
#             \\topNdot{} -- in the top 5.", latex.environment="center"),
#      file="unionTopScatternessVisual.tex",
#      scalebox=0.8,
#      sanitize.text.function = function(x){x},
#      include.rownames=FALSE,  
#      rotate.colnames=FALSE)
write.csv(res, paste(dataRoot, "/allbooks/", "unionTopScatternessVisual.csv", sep=""))

