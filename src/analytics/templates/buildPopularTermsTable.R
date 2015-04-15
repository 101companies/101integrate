library("xtable")

dataRoot <- "../../data"

"topFrequencyWBPP" <- read.csv(paste(dataRoot, "/perbook/", "WBPP","/topFrequency.csv", sep=""))

"frequencyWBPP" <- read.csv(paste(dataRoot, "/perbook/", "WBPP","/frequenciesMerged.csv", sep=""), sep=";")

"frequencyWBPP" <- subset("frequencyWBPP", select=c(0,3))


#take union of TOP terms across all books
all <- rbind(
"topFrequencyWBPP")
union <- data.frame(sort(unique(all\$Term), decreasing = FALSE))
names(union) <- c("Term")
v <- data.frame(vector(mode = "integer",length(union\$Term)),stringsAsFactors = FALSE) 

#initialize columns per book with default values
union <- cbind(union, v)


names(union) <- c("Term", "WBPP")
row.names(union) <- seq(nrow(union))
union\$Term <- as.character(union\$Term)
union <- union[with(union, order(union\$Term)),]

for(t in union\$Term) if(t %in% as.vector("frequencyWBPP"\$Term)) union[which(union\$Term == t),2] <- "frequencyWBPP"[which("frequencyWBPP"\$Term == t),2]


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

qWBPP <- as.vector(quantile(union\$WBPP))
qWBPPMedian = qWBPP[3]



\toTex  functioncolumn M
  r  vector
  topN  sortas.vectorcolumn decreasing  TRUE5
  forv in column
    c  as.integerv
    ifc  0
      r  cr emptyDot
 else ifc  1
      r  cr oneDot
 else if c  M & c  0
      r  cr belowMdot
 else if c  M & c  topN 
      r  cr greaterMdot
 else r  cr topNdot
 r


WBPPColumn <- toTex(union\$WBPP, qWBPPMedian)


res <- cbind(union\$Term)

res <- cbind(res, data.frame(WBPPColumn))



names(res) <- c("Term",)



#print(xtable(res, label=paste('F:unionTopFrequenciesVisual', sep = ""), 
#             caption="Union of TOP 30 frequent terms from the books. empty cell - no occurrence in the given book.
#        \oneDot{} -- frequency is 1.
#        \belowMdot{} -- below median but larger than 1.
#        \greaterMdot{} -- greater or above median.
#        \ensuremath{\topNdot{}} -- in the top 5.", latex.environment="center"),
#      file="unionTopFrequenciesVisual.tex",
#      sanitize.text.function = function(x){x},
#      scalebox=0.8, include.rownames=FALSE,  
#      rotate.colnames=FALSE)

write.csv(res, paste(dataRoot, "/allbooks/", "unionTopFrequenciesVisual.csv", sep=""), row.names=FALSE)