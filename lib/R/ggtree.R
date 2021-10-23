
args <- commandArgs(trailingOnly = TRUE)
print("Input", str(args))

library("ggtree")

Arg = strsplit(args, "##")[[1]]
INPUT = Arg[1]
Size_w = as.numeric(Arg[2])
Size_h = as.numeric(Arg[3])


tree <- read.tree(INPUT)

Num = 0
for( i in tree$tip.label){
  tmp = length(strsplit(i, "*")[[1]])
  if(tmp > Num)Num=tmp
}
ggtree(tree, branch.length = 'none') +
  geom_text2(aes(subset=!isTip, label=node), hjust= 1.5, vjust = -0.5) +
  geom_tiplab() +
  xlim(NA, 15 + Num)
ggsave(paste(INPUT, ".png", sep=""),
    width = Size_w, height = Size_h)
