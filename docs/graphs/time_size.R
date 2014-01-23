args <- commandArgs(trailingOnly = TRUE)

data <- read.csv(file=sprintf("../simulations/%s.csv", args[1]), head=TRUE, sep=",", comment.char = "#")

png(sprintf("../images/%s.png", args[1]))

data = aggregate(data[c("opt","noOpt")],list(size = data$size),mean)

plot(spline(data$size, data$opt, method="natural"), type="l", main="Wykres zależności czasu przejazdu\nod rozmiaru sieci drogowej", col="red", xlab="Rozmiar sieci drogowej [ulica]", ylab="Całkowity czas przejazdu [krok symulacji]")
lines(spline(data$size, data$noOpt, method="natural"), type="l", col="blue")
legend('topleft', legend=c("Optymalizacja", "Brak optymalizacji"), lty=c(1,1), col=c("red", "blue"))

dev.off()

png(sprintf("../images/%s_diff.png", args[1]))

diff = (data[["opt"]] - data[["noOpt"]]) * 100 / data[["noOpt"]]

plot(spline(data$size, diff, method="natural"), type="l", main="Wykres zależności różnicy bezwzględnej czasów przejazdu\nod rozmiaru sieci drogowej", col="green", xlab="Rozmiar sieci drogowej [ulica]", ylab="Różnica bezwzględna czasu przejazdu [%]")
legend('topleft', legend=c("Różnica bezwzględna"), lty=c(1), col=c("green"))

dev.off()

tableFile = sprintf("../tables/%s.tex", args[1])
write("\\begin{table}[H]", file=tableFile)
write("\\begin{tabular}{ | C{4cm} | C{4cm} | C{4cm} | }", file=tableFile, append=TRUE)
write("\\hline", file=tableFile, append=TRUE)
write("Rozmiar sieci drogowej [ulica] & Optymalizacja [krok symulacji] & Brak optymalizacji [krok symulacji] \\\\ \\hline", file=tableFile, append=TRUE)
write.table(data, file=sprintf("../tables/%s.tex", args[1]), row.names=FALSE, col.names=FALSE, sep=" & ", eol=" \\\\ \\hline\n", append=TRUE)
write("\\hline", file=tableFile, append=TRUE)
write("\\end{tabular}", file=tableFile, append=TRUE)
write("\\caption{Zależność czasu przejazdu od rozmiaru sieci drogowej.}", file=tableFile, append=TRUE)
write("\\end{table}", file=tableFile, append=TRUE)