#[Handouts Archive](http://sudhirmishra.github.io/course-handouts)#


Installing pre-requisites and setting up the enviornment
```
# Install pip
sudo apt-get install python-pip

# Clone the repository
git clone http://github.com/sudhirmishra/course-handouts.git

# Install the required libraries
pip install requests bs4

# Run the download script
python download_handouts.py

# Rename the download directory
mv "Rename Handouts" <semester>_SEM_<year>
# semester = I or II and year = 2015-16,2016-17, ....

# Push the update to archive
git add <semester>_SEM_<year>
git commit -m "Handout for <semester>_SEM_<year> added"
```

