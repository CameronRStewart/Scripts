import os
import string
import logging
import mysql.connector
from mysql.connector import errorcode
import ConfigParser




class Migration:

	def __init__(self):
		configParser = ConfigParser.ConfigParser()
		configParser.readfp(open(r'config.txt'))
		self.dbConfig = dict(configParser.items('database'))
		self.dbConfig['raise_on_warnings'] = configParser.getboolean('database', 'raise_on_warnings')

		#log_path = configParser
		#logging.basicConfig(filename=)

	def runMigration(self):
		cursor = self.getEresDocumentInfo()


	def getEresDocumentInfo(self):
		try:
			con = mysql.connector.connect(**self.dbConfig)
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				print("Database Connection Error: Access denied.  Check Username/Password.")
			elif err.errno == errorcode.ER_BAD_DB_ERROR:
				print("Database Connection Error: Database doesn't exist.")
			else:
				print(err)
			exit(1)

		cursor = con.cursor()

		query = ("""SELECT coursetodoc.docid, documents.title, departments.deptname, departments.abbreviation, courses.number, courses.coursename, courses.term, courses.year, courses.instrlastnames
					FROM coursetodoc
					JOIN courses ON coursetodoc.courseid=courses.courseid
					JOIN departments ON courses.deptID=departments.deptid
					JOIN documents ON coursetodoc.docid=documents.docid""")

		cursor.execute(query)

		if cursor.rowcount:
			self.printTables(cursor)
		else:
			print("Warning: Nothing retrieved in database query.")
			exit(0)


		cursor.close()
		con.close()

		return cursor


	def cleanString(self, dirty_string, mode='f'):

		# -_ abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
		valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

		# .abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789
		# Also, Later I replace any '/' with '-'
		valid_coursenumber_chars = ".-%s%s" % (string.ascii_letters, string.digits)


		if mode == 'f':
			clean_string = ''.join(c for c in dirty_string if c in valid_filename_chars)
		elif mode == 'c':
			dirty_string.replace("/", "-")
			clean_string = ''.join(c for c in dirty_string if c in valid_coursenumber_chars)
		else:
			print("Error: Unknown mode value passed to cleanDirectoyName.")
			exit(1)

		# Give ourself some room to avoid filename character count restrictions
		# In general: filenames cant be longer than 255 chars.  
		# We also need some room for the .pdf, .doc, et. al.
		if len(clean_string) > 250:
			clean_string = clean_string[:250]

		return clean_string




	def printTables(self, cursor):
		# docid          = row[0]
		# title          = row[1]
		# deptname       = row[2]
		# abbreviation   = row[3]
		# number         = row[4]
		# coursename     = row[5]
		# term           = row[6]
		# year           = row[7]
		# instrlastnames = row[8]

		#row = cursor.fetchone()
		#while row is not None:
		#	print "Title: %s Department: %s-%s" % (self.cleanString(row[1], mode='f'), self.cleanString(row[3], mode='f'), self.cleanString(row[4], mode='c'))
		#	row = cursor.fetchone()

		row = cursor.fetchone()
		while row is not None:
			print "Semester: %s%s \nDepartment: %s \nInstructor: %s \nCourse: %s-%s \nDocument: %s \n" % (self.cleanString(row[6], mode='f'),
																							self.cleanString(row[7], mode='f'), 
																							self.cleanString(row[2], mode='f'), 
																							self.cleanString(row[8], mode='f'),
																							self.cleanString(row[3], mode='f'), 
																							self.cleanString(row[4], mode='c'),
																							self.cleanString(row[1], mode='f'))
			row = cursor.fetchone()



