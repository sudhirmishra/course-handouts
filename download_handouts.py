import requests
import urllib
import os
import sys
from bs4 import BeautifulSoup

"""
Course Handout download script

Fetches the course handouts from the intranet site,
relies on the HTML content of the site which is subject to change.

Downloaded handouts are named as per the following convention

SubjectName_CourseCode_CompCode.pdf

The directory structure to be maintained for the archive is

course-handouts/I_SEM_2015-16/
course-handouts/II_SEM_2015-16/
course-handouts/I_SEM_2016-17/
course-handouts/II_SEM_2016-17/
course-handouts/I_SEM_2017-18/
course-handouts/II_SEM_2017-18/


"""

# IP address for the intranet website hosting the
# May change in future
hostname = "http://172.18.6.180"
home_page_url = hostname + "/ID/Handouts.do"

# Get the page containing the table of handout files
html_home = requests.get(home_page_url,"html.parser")

# Create a HTML parser using library beautiful-soup
soup = BeautifulSoup(html_home.text)

"""
Repair utility to add subject names to the filename

"""
def repair(mypath):	
	
	url = "http://172.18.6.180/ID/Handouts.do"

	response = requests.get(url)
	soup = BeautifulSoup(response.text,"html.parser")

	table = soup.find('div',{'class':'tableGrid'})

	rows = table.find('table').findAll('tr')

	# Stores values of the form {course_code_comp_code : subject_name}
	mapping_table = {}

	for row in rows:
		cols = row.findAll('td')
		if len(cols) == 4:
			key = cols[1].text.replace(" ","_") +"_"+cols[0].text
			value = cols[2].text
			mapping_table[key] = value


	# Iterate over each file and add subject name; source : http://stackoverflow.com/questions/3207219/how-to-list-all-files-of-a-directory-in-python
	for f in listdir(mypath):
		# Extract course_code_comp_code
		course_code = f.replace(".pdf","")

		# Check if the f is a file or directory
		if isfile(join(mypath,f)) and course_code in mapping_table:
			
			subject_name = mapping_table[course_code]

			fileName = "{0}_{1}"
			# Rename the file; source : http://www.tutorialspoint.com/python/os_rename.htm
			rename(join(mypath,f),join(mypath,fileName.format(subject_name,course_code)))
			
		


def main():
	# Name of the download directory
	directory = "Rename Handouts/"

	# Create a download directory to which the handouts are downloaded
	try:
		if not os.path.exists(directory):
			os.makedirs(directory)
	except:
		print("Couldn't create the directory ")
		sys.exit(1)

	# The selector for the table
	table = soup.find('div',{'class':'tableGrid'})

	# Get all table rows ( tr tag ) from the HTML as a python list
	rows = table.find('table').findAll('tr')

	"""
	Iterate over each row which contains,
	Comp Code, Course Code, Course Name, Download link to handout
	"""
	for row in rows:
		# Extract all columns in each row
		cols = row.findAll('td')
		# The row that contains 4 columns or cells is a valid row 
		if len(cols) == 4:
			# Course Code and Comp Code
			key = cols[1].text.replace(" ","_") +"_"+cols[0].text
			# Subject Name
			value = cols[2].text
			# Handout download link
			href = row.find('a')
			
			print("Downloaded ",key,value)

			# Source : http://stackoverflow.com/a/7244263
			try:
				# Usage urlretrieve(soure,filename=local_file_name)
				urllib.request.urlretrieve( hostname+href['href'],
						filename=directory+value+"_"+href['href'].split('/')[-1] )
			except:
				print("Couldn't download " + href)


if __name__ == '__main__':
	main()