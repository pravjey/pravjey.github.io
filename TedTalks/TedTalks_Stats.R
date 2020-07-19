tedtalks <- read.csv("../TedTalks/ted_main.csv/ted_main.csv")
names(tedtalks)
nrow(tedtalks)

#What are the most common occupations of speakers?
tail(sort(table(tedtalks$speaker_occupation)),20)
barplot(tail(sort(table(tedtalks$speaker_occupation)),10))

#Which Ted Talk events have the most number of speakers?
#Which country-specific Ted Talk event has the most number of speakers?
tail(sort(table(tedtalks$event)),20)

#How many days' worth of talks has been uploaded to TED.com website up until 21 September 2017?
sum(tedtalks$duration) / (60*60*24)

#What is the average (mean and median) duration of a talk in minutes?
mean(tedtalks$duration) / 60
median(tedtalks$duration) / 60

#What is the most common (mode) length of a talk in minutes?
as.numeric(names(sort(-table(tedtalks$duration)))[1]) / 60

#Who gave the longest TED Talk in minutes and what was it?
tedtalks$main_speaker[tedtalks$duration == max(tedtalks$duration)]
tedtalks$title[tedtalks$duration == max(tedtalks$duration)]
tedtalks$url[tedtalks$duration == max(tedtalks$duration)]
#Check
tedtalks$duration[tedtalks$main_speaker == "Douglas Adams"] / 60
max(tedtalks$duration) / 60

#Who gave the shortest TED Talk in minutes?
tedtalks$main_speaker[tedtalks$duration == min(tedtalks$duration)]
tedtalks$title[tedtalks$duration == min(tedtalks$duration)]
tedtalks$url[tedtalks$duration == min(tedtalks$duration)]
#Check
tedtalks$duration[tedtalks$main_speaker == "Murray Gell-Mann"] / 60
min(tedtalks$duration) / 60

#Is there any correlation between duration and number of views?
cor(tedtalks$duration, tedtalks$views)

#Is there any correlation between the number of comments and the duration or number of views of a talk
cor(tedtalks$duration, tedtalks$comments)
plot(tedtalks$duration, tedtalks$comments, xlab = "Duration", ylab = "Number of comments")
cor(tedtalks$views, tedtalks$comments)
plot(tedtalks$views, tedtalks$comments, xlab = "Number of views", ylab = "Number of comments")

#Who were the most prolific main speakers (in terms of number of talks)
tail(sort(table(tedtalks$main_speaker)),20)

#What was the average (mean and median) number of talks per speaker?
mean(table(tedtalks$main_speaker))
median(table(tedtalks$main_speaker))
sd(table(tedtalks$main_speaker))

#What was the most common number (mode) of talks per speaker?
table(table(tedtalks$main_speaker))[1]
  barplot(table(table(tedtalks$main_speaker)), xlab = "Number of talks", ylab = "Number of main speakers")




