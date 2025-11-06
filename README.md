# Project 2: Electricity consumption in Scotland [40 marks]

The UK government releases open data about domestic electricity consumption every year, for all the different postcodes in the country. Each UK postcode typically contains 10-20 different houses or flats ([learn more about UK postcodes](https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom)), therefore it's possible to learn about electricity consumption at quite a precise geographical level.

In this project, you will use this data to explore electricity consumption across Scotland, and supplement it with other local data to investigate a topic of your choice. You will get started on the project during the **Week 8 workshop**.

---

## Goal and structure

The goal of this project is for you to present a **coherent and well-coded investigation** of a particular question or topic related to the data. You should do this in the Jupyter notebook called **`project-2-report.ipynb`**. The notebook should contain code cells, such that running all cells in your notebook produces all your results and your data visualisations. You should also use Markdown cells to structure the notebook, describe your investigations, and present/explain your results.

You should produce **one main data visualisation**, showing the key result(s) of your investigation. This will either be several plots or charts displayed together coherently in a single figure and which complement each other, or a single, more complex data visualisation combining multiple aspects of the data.

Before you get to this main result, you will clearly state your objectives and your topic of investigation, describe the datasets you will use, and explain the different steps of your investigation and data manipulation to the reader. You will tell the story of how you progressed towards answering your main question over the course of the project, explaining how you processed the data, and justifying the choices you have made in selecting or processing the data, and in structuring your code generally. You can display intermediate plots or results to clarify your explanations. If you have spent quite a lot of time trying something which didn't work as you expected in the end, you can also include this in your report, as long as it fits well with the overall story; if you do this, you should reflect on what went wrong and what else you would have tried if you had more time (if anything). Finally, after showing your main result, you should briefly discuss what you are observing, and how it helps to answer your question.

The section "A problem-solving example: the Post Office problem" in the Week 6 notebook is a (shorter) example of what your report could look like. It sets out the question at the start, states what data is available, and walks the reader through the different steps of writing code to answer the question, before presenting the final result. You really shouldn't try to match this example too closely; this is just to give you a rough idea of the general structure, scope, and level of detail that's expected. Of course, you will need to collaborate as a team to produce your final result, and your report should reflect this.

This project is an **open-ended** task, so you should come up with your **own ideas** to analyse the data and extract useful information or interesting insights. Some ideas of questions you might address in your analysis will be given in the section "Some ideas to get you started"; they are a guide to some things you could think about, but you are also strongly encouraged to come up with your own question(s) to investigate.

Your final report should present a coherent and professionally laid out narrative of how you worked as a team to produce your final result. Since you are working as a group, some work will be needed to combine all of the code and writing that you each contribute into the submitted notebook -- this is something that you should plan to do, and the quality of **presentation** will be marked. Note, in particular, that this is a **group project, and not a collection of small individual projects** -- your report should be coherent, and evidence that you have collaborated effectively.

---

## Data

### Main dataset: electricity consumption in 2023

The main dataset provided for this project is the file `Postcode_level_all_meters_electricity_2023.csv`, which can be downloaded using the following link:

`https://assets.publishing.service.gov.uk/media/6762f39cff2c870561bde826/Postcode_level_all_meters_electricity_2023.csv`

