# Classification of Ecoli Dataset

Having studied Machine learning, I chose this project primarily because I wanted to learn how to build a program that could classify data into categories efficiently and accurately. I have always had an layperson's interest in science and medical technology. But I had no prior domain knowledge of ecoli and relied completely on the description file provided in order to understand the dataset by observation. The purpose of this project was to identify the most important features and the maximum number of features need to achieve an accurate classification and evaluate the resultant decision tree.

The program was written using Python and the following libraries were used: matplotlib, mpl_toolkits.mplot3d, pandas, sklearn, tabulate and time.

The project/program can be split into the following sections:

	_Initial section_		  

	1. Read dataset as a text file
	
	2. Count the length of the dataset, the number of characters per line and the number of lines
	
	This shows whether the dataset has been read as one would expect from a visual inspection and therefore gives an indication of how it should be cleaned.
	
	_Data cleaning_
	
	The dataset is cleaned as outlined in the following blog post:
	
	(https://pravinjeyaraj.wordpress.com/2019/05/04/cleaning-the-ecoli-dataset-using-python/)	
	
	_Feature Selection_
	
	After cleaning, the dataset is stored in a dataframe so that the number of classes can be indentified and the features can be ranked, using the Extra Trees Method. It is observed that the results of the ranking function vary between function calls, so that the importance of some features change depending on the function call. Bagging and averaging is thus used to calculate in order to reduce the executional variance and calculate the relative importance of each feature.
	
	_Model Building and Evaluation_
	
	A decision tree was created using the feature with highest relative importance and the accuracy of the model was assessed by splitting the dataset into a training and test set, using the holdout method. However, the problem was to identify how the training set should be in order to achieve the highest accuracy. So the model building was repeated nine times using test sets that were 10% to 90% of the dataset. It was found that the accuracy ws highest when the test set size was 10% to 30% of the dataset, with the highest being at 30%. Once the test set became larger than this, the accuracy dropped significantly, presumably because there was not enough data in the training set to build a good model.
	
	However, even with a test set of 30%, the accuracy rate using only the most important feature was just 68%. There was clearly room to improve.
	
	The second stage was thus identify how many features were needed and the resulting accuracy, with a test set size of 30%. In order to select the features to be used, a threshold was set from 10% to 90% of the relative importance of the most important feature. The lower the threshold, the most features were selected. The output was a table showing the threshold, resultant accuracy and the features used. It was found that the highest accuracy was obtained when four or five features were used, at over 80%.
	
	The third stage was then to work out whether there was any computational advantage of using five features over four. This involved repeating the second stage, with the time taken for building the model at each threshold point being measured.
	
	The output for the Feature Selection and Model Building and Evaluation stages were in table and graph forms. The findings and graphs are presented in the following blog post:
	
	(https://pravinjeyaraj.wordpress.com/2019/10/23/feature-selection-in-the-ecoli-dataset/)	
	
The full code is available from [Github](https://pravjey.github.io/Ecoli/ml-ecoli.py)

[Back to Portfolio page](https://pravjey.github.io/portfolio/archive.html)




