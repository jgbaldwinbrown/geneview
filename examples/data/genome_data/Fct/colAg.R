#######################################
## Computations on Column Aggregates ##
#######################################
## Author: Thomas Girke
## Last update: June 4, 2009
## Utility: convenience function for applying a variety of computations 
## on any combination of column aggregates in a matrix or data frame. 
## How to run the function:
## 	myMA <- matrix(rnorm(100000), 10000, 10, dimnames=list(1:10000, paste("C", 1:10, sep="")))
## 	colAg(myMA=myMA, group=c(1,1,1,2,2,2,3,3,4,4), myfct=mean)[1:4,]	

## Define the colAg() function 
colAg <- function(myMA=myMA, group=c(1,1,1,2,2,2,3,3,4,4), myfct=mean, ...) {
        myList <- tapply(colnames(myMA), group, list)
        names(myList) <- sapply(myList, paste, collapse="_")
        myMAmean <- sapply(myList, function(x) apply(myMA[,x], 1, myfct, ...))
        return(myMAmean)
}