You can preview the content of the file on [this page](https://www.gov.uk/csv-preview/6762f39cff2c870561bde826/Postcode_level_all_meters_electricity_2023.csv). The data contains the total number of electricity meters in each postcode area, the total electricity consumption across all meters, and the average and median electricity consumption per meter, for each postcode in the UK over the year 2023 (all measured in kWh). You can assume that there is one electricity meter per household.

In your project, **you must use this dataset**, together with **at least one more dataset of your choice** to complement your investigation. Since we will focus on Scotland, one of your first tasks will be to select the data from Scottish postcodes from the dataset.

### Additional datasets

Here are some possible additional datasets that could be useful in your project:

- The main dataset gives electricity consumption by postcode. Some of these other datasets are also separated by postcode, but others are separated by slightly different types geographical areas (for example, the census data is given by "data zone"). There is a dataset available which allows you to match these different ways that the country is partitioned (for example, which postcode corresponds to which data zone): the [Scottish Statistics Postcode Lookup](https://www.nrscotland.gov.uk/publications/scottish-statistics-postcode-lookup/). It also gives you useful geographical information, for example the geographical coordinates of each postcode area.
- Scotland undertakes a census every 10 years, and publishes the results as open data. The [Scottish census data](https://www.scotlandscensus.gov.uk/) contains a lot of incredibly useful information.
    - You can [search the census data](https://www.scotlandscensus.gov.uk/search-the-census#/search-by) by topic or by location. When you've selected a topic, you can select "Census locality" or "data zone" for the geographical breakdown, as you will be able to match this to postcodes in the postcode lookup linked above. Then, click "Select all" when you get to the map, and you will arrive at a table. You can then download the table as an Excel spreadsheet, which you will then be able to read with pandas (see [`pd.read_excel()`](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html).
    - For example, the [housing data](https://www.scotlandscensus.gov.uk/search-the-census#/topics/list?topic=Housing&categoryId=3) includes accommodation type (i.e. how many households in a particular area are flats, houses, or something else), or how many houses in each area have different kinds of central heating (electric, gas, something else...). The [demographics data](https://www.scotlandscensus.gov.uk/search-the-census#/topics/list?topic=Demography%20and%20migration&categoryId=2) gives information about how many people live in each area (Household composition - People), and even more information about the demographics of the people there, across different characteristics.
- The Scottish Multiple Deprivation Index is an index which is calculated across Scotland to say something about the overall socio-economic deprivation in different areas. The most common ways the SIMD is used, is either by referring to the decile (an index from 1 to 10) or the quintile (from 1 to 5). There is a [database available here](https://www.gov.scot/publications/scottish-index-of-multiple-deprivation-2020v2-postcode-look-up/) which indicates the SIMD decile and quintile for each postcode.
- The same data as your main 2023 dataset is also available separately for previous years (from 2015): see [Postcode level data on this page](https://www.gov.uk/government/collections/sub-national-electricity-consumption-data).
- Data is available on [Scottish house prices](https://www.ros.gov.uk/data-and-statistics/property-market-statistics/small-area-statistics) between 2004 and 2024, broken down by different small subdivisions of the country (which you can match to a postcode -- see below).
- If you'd like to produce a map with Geopandas, these geographic "shapefiles" could be useful (although you can also produce great maps without these, e.g. using Folium): [Data Zone Boundaries](https://spatialdata.gov.scot/geonetwork/srv/eng/catalog.search#/metadata/f6656adf-b720-4612-ad5c-1d13eae94c8b), [Data Zone Centroids](https://spatialdata.gov.scot/geonetwork/srv/eng/catalog.search#/metadata/6755b5a3-5d99-4ca3-bd19-33d5454774ac)
- There is an API which you can use to request information about the electricity generation mix -- i.e. which proportion of electricity used in Scotland was generated from different types of fuel (e.g. wind, solar, coal...); see the Week 7 workshop on how to use an API. The [API documentation is here](https://carbon-intensity.github.io/api-definitions/#carbon-intensity-api-v2-0-0), along with some Python code snippets to give examples on how to request data. If you use this, please be careful not to request too much data at a time! You can go all the way down to postcode area, but the historical data is only available in slices of 30 minutes at a time, so be mindful of this, and e.g. don't request data for 6 months for all the Scottish postcodes in a big loop (you will exceed the API rate limits!).

You are also free to download and use other related data (from the links above or from other sources -- just make sure the data is licensed in a way which allows you to use it!) to complement your investigation if you wish. Please discuss this with your tutor if you plan to do so!


---

## Some ideas to get you started

Please note that **this is not a Statistics or data science course**, but a Python programming course. For example, you can produce an excellent report "only" with carefully selecting and aggregating relevant data and producing some (non-trivial) visualisations of different aspects, perhaps with some basic statistics/aggregation. The important thing in your report is that you can use your Python skills to good effect to show interesting things about the data. If you do attempt some statistical analysis, don't worry too much about it being perfectly rigorous -- the important thing is that your choices and assumptions are sensible and that you justify them in your report.

Here are some example questions your report could address; these could be standalone questions if you investigate them in sufficient depth, or smaller questions as part of your main investigation topic and key result. Again, you are also encouraged to come up with your own question(s) too. The important thing is that your report is **coherent and well-presented**, that your **code** works as intended, and that you explore some of the aspects of the data in reasonable depth. Generally speaking, it's a good idea to **limit the scope of your report**; don't try to do too many different things at once, but instead try to focus on one key topic or problem. Doing this well will take plenty of time and effort!

- How does electricity consumption vary across different parts of the country? For example, you could consider consumption per household or per capita, using appropriate census data. You could also focus on electricity consumption across a particular region or city, or perhaps differences between urban and rural areas, or even differences depending on average temperature and daylight hours.
- How does electricity consumption vary depending on what kind of building you live in? For example, you could use the census data to find out which postcodes have mostly single houses or mostly flats, and try to draw comparisons. The census data also contains information about how people heat their houses (e.g. electric or gas central heating), which you could explore.
- How has electricity consumption changed over recent years? You could use the datasets from years before 2023 and aggregate this over the entire country or by region or overall postcode area, or look at smaller areas of interest. For example, you could show overall changes over time since 2013, or focus on comparing 2023 with 2020 (where a lot of people stayed at home because of the Covid pandemic).
- How does consumption vary depending on socio-economic deprivation? For example, you could investigate whether people living in more deprived areas tend to consume more electricity or less electricity than people living in wealthier areas. You could also look at house prices; for example, perhaps more expensive houses are also more expensive to power, or less expensive because they might be better insulated.
- The main dataset gives you total yearly electricity consumption per postcode (and average yearly consumption per household in each different postcode). You can divide this by 365 to get an estimate of average daily consumption. On a given day, using the generation mix dataset, can you say something about how different parts of the country (or different parts of a city, or different regions overall) use different amounts of the different fuels, and perhaps how different areas contribute differently to carbon emissions as a result? The electricity generation mix can change quite a lot each day, and even at different times of the same day (e.g. wind will only produce power when it's windy; solar will only produce power when it's sunny; etc.), so you could even compare a few different days, or look at a particular day where the mix changes significantly.

If you have another idea for a question, but you're not sure whether the data exists to support your investigation, please discuss this with your tutor.

---

## Working on your project

During the Week 8 workshop, you should discuss with your group and come up with a **plan**.

- First of all: **please work and discuss in English** with your group (including writing code comments!). Good communication is key to succeed in group work!
- **Discuss your strengths** and what you bring to the group. Depending on your background, you might feel more confident with performing computations on the data using Python, or with planning and producing professionally-laid-out data visualisations, or with interpreting results and writing up the report, or with planning and coordinating teamwork; discuss this with your group and divide the work so you can each best use your strengths, in a way which feels fair to everyone. All these skills are important parts of making a great project. **Be supportive of each other**!
- **Pair-program** as much as possible! You will likely be much more productive if you have another person to bounce ideas off of about what to investigate or how to present results, and help each other solve problems. You can do this in pairs, you can mix up pairs, you can even do "group programming" sessions with one driver and 2-3 navigators.
- Schedule quick **code reviews** for each other, to help each other stay on track and write better code.
- Use your shared GitHub repo to **collaborate**.
    - Every time you start working on the project, start by **pulling** the latest version from GitHub into your codespace (or your computer).
    - Then, as you work, **commit** your changes regularly. When you are done for the day (or even before that), **push** your work to the GitHub repo to share it with your team.
- To **submit** your project, the process will be the same as for Project 1: first, **push** your final version (ready for submission) **to your GitHub repo**, then submit your repo to Gradescope. Gradescope will be set up so that one person can submit the report on behalf of their group.

---

## Submission format

### What should the report look like?

You will write your report as a Jupyter notebook (use `project-2-report.ipynb`), structured as described earlier. Look at the **C3** criterion in the marking scheme for what constitutes good presentation.

### Where do I write code?

Like in Project 1, write one or more **modules** with different functions to perform all the data reading, cleaning, selection, manipulation, and visualisation. Then, in your report notebook, call your functions in code cells to actually read/clean/select/manipulate the data and display your visualisations.

### How do I manage CSV files?

The file `.gitignore` in your repository contains a list of files and paths that git will automatically ignore in your commits. In particular, the line `*.csv` means that by default, all CSV files will be ignored.

**This is important, don't remove it** -- GitHub has a maximum file size limit, which the main datafile for the project will likely exceed.

Recall from the Week 8 lecture that Pandas can use the URL of a `.csv` file as input, to download the data directly without you having to save the file manually.

Once you have read the data into a dataframe, you can save a local copy into your current folder (in your codespace), for instance as a `.csv` file. The next time you want to use the data, you can just use `pd.read_csv()` with your local file as input.

To minimise the size of the saved files, you can also select only the parts of the data that you know you'll be interested in, using `.loc[]`, before saving the CSV file. Just be careful with the amount of data you are saving -- try not to save too many heavy data files in your codespace.

If someone else in your group needs to access a CSV file you've created like this, they can just run the code again and produce it in their own codespace.

### Can I use Excel to work on the data (e.g. filter, order, or select sections of the data) before I read it using Python?

**No**. Everything you do with the data must be done using Python, and all the code you use for processing the data must be included in your submission. When marking your projects, a marker must be able to reproduce all of your results exactly as they are, by just running the code in your notebook, starting from the original data files.

---

## Libraries

The same libraries as usual are available in your codespaces -- these are:

```
python
numpy
scipy
matplotlib
pandas
seaborn
jupyter
ipywidgets
requests
pip
```

The version of Python is `3.12.11`. Beyond these, for this project, **you can also use other packages or libraries that you find useful**. If there are any other packages you want to use:

- Find out the name of the package in the installation instructions.
- Add the name of the package as a new line to the file `requirements.txt`.
- In the terminal at the bottom of your codespace, run the command `pip install -r requirements.txt`.

This should install any new packages you've added to `requirements.txt` to your codespace permanently. (If you create a new, separate codespace however, you'll need to run the command again.)

Here are some packages you might find useful:

- If you choose to visualise anything on a map, packages like [folium](https://python-visualization.github.io/folium/) or [geopandas](https://geopandas.org/) might be useful.
- If you fancy making interactive visualisations, with things like toggle buttons or sliders, you could look into [IPython widgets](https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Basics.html). (This is how the "Solution" buttons are made in your tutorial notebooks, for example -- note that this is already installed in your codespaces.)
- Beyond matplotlib and seaborn, other popular plotting/visualisation libraries include [bokeh](https://docs.bokeh.org/en/latest/docs/gallery.html) and [plotly](https://plotly.com/python/).
- For those of you with an interest/experience in machine learning who would like to use this in your project, [Scikit-learn](https://scikit-learn.org/stable/) has plenty of useful functions for supervised and unsupervised learning. (Again, this is very much not a requirement of the course!)

For example, if you wanted to use folium and Scikit-learn, you would add the following to `requirements.txt`, then run the terminal command `pip install -r requirements.txt`:

```
folium
scikit-learn
```

---

## Marking scheme

Your project will be marked on 4 criteria:

- Technical proficiency (16 marks)
- Amount of work done and depth of investigation (12 marks)
- Presentation and cohesion of the report (8 marks)
- Code comments, docstrings, code style, and readability (4 marks)

The detailed marking scheme will be available in your repositories under `project-2-markingscheme.md`.

### Peer moderation of group contributions

When submitting your group project, we will also ask each student to complete a short peer moderation form. You will be asked to rate each of your group members' contributions to the project, as well as your own contributions, on 3 different aspects:

- **Engagement and communication**: attendance and contribution to meetings, reliability, communication between meetings, and contributions to positive and supportive group dynamics.
- **Effective collaboration and good will**: overall efforts to contribute to the project as a team member, and to seek and provide feedback to/from other team members. Keep in mind that different students have different strengths; the important thing here is that everyone tries their absolute best.
- **Quality of contribution**: overall technical quality of the contribution of an individual to the project.

The results will inform the marking, together with the information gathered by your tutors over the next few weeks during the workshops (including your attendance at the workshops and your engagement with the group). Each report will first be marked on its own merits, for the whole group; but if significant evidence of unequal contributions to the project is found, then grades may be adjusted for individual group members.

---

## Academic integrity

### Generative AI

As for Project 1, the use of generative AI tools (ELM, ChatGPT, etc.) is **not permitted** at any point for this assignment without explicit acknowledgement, including: to obtain starter code that you then modify; to review, improve, or comment your code; to translate any part of your work to English before submitting. Please read the [University guidance for students on using generative AI](https://information-services.ed.ac.uk/computing/communication-and-collaboration/elm/generative-ai-guidance-for-students/using-generative). In particular, of relevance to this assignment:

> Passing off someone – or something’s – work as your own for an assessment is academic misconduct. This could be failing to cite a source you have used in piece of assessed work, getting someone else to complete an assessment for you, claiming authorship of machine-generated content or presenting machine-translated work as your own.
> 
> If you submit a piece of work for assessment that is not your own original work you risk being investigated according to the university’s academic misconduct investigation procedures. This could have serious implications for you and your studies.
> 
> The following uses of generative AI are **not acceptable** and constitute misconduct: if you use them you risk investigation and penalties.
> 
> - Presenting AI outputs as your own, original work.
> - Use of an AI translator to convert assessments to English before submission: English is the language of teaching and assessment at Edinburgh – machine translation is treated as false authorship and is not acceptable. [This is true for all text you submit, including code comments.]
> - Submitting an assessment which includes elements of AI-generated text without acknowledgment.
> - Submitting an assessment which includes AI-generated mathematical formulae or reasoning, or computer code, without acknowledgment.

### References

As for Project 1, **most** of the code you submit must be **authored by your group**. That being said, you may use any code from the course material (e.g. workshop tasks, notebooks, lectures), without citing it.

You may use **small pieces of code** (3-4 lines maximum at a time) that you found elsewhere -- e.g. examples from the documentation, a textbook, forums, blogs, etc... You may use this code *verbatim* (i.e. almost exactly as you found it), or adapt it to write your own solution.

A programming assignment is just like any other academic assignment -- and therefore, **you must provide a citation for any such code**, whether you use it *verbatim* or adapt it. To do so, include a code comment at the start of your script or notebook cell, indicating:

- the line numbers where the code was used or adapted,
- the URL of the source (or, if it's from a book, a full reference to the book),
- the date you accessed the source,
- the author of the code (if the information is available). **This includes cases where the "author" is a generative AI tool (e.g. ChatGPT).**

You can use this template -- delete one of the URL or book reference lines as appropriate:

```python
# Lines X-Y: Author Name
# URL: http://...
# Book Title, year published, page number.
# Accessed on 30 Feb 2025.
```

You must also provide **detailed code comments** for any such code, **in your own words**, to demonstrate that you fully understand how it works -- you will lose marks if you use external code without explaining it, even if it's cited correctly.

Your mark will also be negatively affected if a substantial part of your submission (more than approx. 20%) has not been authored by your group, even if everything has been cited appropriately. The extent of this will depend on the proportion of your submission which you have authored yourself, and the proportion which comes from other sources.

Remember to exercise caution if you use any code from external sources -- there are a lot of blogs, forums, and genAI tools which will give you very bad code!

With all that, we trust that you'll be able to use your best judgement, and to cite your sources appropriately -- if anything is not clear, please do ask. Note that **all submissions** will be automatically checked (and manually reviewed) for plagiarism and collusion, and [the University's academic misconduct policy](https://www.ed.ac.uk/academic-services/staff/discipline/academic-misconduct) applies.


