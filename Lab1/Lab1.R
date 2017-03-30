coin = read.csv("cointoss.csv")

plot(percentones~nruns, xlab = 'Nruns', ylab = 'Percentones', data = coin)
with(data, text(percentones~nruns, labels = row.names(data), pos = 4))

plot(percentones~maxrunlength, xlab = 'Max run lenght', ylab = 'Percentones', data = coin)
with(data, text(percentones~maxrunlength, labels = row.names(data), pos = 4))

plot(nruns~maxrunlength, xlab = 'Max run lenght', ylab = 'Nruns', data = coin)
with(data, text(nruns~maxrunlength, labels = row.names(data), pos = 4))