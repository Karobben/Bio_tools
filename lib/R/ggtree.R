
args <- commandArgs(trailingOnly = TRUE)
print("Input", str(args))

library("ggtree")


tree <- read.tree(args)
ggtree(tree, branch.length = 'none') +
  geom_text2(aes(subset=!isTip, label=node), hjust= 1.5, vjust = -0.5) +
  geom_tiplab() +
  xlim(NA, 15 + length(strsplit(tree$tip.label[1], "*")[[1]])/2.5)
ggsave(paste(args, ".png", sep=""))
