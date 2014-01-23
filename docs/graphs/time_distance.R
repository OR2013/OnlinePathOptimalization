args <- commandArgs(trailingOnly = TRUE)

data <- read.csv(file=sprintf("../simulations/%s.csv", args[1]), head=TRUE, sep=",", comment.char = "#")

png(sprintf("../images/%s.png", args[1]))

size = as.integer(data[1,]["size"])
data = aggregate(data[c("opt","noOpt")],list(distance = data$distance),mean)

plot(spline(data$distance, data$opt, method="natural"), type="l", main=sprintf("Wykres zależności czasu przejazdu\nod maksymalnej długości ulicy\n(rozmiar sieci drogowej = %s ulic)", args[2]), col="red", xlab="Maksymalna długość ulicy [m]", ylab="Całkowity czas przejazdu [krok symulacji]")
lines(spline(data$distance, data$noOpt, method="natural"), type="l", col="blue")
legend('topleft', legend=c("Optymalizacja", "Brak optymalizacji"), lty=c(1,1), col=c("red", "blue"))

dev.off()

png(sprintf("../images/%s_diff.png", args[1]))

diff = (data[["opt"]] - data[["noOpt"]]) * 100 / data[["noOpt"]]

plot(spline(data$distance, diff, method="natural"), type="l", main=sprintf("Wykres zależności różnicy bezwzględnej czasu przejazdu\nod maksymalnej długość ulicy\n(rozmiar sieci drogowej = %s ulic)", args[2]), col="green", xlab="Rozmiar sieci drogowej [ulica]", ylab="Różnica bezwzględna czasu przejazdu [%]")
legend('topleft', legend=c("Różnica bezwzględna"), lty=c(1), col=c("green"))

dev.off()

tableFile = sprintf("../tables/%s.tex", args[1])
write("\\begin{table}[H]", file=tableFile)
write("\\begin{tabular}{ | C{4cm} | C{4cm} | C{4cm} | }", file=tableFile, append=TRUE)
write("\\hline", file=tableFile, append=TRUE)
write("Maksymalna długość ulicy [m]& Optymalizacja [krok symulacji] & Brak optymalizacji [krok symulacji] \\\\ \\hline", file=tableFile, append=TRUE)
write.table(data, file=sprintf("../tables/%s.tex", args[1]), row.names=FALSE, col.names=FALSE, sep=" & ", eol=" \\\\ \\hline\n", append=TRUE)
write("\\hline", file=tableFile, append=TRUE)
write("\\end{tabular}", file=tableFile, append=TRUE)
write("\\caption{Zależność czasu przejazdu od maksymalnej długości ulicy.}", file=tableFile, append=TRUE)
write("\\end{table}", file=tableFile, append=TRUE)