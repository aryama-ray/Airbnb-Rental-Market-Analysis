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

![fig7](https://github.com/user-attachments/assets/b247f047-8e7d-4653-b675-88b73ad8d4ff)

### 4.4. Review Analysis
The project aims to analyze host performance and recommendation for potential Airbnb hosts based on review score ratings. Figure 9 shows the review score summary and distribution across West Region States.
##### Figure 9
![fig8](https://github.com/user-attachments/assets/40a2ff14-897b-498c-a44c-942febc0de37)

The average review score for Airbnb rentals is 4.8 on a scale of 0 to 5, with scores ranging from a minimum of 0 to a maximum of 5. Distribution plot shows that the rating is left skewed. Also, the distribution for the number of reviews is right skewed. This plot suggests that visitors to the rentals mostly avoid giving reviews and whenever they do, they mostly end up giving higher review ratings.

### 4.5. Top 10 Listing Analysis
We performed analysis to understand the number of active rentals and rental listings across cities and neighborhoods. Top 10 analyses were performed with various features to understand the distribution of rentals. Figure 10 shows the top 10 cities based on the number of Airbnb rentals.
##### Figure 10
![fig10](https://github.com/user-attachments/assets/5ca373fd-ba27-4966-914a-fc8fbdb73b77)

Los Angeles has the highest number of Airbnb rentals followed by San Diego and San Francisco. Figure 11 shows rentals distribution across the various neighborhoods.
##### Figure 11
![image](https://github.com/user-attachments/assets/ee94af7c-89b8-4efc-9e19-76a3babe2e0b)


The San Jose neighborhood has the highest number of rentals followed by Mission Bay and Long Beach. Figure 12 shows the rental distribution for hosts.
##### Figure 12
![image](https://github.com/user-attachments/assets/f8a308c3-79cc-4404-bf27-225742ede854)

Blueground has the highest number of rentals hosted on the Airbnb platform followed by “Roompicks” and “Michael”. Figure 13 shows the average number of listings on Airbnb by various hosts. Hosts can have both active and inactive listings.
##### Figure 13
![image](https://github.com/user-attachments/assets/91a67f64-ae1c-47d7-a76f-b26d985892b4)
Though Blueground has the highest number of rentals, Figure 13 shows that “RoomPicks by Victoria” has the highest average listings on the Airbnb platform followed by “LuxurybookingsFZE”. Listing- count-wise, “Blueground” comes third in the list.

### 4.6. Neighborhood-wise Analysis
There is a huge average rental price difference between expensive and inexpensive neighborhoods hosted by Airbnb. Figure 14 shows the top 10 and bottom 10 expensive neighborhoods in terms of the average rental price in those neighborhoods.
##### Figure 14
![image](https://github.com/user-attachments/assets/007dde37-b301-40a9-8da7-7a3c30324f0c)

The Bel-Air neighborhood has the most expensive Airbnb rental properties in the West Coast states. The rental price in this location is above $2500 per night. Malibu and Beverly Crest also have expensive rentals, with a price of around $1500 per night. Compared to these expensive rentals, Colma, Tijuana River Valley, and Watts have the most inexpensive rentals. Figure 15 shows more details on these expensive rentals.

##### Figure 15
![image](https://github.com/user-attachments/assets/6573ea8c-772b-4e53-90cd-7dc2d070b1b9)

### 4.7. Host-Related Listing Analysis
From the descriptive summary it was found that Airbnb has more non-superhosts than superhosts. However, more superhosts have their listings in the most expensive neighborhoods compared to non- superhosts, which indicates they might earn more revenue out of these listings.
#### Figure 16
![image](https://github.com/user-attachments/assets/06880ec2-9ca3-47c7-b59c-a5be86158816)

More detailed analysis as shown in Figure 17 elaborates the fact that superhosts have more listings in most expensive neighborhoods like Bel-Air, Beverly Crest, Malibu and Hollywood Hills West.
##### Figure 17
![image](https://github.com/user-attachments/assets/515e206a-1910-45b2-ab23-0c1df20389a0)

However, the bottom 10 inexpensive neighborhoods tell the opposite story. Figure 18 shows the listing count from both host types in the bottom 10 low-cost neighborhood.

##### Figure 18
![image](https://github.com/user-attachments/assets/c12ecb66-ce81-4b35-a0aa-e279bc109f86)

A greater number of hosts without superhost status have their listing in the bottom 10 low-cost neighborhoods. The lowest-cost neighborhood, Peralta-Laney, does not have any listing from a superhost.

### 4.8. Host Status-wise Performance Analysis
The project analyzed performance of the rentals based on their yearly occupancy rate and monthly occupancy rate by both types of hosts. In the cities where price for the rentals are higher, we analyzed the yearly and monthly occupancy rate for each type of host. Figure 19 shows the distribution comparison of yearly and monthly occupancy rate for each of the highest grossing cities and for each type of hosts.
##### Figure 19
![image](https://github.com/user-attachments/assets/9c994bec-8048-4cc6-9ab0-318ecebaab6e)

Monthly occupancy rate per city shows that rentals hosted by both superhosts and non-superhosts have similar median occupancy rates. However, minimum occupancy rates are high for the rentals hosted by superhosts. This indicates that the minimum number of nights stayed in the rentals hosted by a superhost are more than those hosted by non-superhosts.
Based on the derived feature Monthly Revenue Per Rental, which was derived based on occupancy rate and price, we analyzed rentals’ performance hosted by both types of hosts in each state. Analysis shows that in all the states, California, Oregon, and Washington, superhosts are earning more monthly revenue from their hosted rentals compared to non-superhosts. Figure 20 shows the monthly revenue per state by both types of hosts.

##### Figure 20
![image](https://github.com/user-attachments/assets/bf0ad8fa-1708-46ec-a1bb-e1c7c196d37e)

Also, superhosts are earning more average monthly revenue from rentals in each city compared to the rentals hosted by non-superhosts. Figure 21 shows average monthly revenue per rentals by cities for both types of hosts.

##### Figure 21
![image](https://github.com/user-attachments/assets/e7895b28-f2c4-450b-a3ff-d6059db6cfc3)

### 4.9. Correlation and Heatmap
We performed correlation analysis on the numerical features. Figure 22 shows the heatmap for the numeric feature correlation coefficient. Darker colors in the plot signifies higher correlation.

##### Figure 22
![image](https://github.com/user-attachments/assets/569be44b-b589-4014-b6dd-398f441ec543)

Analysis shows that various review-related features are highly correlated with each other. Similarly, rental features such as ‘accommodates’, ‘bedrooms’, ‘bathrooms’, and ‘beds’ are highly correlated with each other. Revenue-related features are positively correlated with occupancy rates and price and negatively correlated with various availability features.

### 4.10.Popular Property descriptions words by Host across various cities
The dataset includes a description feature associated with each rental, which hosts use to highlight details about their properties. Word cloud analysis reveals that this feature emphasizes key attractions and tourist interests when selecting rentals in a specific location. Figure 18 presents the word cloud for Monterey, California, a destination renowned for attractions such as Pacific Grove, Monterey Bay, and Pebble Beach. Visitors frequently choose this area to experience the ocean and stay in accommodations with ocean views.


### 4.11 EDA Conclusion
Key findings from exploratory data analysis are:
1. Superhosts focus on high-end neighborhoods with significant investments in luxury properties.
2. Non-superhosts cater to budget-conscious guests and dominate areas with low rental costs.
3. Review score is not impacted by superhost status, but booking of rental properties is impacted by
the host status. Superhosts get a higher number of bookings compared to non-superhosts.
4. More hosts may be encouraged to achieve Superhost status as superhosts tend to earn higher
revenue from their listings.


