coin = read.csv("cointoss.csv")

#plot(percentones~nruns, xlab = 'Nruns', ylab = 'Percentones', data = coin)
#with(coin, text(percentones~nruns, labels = row.names(coin), pos = 4))

#plot(percentones~maxrunlength, xlab = 'Max run lenght', ylab = 'Percentones', data = coin)
#with(coin, text(percentones~maxrunlength, labels = row.names(coin), pos = 4))

#plot(nruns~maxrunlength, xlab = 'Max run lenght', ylab = 'Nruns', data = coin)
#with(coin, text(nruns~maxrunlength, labels = row.names(coin), pos = 4))

plot(percentones~c(1:dim(coin)[1]), xlab = 'Index', ylab = 'Percentage of ones', data = coin)
with(coin, text(percentones~c(1:dim(coin)[1]), labels = row.names(coin), pos = 4))

plot(nruns~c(1:dim(coin)[1]), xlab = 'Index', ylab = 'Number of runs', data = coin)
with(coin, text(nruns~c(1:dim(coin)[1]), labels = row.names(coin), pos = 4))

plot(maxrunlength~c(1:dim(coin)[1]), xlab = 'Index', ylab = 'Maximal run length', data = coin)
with(coin, text(maxrunlength~c(1:dim(coin)[1]), labels = row.names(coin), pos = 4))
