#Initialize packages
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.model_selection as model_selection
from sklearn import linear_model
import sklearn.metrics as metrics
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.feature_selection import RFE
from sklearn.impute import KNNImputer
import warnings



#Read in data
df = pd.read_csv(r'C:\Users\Alex\Downloads\letterboxd\movie_data_final.csv')

#If revenue is less than $5000 set to NA
df.loc[df['revenue'] <= 5000,'revenue'] = np.nan
#Impute missing reveneue using KNN (ignoring date and name columns)
imputer = KNNImputer(n_neighbors=2)
df.iloc[: , 2:] = imputer.fit_transform(df.iloc[: , 2:])

#Drop columns that cause problems with the modeling aspect
df=df.drop(['Logged_Date','Name','Logged_Year'], axis=1)


######################## Transformations ######################## 

#Plot correlation matrix
corrMatrix = df.corr()
plt.subplots(figsize=(20,15))
sns_plot = sns.heatmap(corrMatrix,cmap="RdBu",annot=True)
fig = sns_plot.get_figure()
fig.savefig("jupyter_heatmap.png")


#Scale non-boolean features 
df[['Year','popularity','vote_average','vote_count','revenue','runtime','Rating','Logged_DOW','Logged_Month','Logged_Week','Daily_Movie_Count','Weekly_Movie_Count']] = StandardScaler().fit_transform(df[['Year','popularity','vote_average','vote_count','revenue','runtime','Rating','Logged_DOW','Logged_Month','Logged_Week','Daily_Movie_Count','Weekly_Movie_Count']])


#Plot potenitally problematic features
fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, sharey=True,figsize=(14,5))
sns.scatterplot(data=df,x="movie_sentiment",y="revenue",ax=ax1)
sns.scatterplot(data=df,x="runtime",y="revenue",ax=ax2)
sns.scatterplot(data=df,x="popularity",y="revenue",ax=ax3);

#Remove outliers and replace with mean
replace = df['runtime'].mean()
df.loc[df['runtime'] >= 2,'runtime'] = np.nan
df['runtime'] = np.where(df['runtime'].isna(),replace,df['runtime'])
#Same process but with popularity
replace = df['popularity'].mean()
df.loc[df['popularity'] >= 2,'popularity'] = np.nan
df['popularity'] = np.where(df['popularity'].isna(),replace,df['popularity'])

#Transform problematic columns
df['movie_sentiment'] = df['movie_sentiment']**(1./3.)

#Recode bad values to mean 
df.replace([np.inf, -np.inf], np.nan, inplace=True)
replace = df['movie_sentiment'].mean()
df['movie_sentiment'] = np.where(df['movie_sentiment'].isna(),replace,df['movie_sentiment'])

#Plot again to see change in features after transformation 
fig, (ax1, ax2, ax3) = plt.subplots(ncols=3, sharey=True,figsize=(14,5))
sns.scatterplot(data=df,x="movie_sentiment",y="revenue",ax=ax1)
sns.scatterplot(data=df,x="runtime",y="revenue",ax=ax2)
sns.scatterplot(data=df,x="popularity",y="revenue",ax=ax3);


############ Research Question: Which factors impact revenue the most? ############ 

#Train Test Split
X=df.drop('revenue', axis=1)
y=df[['revenue']]
X_train, X_test, y_train, y_test = model_selection.train_test_split(X,y,test_size=0.3, random_state=24)


###### 1.1 OLS ###### 
lm = linear_model.LinearRegression()  
lm.fit(X_train, y_train)
ols_fitted = lm.predict(X_test)

#Calculate R Squared
print("OLS R Squared: %s" % round(metrics.r2_score(y_test, ols_fitted),2))


###### 1.2  Elastic Net ###### 
search=model_selection.GridSearchCV(estimator=linear_model.ElasticNet(),param_grid={'alpha':np.logspace(-5,2,8),'l1_ratio':[.2,.4,.6,.8]},scoring='neg_mean_squared_error',n_jobs=1,refit=True,cv=10)
search.fit(X_train,y_train)
print(search.best_params_)

enet=linear_model.ElasticNet(normalize=True,alpha=0.001,l1_ratio=0.8)
enet.fit(X_train, y_train)
enet_fitted = enet.predict(X_test)

#Calculate R Squared
print("Elastic Net R Squared: %s" % round(metrics.r2_score(y_test, enet_fitted),2))


###### 1.3 RF ###### 
warnings.simplefilter("ignore")
nof_list=np.arange(1,37)            
high_score=0
nof=0           
score_list =[]
#Variable to store the optimum features
for n in range(len(nof_list)):
    X_train, X_test, y_train, y_test = model_selection.train_test_split(X,y,test_size=0.3, random_state=24)
    model = linear_model.LinearRegression()
    rfe = RFE(model,nof_list[n])
    X_train_rfe = rfe.fit_transform(X_train,y_train)
    X_test_rfe = rfe.transform(X_test)
    model.fit(X_train_rfe,y_train)
    score = model.score(X_test_rfe,y_test)
    score_list.append(score)
    if(score>high_score):
        high_score = score
        nof = nof_list[n]
print("Optimum number of features: %d" %nof)
print("Score with %d features: %f" % (nof, high_score))

#Optimum number of features: 35
#Score with 35 features: 0.645497

rf = RandomForestRegressor(max_features = 35, n_estimators=100)
rf.fit(X_train, y_train)
rf_fitted = rf.predict(X_test)

#Generate Feature Importance
rev_importance = {} # a dict to hold feature_name: feature_importance
for feature, importance in zip(X_train.columns, rf.feature_importances_):
    rev_importance[feature] = importance #add the name/value pair 
rev_importance = pd.DataFrame.from_dict(rev_importance, orient='index').rename(columns={0: 'Revenue_Importance'})

#Calculate R Squared
print("RF R Squared: %s" % round(metrics.r2_score(y_test, rf_fitted),2))


################### Feature Importance ###################

#Plot Feature Importance table
print(rev_importance.sort_values(by='Revenue_Importance', ascending=False))
#Plot as bar chart
rev_importance.sort_values(by='Revenue_Importance', ascending=False).plot(kind='bar', rot=45)
