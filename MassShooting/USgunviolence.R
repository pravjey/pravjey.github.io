usgunviol <- read.csv("e:/Data Science projects/US Gun violence/gun-violence-data_01-2013_03-2018.csv")

names(usgunviol)

#The Gun Violence Archive has identified 239,677 incidents of gun violence between 2013 and 2018 

nrow(usgunviol)


#Number of gun deaths, non-fatal injuries and injuries (fatal & non-fatal)

sum(usgunviol$n_killed)
sum(usgunviol$n_injured)
sum(usgunviol$n_killed) + sum(usgunviol$n_injured)

mean(usgunviol$n_killed)
mean(usgunviol$n_injured)
(sum(usgunviol$n_killeed) + sum(usgunviol$n_injured)) / nrow(usgunviol)

mode_killed <- sort(table(usgunviol$n_killed))
mode_injured <- sort(table(usgunviol$n_injured))
n_allinjuries <- data.frame(usgunviol$n_killed + usgunviol$n_injured)
table(n_allinjuries)
mode_allinjured <- sort(table(n_allinjuries))

mode_killed
mode_injured
mode_allinjured

plot(mode_killed)
plot(mode_injured)
plot(mode_allinjured, main = "Outcome of gun violence incidents",
     xlab = "Number of fatal and non-fatal injuries",
     ylab = "Frequency")

citation()


# How many mass shootings

table(n_allinjuries)
sort(mode_allinjured)

# How many mass shootings (at least 4 deaths or injuries)
sort(mode_allinjured[1:24])
sum(sort(mode_allinjured[1:24]))

# How many mass shootings (at least 3 deaths or injuries)
sort(mode_allinjured[1:25])
sum(sort(mode_allinjured[1:25]))

# How many mass shotings (at least 5 deaths or injuries)
sort(mode_allinjured[1:23])
sum(sort(mode_allinjured[1:23]))

# The variability between different definitions of mass shooting

y <- (0)
x <- as.integer(names(sort(mode_allinjured[1:i])))
for (i in seq(1,25)) {
  massshooting <- sum(sort(mode_allinjured[1:i]))
  y <- c(y, massshooting)
}
y <- y[2:26]
x
plot(x,y,main = "The variability in number of mass shootings based on definition", xlab = "Number of victims", ylab = "Number of mass shootings")

median(x)
mean(x)
quantile(x)
var(x)
sd(x)

#Where and when did mass shooting take place in the last 5 years?

massshooting_state <- table(usgunviol$state[usgunviol$n_killed + usgunviol$n_injured > 14])
massshooting_state
sum(massshooting_state)

mass_dates <- usgunviol$date[usgunviol$n_killed +  usgunviol$n_injured > 14]
mass_states <- usgunviol$state[usgunviol$n_killed +  usgunviol$n_injured > 14]
mass_deaths <- usgunviol$n_killed[usgunviol$n_killed +  usgunviol$n_injured > 14]
mass_injured <- usgunviol$n_injured[usgunviol$n_killed +  usgunviol$n_injured > 14]
mastates_dates <- data.frame(mass_dates, mass_states,mass_deaths+mass_injured)
states_dates
colnames(states_dates) <- c("Date of event", "State", "Deaths and injuries")

names(usgunviol)
head(usgunviol$date)

usgunviol$incident_characteristics[usgunviol$date == states_dates$`Date of event`]

table(usgunviol$date == states_dates$`Date of event`)


