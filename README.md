# 1. Introduction
The Airbnb rental market on the West Coast of the United States is diverse, encompassing a wide range of property types, pricing strategies, and guest preferences across neighborhoods. With increasing competition and a growing number of hosts joining the platform, understanding the factors driving performance metrics such as pricing, availability, review scores, and property types has become crucial. Data-driven insights can empower hosts to adapt to market dynamics, enhance guest satisfaction, and improve profitability, while also helping Airbnb maintain host loyalty and platform trust. The primary goal is to deliver actionable insights that enable Airbnb hosts to better understand rentals’ performance and guest preferences, to build recommendation systems for potential hosts to maximize revenue from the rentals, and to identify trends across neighborhoods. The study uses a comprehensive dataset of over 91,000 Airbnb listings from key counties in California, Oregon, and Washington, comprising 75 features related to host details, property attributes, and market performance.

# 2. Data Source
The dataset used in this project is sourced from an open-source Airbnb dataset containing information on over 91,000 listings from key regions in California, Oregon, and Washington. 

Reference Link : https://insideairbnb.com/get-the-data/

# 3. Data Preprocessing
From a pool of Airbnb listings data, we considered all listings from the counties of California (8 counties), Oregon (2 counties) and Washington (1 county). All of these listings files are in CSV format and have common features. We merged all of these files into one common file for further analysis. `
## 3.1. Descriptive Statistics
Performed initial descriptive statistics on numeric features from the dataset as shown in the figure 1.
##### Figure 1
![image](https://github.com/user-attachments/assets/ad55fa55-6e42-4a9f-a6b6-33b05de51f0a)
## 3.2. Data Cleaning and Transformation
The price column in the dataset was initially in string format with currency symbols. We converted the features into numeric format by removing the ‘$’ symbol using regex and converting the value into float type.
Some of the categorical variables contained URLs, such as those for host pictures and rental pictures. The presence of these URLs can attract customers and positively influence the performance of the rental. Therefore, these URL-related features were converted into Boolean-type features to indicate whether a URL was present for the corresponding attributes.
Features irrelevant to analysis, such as ‘id’, ‘scrape_id’, ‘neighbourhood_group_cleansed’, and URL fields were dropped from the dataset. Also, the presence of duplicate values in the dataset were checked.
## 3.3. Handling Missing Values
The merged dataset initially had null values in both numeric and text columns. Figure 2 shows the percentage of missing values in all columns having null values. We dropped the columns with more than 50% null values, like ‘calender_updated’ and ‘license’.
##### Figure 2
![image](https://github.com/user-attachments/assets/d82d8448-5cd9-4133-9101-4eb3eff3e098)


Null values in numerical and text fields were handled using different methods.
### A. Numerical Columns:
Missing values in numerical columns were imputed using subgroups. We used imputation logic implemented in the function impute_missing_values_subset_advanced_fixed, which used ‘group by’ for context-specific statistics, and we used global statistics if group-level statistics were unavailable. Continuous columns (e.g., ‘price’, ‘review_scores’) were imputed with median, and categorical numerical columns (e.g., ‘bathrooms’, ‘beds’) were imputed with mode.

### Text Columns:
Null values in textual columns were handled in three different ways.

1. String Replacement: Missing values were replaced with default placeholders (e.g., "Unnamed Listing" for name, "No Description Provided" for description).
2. Model-based Imputation: For fields like ‘host_response_time’ or ‘host_is_superhost’, the most frequent value was applied.
3. Drop Columns: Columns with excessive null percentages (>40%, e.g., ‘host_about’, ‘neighbourhood’) were removed.

## 3.4. Feature Engineering
### 3.4.1. City and State
The dataset contained latitude and longitude features, which were used to derive the City and State features for the hosted rentals. A Cartographic Boundary file from U.S. Census data was utilized to map the latitude and longitude to corresponding ‘city’ and ‘state’ values. This Cartographic data contains pre- loaded boundary data. We employed geopandas and shapely.geometry to access these shapefiles. The County shapefile for the US includes both state and county names. Figure 3 shows the snippet of the County shapefile used in this project for city and state name derivation.
##### Figure 3
![image](https://github.com/user-attachments/assets/9edb3979-9fa7-4a34-9840-cf95405733da)

We used ‘name’ from the County shapefile as city names and ‘state_name’ as state names. A spatial join was performed (gpd.sjoin) to associate coordinates with their corresponding city and state. This derivation amplified the quality of the data by identifying the correct location of the Airbnb rental locations.

### 3.4.2. URL Field transformation
All URL fields ('listing_url', 'picture_url', 'host_url', 'host_thumbnail_url', 'host_picture_url') were converted into binary indicators such as:
Presence: 1
Absence: 0
These feature names were renamed using the format <url-feature-name>_url_present, and the original
features were subsequently dropped.

### 3.4.3 Temporal Features
The dataset contained datetime features such as ‘host_since’, ‘first_review’, and ‘last_review’ in text format. We converted these features into datetime format and derived new features such as Hosting Tenure and Days Since First and Last Review.

### 3.4.4 Amenities Parsing
The amenities column, stored as a string of lists, was converted to a list. Based on the count of relevant amenities (e.g., "Self check-in", "Private entrance", "Wifi", "Air conditioning", "Heating" etc), ‘relevant_amenities_count’ feature was generated.

### 3.4.5 Bathrooms Text
The feature ‘bathrooms_text’ column is categorized into Private Bath or Shared Bath based on string parsing. Also, the original ‘bathrooms_text’ field was dropped.

### 3.4.6 Occupancy Rate
Two occupancy rate features, Year-Round Occupancy Rate and Monthly Occupancy Rate, were calculated using the following formulas:
![image](https://github.com/user-attachments/assets/437284a1-c23a-47ee-869f-ed10195e4d06)

These two metrics capture the percentage of days a property is occupied over an entire year and over an entire month respectively. The ‘availability_365’ feature represents the number of days a property is available for booking throughout the year, and the ‘availability_30’ feature represents the number of days the property is available for booking in the past 30 days. A higher occupancy rate indicates better utilization of the rental property and potentially higher profitability.

### 3.4.7 Revenue Per Rental
Annual Revenue Per Rental and Monthly Revenue Per Rental features were computed based on ‘year_round_occupancy_rate’ and ‘month_round_occupancy_rate’ respectively using following formulas:
![image](https://github.com/user-attachments/assets/03a495e1-10e6-4df0-a278-f85dd0effa2f)

These metrics estimate the annual revenue and monthly estimated revenue generated per rental property. These features provide an indication of the long-term and short-term earning potential of properties, which is crucial for financial planning and benchmarking performance across listings.


## 4. Exploratory Data Analysis
### 4.1. Summary Statistics
Descriptive statistics were performed for a few key numeric attributes. Figure 4 shows the descriptive statistics for ‘host_response_rate’, ‘host_acceptance_rate’, ‘host_listing_count’, ‘reviews_per_month’, and ‘host_since’.
##### Figure 4
![image](https://github.com/user-attachments/assets/f803b1cc-0e08-4bba-8ed7-2c419f56ac88)

This summary statistics shows that a median number of Airbnb hosts were hosting their rentals since 2016. On average, they have 76 listings on Airbnb. The average response rate is 96.9% whereas acceptance rate is 89.54%. Figure 8 shows the super host count on this platform.
There are 37,917 superhost listings compared to 53,190 non-superhost listings present in the West Coast. We also performed descriptive statistics on the number of reviews, price, and the minimum and maximum number of nights spent in these rentals. Figure 9 shows the summary of these statistics.

##### Figure 5
![image](https://github.com/user-attachments/assets/2e54084a-59d7-4d9b-a717-c4ab00d1e46b)

### 4.2. Price Analysis
Price is one biggest cost driver for the Airbnb rental performance. From descriptive statistics we found the average rental price is $254.78. However the price range varies from a minimum of $5 to a maximum of $59,000 in West Coast states. We analyzed the price feature further. Figure 6 shows the price distribution.
##### Figure 6
![image](https://github.com/user-attachments/assets/9717b2ca-a07e-409b-92a8-56a8dd7499ce)

Rental price was highly skewed after preprocessing of the data. We performed a log transformation to reduce the skewness in the data. Figure 11 shows the log transformed price distribution in a histogram plot. Figure 7 shows log transformed price distribution.
##### Figure 7
![image](https://github.com/user-attachments/assets/ac912a7d-088f-4ead-ac6d-bb6ccf74908d)

### 4.3. Property Type Analysis
We performed univariate analysis of property-type features to understand the distribution of different Airbnb rental properties across the West Coast region. Figure 8 shows the various property types for the current dataset. Analysis shows that the most listed property types are “Entire home” followed by “Entire rental unit”. The least listed property types are hotel rooms and private rooms in a condo.

##### Figure 8


