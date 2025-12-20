# -SDA-_Group4

This is the Github page for the Scientific Data Analysis group project.

1. Project Description:
   This study discusses a possible correlation between mental health issues and the usage of social media. The study attempts to find a correlation between different
   age groups and their mental health state with the platforms they use. The duration of social media usage for each age group will also be studied. Finally, the study
   compares the population growth against the growth of the total number of social media users within different countries, discussing a possible correlation between a
   fast uptake in the number of social media users and a fast decline in mental health within countries. Because this study uses country- and age-group-level data,
   all conclusions are also limited to these groups. Therefore, to prevent the ecological fallacy, this study does not draw conclusions about individuals.

3. Github structure:
    - **Data**: The raw data (like .csv files) we use for our experiments, and code used for the webscraping of data.
    - **Experiments**: The code used for processing and plotting the data.
         - Sub1_Sub2: Code related to subquestion 1 and 2.
            - collect_data.py: Collects and cleans the data from the dataset.
            - plot_data.py: Plots the results from the dataset.
            - process_data.py: Perform experiments on the data.
            - test_data.py: Compare result to statistical test to show accuracy.
         - Sub3: Code related to subquestion 3.
            - country.py: Code for the experiments on the relation of countries.
            - continent.py: Code for the experiments on the relation of continents.
         - Sub4: Code related to subquestion 4.
            - collect_data.py: Collects and cleans the data.
            - plot_data.py: Plots the results from dataset.
            - mann_whitney_u_test.py: Implement the Mann-Whitney-U test to perform on the data.
    - **Plots**: The visual results from our experiments, sorted in folders per sub question.
    - **Presentation**: All the stuff necessary for the final presentation (Like the presentation slides and
      copies of the conclusions and limitations, which can also be found in the planning document).
   

4. How to run the code:
   - From the base folder ('\-SDA-_Group4') run the command 'python3 ./Experiment/{subquestion}/{filename}.py',
     or from the sub-question folder 'python3 ./{filename}.py', to run a specific file. The used tests will run
     automatically afterwards and show the results/plots.
   - In the case of multiple tests (like process_data.py in Sub1_Sub2), Tests
     can be uncommented with # to disable/enable them, to run specific tests.

5. Credits:
   - Ryan: Subquestions 1 and 2, presentation planning, Github maintenance.
   - Hero: Subquestion 4, \webscraping code and presentation planning.
   - Mingtao: Subquestion 3 (continent) and \IHME_data
   - Maryelis: Subquestion 3 (country.py)
     -> (NOTE: One member left the course during this project, which explains why their section was smaller).

6. How to use Github (for group members):
   - In the Github repo you can view all the files and folders uploaded to this repo.
   - You can click on the files and folders to view the documents.
   - By clicking on the EDIT button, you can make changes to the file. Once you are done
     finish by clicking 'commit changes' and enter a short message explaining your changes.
   - On the main repo page, you can click on the 'add file' button to make new files, or upload
     from you pc directly to the repo. Afterwards, you just need to leave a commit message.
   - If possible, try to group similar files into folders, to keep the github clean, such as a data folder,
     or result folder. 
  
7. Tech support:
   - If there are any issues with editing/uploading files, try to contact **Ryan** on telegram.
