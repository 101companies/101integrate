frequencies <- read.delim("~/Projects/101/101nonpublic/tools/icfp2012/books/RWH/frequencies.csv", header=F)
View(frequencies)
View(frequencies)
View(frequencies)
load("~/analytics/analytics.RData")
# Sort by freqencies in RWH in a descending order
data = frequencies[order(-frequencies$V2),]
# Plot RWH frequencies with nice axis labels
plot(data$rhw, log="y", xlab="Terms", ylab="Frequencies (log.)")
# Add points of two other sources, each time in different colour and shape of the point
points(sortedByRwh$V3, col="red", pch=17)
points(sortedByRwh$V4, col="green", pch=3)
points(data$V4, col="green", pch=3)
# Sort by freqencies in RWH in a descending order
data = frequencies[order(-frequencies$V2),]
# Plot RWH frequencies with nice axis labels
plot(data$rhw, log="y", xlab="Terms", ylab="Frequencies (log.)")
# Add points of two other sources, each time in different colour and shape of the point
points(data$V3, col="red", pch=17)
points(data$V4, col="green", pch=3)
plot(data$V2, log="y", xlab="Terms", ylab="Frequencies (log.)")
points(data$V3, col="red", pch=17)
points(data$V4, col="green", pch=3)
# Sort by freqencies in RWH in a descending order
data = frequencies[order(-frequencies$V2),]
# Plot RWH frequencies with nice axis labels
plot(data$V2, log="y", xlab="Terms", ylab="Frequencies (log.)")
# Add points of two other sources, each time in different colour and shape of the point
points(data$V3, col="red", pch=17)
points(data$V4, col="green", pch=3)
View(data)
View(data)
View(data)
View(data)
View(frequencies)
View(frequencies)
frequencies <- read.delim("~/projects/101nonpublic/tools/icfp2012/books/RWH/frequencies.csv", header=F)
View(frequencies)
View(frequencies)
View(frequencies)
load("~/analytics/analytics.RData")
# Sort by freqencies in RWH in a descending order
data = frequencies[order(-frequencies$V2),]
# Plot RWH frequencies with nice axis labels
plot(data$rhw, log="y", xlab="Terms", ylab="Frequencies (log.)")
# Add points of two other sources, each time in different colour and shape of the point
points(sortedByRwh$V3, col="red", pch=17)
points(sortedByRwh$V4, col="green", pch=3)
points(data$V4, col="green", pch=3)
# Sort by freqencies in RWH in a descending order
data = frequencies[order(-frequencies$V2),]
# Plot RWH frequencies with nice axis labels
plot(data$rhw, log="y", xlab="Terms", ylab="Frequencies (log.)")
# Add points of two other sources, each time in different colour and shape of the point
points(data$V3, col="red", pch=17)
points(data$V4, col="green", pch=3)
plot(data$V2, log="y", xlab="Terms", ylab="Frequencies (log.)")
points(data$V3, col="red", pch=17)
points(data$V4, col="green", pch=3)
# Sort by freqencies in RWH in a descending order
data = frequencies[order(-frequencies$V2),]
# Plot RWH frequencies with nice axis labels
plot(data$V2, log="y", xlab="Terms", ylab="Frequencies (log.)")
# Add points of two other sources, each time in different colour and shape of the point
points(data$V3, col="red", pch=17)
points(data$V4, col="green", pch=3)
View(data)
View(data)
source('~/.active-rstudio-document')
source('~/.active-rstudio-document')
source('~/.active-rstudio-document')
