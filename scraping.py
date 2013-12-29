import urllib2
from bs4 import BeautifulSoup
import xlsxwriter

def scrap_tutor_id(page_num):
	j=1
	while j <= page_num:
		print "This is Page #" + str(j)
		url = "http://www.tuitionplaza.com/asp/tutor.asp?sestate=K.Lumpur/Selangor&selevel=Form%204%20-%205&MemPagePosition=" + str(j)
		soup = BeautifulSoup(urllib2.urlopen(url).read())


		i=0
		while i < 20:
			row = soup('table', {'bgcolor': '#FBF8D6'})[i].tr.td.font
			tutor_id = row.a["href"][-5:]
			tutor_name = row.a.string.strip()
			with open("tutor", "a") as f:
				text = tutor_id + ":" + tutor_name + "\n"
				f.write(str(text))

			i+=1
		j+=1
	return




def open_tutor_list(file_name):
	f = open(file_name, 'r')
	a = f.read()
	tutor_list = a.split("\n")
	tutor_list.pop()
	return tutor_list



# function to clean up some dirty tutor id data from web scraping
def clean_up():
	tutor_list = open_tutor_list("tutor")
	for t in tutor_list:
		if t[0] == "d":
			t = t[1:]
		if t[0] == "=":
			t = t[1:]
		with open("tutor2", "a") as f:
				text = t + "\n"
				f.write(str(text))	
	return


def output_tutor_id(file_name):
	tutors = open_tutor_list(file_name)
	tutor_id = []
	for t in tutors:
		a = t.split(":")[0]
		tutor_id.append(a)
	return tutor_id


def output_tutor_data(tutor_id, start, end):
	num_tutors = len(tutor_id)
	print "TOTAL TUTOR TO SCRAP = " + str(num_tutors)
	workbook = xlsxwriter.Workbook('demo.xlsx')
	worksheet = workbook.add_worksheet()
	bold = workbook.add_format({'bold': 1})
	worksheet.write('A1', 'Name', bold)
	worksheet.write('B1', 'Tutor ID', bold)
	worksheet.write('C1', 'State', bold)
	worksheet.write('D1', 'Location', bold)
	worksheet.write('E1', 'Tuition Level', bold)
	worksheet.write('F1', 'Tuition Subjects', bold)
	worksheet.write('G1', 'Email Address', bold)
	worksheet.write('H1', 'Telephone Number', bold)
	worksheet.write('I1', 'Posting Date', bold)
	worksheet.write('J1', 'Description', bold)
	

	j=start
	while j < end:
		print "This is Tutor #" + str(j) + " | Tutor ID = " + str(tutor_id[j])

		url = "http://www.tuitionplaza.com/asp/DETAil.asp?TUTORID=" + str(tutor_id[j])
		#soup = BeautifulSoup(urllib2.urlopen(url).read())

		html = urllib2.urlopen(url).read()
		soup = BeautifulSoup(html, "lxml")


		name = soup('td', {'bgcolor': '#003399'})[0].text.strip()
		worksheet.write(j+1, 0, name)

		i=0
		while i < 8:
			row = soup('table', {'bgcolor': '#FBF8D6'})[i].tr.td
			if i == 5:
				if row.font:
					# for cases with email addresses
					row = row.font.text.strip()
				else:
					# if email address is not there then scrap from email link
					row = str(row.table.tr.td.a)
					a = row.index('Email')
					b = row.index('"',63)
					row =  row[a+6:b]
			else:
				row = row.font.text.strip()
			worksheet.write(j+1, i+1, row)
			i+=1

		description = soup('tr', {'bgcolor': '#FBF8D6'})[0].tr.td.font.text
		worksheet.write(j+1, 9, description)
		j+=1	
	return


	

#scrap_tutor_id(99)
#print open_tutor_list("tutorclean")
#print output_tutor_id("tutorclean")
#clean_up()
#print len(output_tutor_id("tutorclean"))
output_tutor_data(output_tutor_id("tutorclean"),1500,1981)

#output_tutor_data([52482, 54480],0,2)