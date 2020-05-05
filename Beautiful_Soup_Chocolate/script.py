import codecademylib3_seaborn
from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

cacao_response = requests.get("https://s3.amazonaws.com/codecademy-content/courses/beautifulsoup/cacao/index.html")
cacao_webpage = cacao_response.content

soup = BeautifulSoup(cacao_webpage, "html.parser")
# print(soup)

rating_tags = soup.find_all(attrs={"class": "Rating"})

ratings = []
for tag in rating_tags[1:]:
    ratings.append(float(tag.get_text()))
# print(ratings)

plt.hist(ratings)
# plt.show()

company_tags = soup.select(".Company")
# print(soup)

companies = []
for company in company_tags[1:]:
    companies.append(company.get_text())
# print(companies)

cocoa_percent_tags = soup.select(".CocoaPercent")
cocoa_percents = []
for percent in cocoa_percent_tags[1:]:
    cocoa_percents.append(float(percent.get_text().strip("%")))
# print(cocoa_percents)

cacao_dict = {"Company": companies, "Rating": ratings, "Cocoa Percentage": cocoa_percents}
cacao_df = pd.DataFrame.from_dict(cacao_dict)

mean_ratings = cacao_df.groupby("Company").Rating.mean()
ten_best = mean_ratings.nlargest(10)
# print(ten_best)

plt.clf()
plt.scatter(cacao_df["Cocoa Percentage"], cacao_df.Rating)
plt.show()

plt.clf()
z = np.polyfit(cacao_df["Cocoa Percentage"], cacao_df.Rating, 1)
line_function = np.poly1d(z)
plt.plot(cacao_df["Cocoa Percentage"], line_function(cacao_df["Cocoa Percentage"]), "r--")
plt.show()
