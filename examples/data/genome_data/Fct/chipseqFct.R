#########################################################
## Helper Functions for Analyzing ChIP-Seq Experiments ##
#########################################################
## Author: Thomas Girke
## Last update: 27-Oct-11

## (A) Function to append coverage information to peaks called by different methods
## The inputs are:
##            1. The peak ranges stored in an IRanges object (peaksIR) for single chromosome data, a 
##               list of IRanges for multiple chromosome data (list components named by chromosomes)
##               or a data frame with the 3 columns: chromosome/space names, start and end positions
##            2. The aligned reads stored as RangedData object (sig).
## For details see: http://manuals.bioinformatics.ucr.edu/home/ht-seq#TOC-BayesPeak
rangeCoverage <- function(summaryFct=viewMaxs, myname="sig_", peaksIR=bpeaksIR, sig=sig, readextend=200, normfactor) {
        require(ShortRead); require(chipseq)
        if(class(peaksIR)=="data.frame") {
		df2IRlist <- function(x) {
        		peaksIR <- IRanges(start=x[, 2], end=x[, 3])
        		peaksIR <- lapply(unique(x[,1]), function(y) IRanges(start=x[x[,1]==y,2], end=x[x[,1]==y,3]))
        		names(peaksIR) <- unique(unique(x[,1]))
        		return(peaksIR)
		}
		peaksIR <- df2IRlist(x=peaksIR)
	}
        if(is.list(peaksIR)==FALSE) { 
		peaksIR <- list(peaksIR)
		names(peaksIR) <- unique(names(sig))
        }
	covDF <- NULL
        for(i in names(peaksIR)) {
                sigsub <- as(sig, "GRanges")
		cov <- coverage(resize(sigsub, width = readextend)) * normfactor
                cov.pos <- coverage(resize(sigsub[strand(sigsub) == "+"], width = readextend)) * normfactor
                cov.neg <- coverage(resize(sigsub[strand(sigsub) == "-"], width = readextend)) * normfactor
                max.peak.cov <- unlist(summaryFct(Views(cov[[i]], peaksIR[[i]])))
                max.pos.peak.cov <- unlist(summaryFct(Views(cov.pos[[i]], peaksIR[[i]])))
                max.neg.peak.cov <- unlist(summaryFct(Views(cov.neg[[i]], peaksIR[[i]])))
                covtmp <- data.frame(space=i, cov=max.peak.cov, cov.pos=max.pos.peak.cov, cov.neg=max.neg.peak.cov)
                covDF <- rbind(covDF, covtmp)
        }
        colnames(covDF) <- paste(myname, colnames(covDF), sep="")
        return(covDF)
}
## Usage: 
## sigcovDF <- rangeCoverage(summaryFct=viewMeans, myname="sig_", peaksIR=peaksIR, sig=sig, readextend=200, normfactor=10^6/length(start(sig)))
## bgrcovDF <- rangeCoverage(summaryFct=viewMeans, myname="bgr_", peaksIR=peaksIR, sig=bgr, readextend=200, normfactor=10^6/length(start(bgr)))
## bpeaksDF <- cbind(bpeaks, sigcovDF[,-1], bgrcovDF[,-1]); bpeaksDF[1:4,]

