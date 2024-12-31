Used Car Price Prediction for Indian Cars
Python Notebook Streamlit

##Overview To be able to predict used cars market value can help both buyers and sellers. There are lots of individuals who are interested in the used car market at some points in their life because they wanted to sell their car or buy a used car. In this process, it’s a big corner to pay too much or sell less then it’s market value.

In this Project, we are going to predict the Price of Used Cars using various features like Mileage,Seat Capacity, Selling_Price, Kms_Driven, Fuel_Type, Year etc. The data used in this project was scrapped from cardekho.com

Steps:
Creating a new Jupyter Notebook.
Data Scraping uisng web driver
Creating the Dataset.
Data Visualizations
Training the Models
Output of the Model

1. Creating a new Jupyter Notebook
To work on this project First we have created a new jupyter notebook file to implement all the codes in python for the project. We have started the notebook with the pre installed libraries.



2. Data Scraping using web driver
In this step we haev used the selenium web driver to navigate through the website and then we have used Beautiful Soup library to store the html content and then scraping the infromation from the stored Html file. This process is followed for different cities. The details scraped with this was Car Name, year , Mileage, Engine Cc, Power, Seats, Location, Price etc.


3.Creating the dataset
In this step we have stored the scraped data in a Data Frame and then we have converted that to a csv file.


4.Data Visualization
In this step have visulaized our data with the information we got about the diffent manufacturers car and from the different locations. The plots used were Bar graphs,Box Plots, Distribution Plots, Violin pLot etc


5. Training the Models
Here we have Trained the different Machine Learning models with our data. We have trained 8 diffeerent models in our training part and comapred the accuracies of the models and used the model with the best accuracy


6.Working of the Model on real-time user inputs
I recommend to install the following packages pip install streamlit Run the app.py in the anaconda prompt using streamlit run app.py then open the web-address displayed below.




. Thankyou!
