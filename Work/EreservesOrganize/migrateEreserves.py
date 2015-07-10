import os
import shutil
import string
import glob
import logging
import pymysql
import ConfigParser




class Migration:

	def __init__(self):
		configParser = ConfigParser.ConfigParser()
		configParser.readfp(open(r'config.txt'))
		self.dbConfig = dict(configParser.items('database'))

		self.origin_root = configParser.get('path', 'origin_root')
		self.destination_root = configParser.get('path', 'destination_root')
		self.default_permissions = configParser.get('path', 'default_permissions')

		self.config_log_level =  configParser.get('logging', 'log_level')
		self.log_file_path = configParser.get('logging', 'log_path')

		if self.config_log_level == 'DEBUG':
			log_level = logging.DEBUG
		elif self.config_log_level == 'INFO':
			log_level = logging.INFO
		elif self.config_log_level == 'WARNING':
			log_level = logging.WARNING
		elif self.config_log_level == 'ERROR':
			log_level = logging.ERROR
		elif self.config_log_level == 'CRITICAL':
			log_level = logging.CRITICAL
		else:
			# Make up a reasonable default
			log_level = logging.ERROR


		logging.basicConfig(filename=self.log_file_path, level=log_level, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p')

		self.run_mode = configParser.get('mode', 'run_mode')


	def runMigration(self):
		logging.info("Running Migration")
		cursor = self.getEresDocumentInfo()

	def getEresDocumentInfo(self):
		try:
			con = pymysql.connect(**self.dbConfig)
		except pymysql.OperationalError as err:
			logging.error(err)
			print ("There were errors that caused this application to abort.  Please see %s for details" % self.log_file_path)
			exit(1)

		cursor = con.cursor()

		# TODO: This query has a massive added overhead by running the ORDERBY statement, but it's useful for debugging.
		query = ("""SELECT coursetodoc.docid, documents.title, departments.deptname, departments.abbreviation, courses.number, courses.coursename, courses.term, courses.year, courses.instrlastnames
					FROM coursetodoc
					JOIN courses ON coursetodoc.courseid=courses.courseid
					JOIN departments ON courses.deptID=departments.deptid
					JOIN documents ON coursetodoc.docid=documents.docid
					ORDER BY coursetodoc.docid""")

		cursor.execute(query)

		if cursor.rowcount:
			self.reorganize(cursor)


		else:
			print ("There were errors that caused this application the exit.  Please see %s" % self.log_file_path)
			logging.error("Nothing retrieved in database query.")
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

		# 0123456789
		valid_numeric_chars = string.digits

		dirty_string = str(dirty_string)

		#dirty_string = unicode(str(dirty_string), 'utf-8')
		if mode == 'f':
			clean_string = ''.join(c for c in dirty_string if c in valid_filename_chars)
		elif mode == 'c':
			dirty_string.replace("/", "-")
			dirty_string.replace(",", "-")
			clean_string = ''.join(c for c in dirty_string if c in valid_coursenumber_chars)
		elif mode == 'n':
			clean_string = ''.join(c for c in dirty_string if c in valid_numeric_chars)
		elif mode == 't':
			clean_string = dirty_string
		else:
			print ("There were errors that caused this application the exit.  Please see %s" % self.log_file_path)
			logging.error("Unknown mode value passed to cleanDirectoyName.")
			exit(1)

		# Give ourself some room to avoid filename character count restrictions
		# In general: filenames cant be longer than 255 chars.  
		# We also need some room for the .pdf, .doc, et. al.
		# Titles, more accurately descriptions, are excluded.
		if not mode == 't':
			if len(clean_string) > 250:
				logging.warning("Filename: %s was truncated to 250 chars." % clean_string)
				clean_string = clean_string[:250]

		return clean_string



	def reorganize(self, cursor):
		row = cursor.fetchone()
		while row is not None:

			docid          = self.cleanString(row[0], mode='n')
			title          = self.cleanString(row[1], mode='t')
			deptname       = self.cleanString(row[2], mode='f')
			abbreviation   = self.cleanString(row[3], mode='f')
			number         = self.cleanString(row[4], mode='c')
			coursename     = self.cleanString(row[5], mode='c')
			term           = self.cleanString(row[6], mode='f')
			year           = self.cleanString(row[7], mode='n')
			instrlastnames = self.cleanString(row[8], mode='c')

			if os.path.isdir(self.origin_root+"/"+docid):

				path = self.destination_root

				# This is just a variable to keep track of the tail of the path we are building:
				# i.e. the destination_path minus the destination_path root.
				path_tail = ""
				for d in [term+year, deptname, instrlastnames, abbreviation+"-"+number]:
					path_tail = path_tail+"/"+d
					path = path+"/"+d
					if not os.path.isdir(path):
						if self.run_mode == 'RUN':
							os.mkdir(path, int(self.default_permissions))
						logging.debug("Created Directory: %s" % path)
				logging.info("Created Directory tree: %s" % path)


				origin_path = self.origin_root+"/"+docid
				destination_path = self.destination_root+path_tail

				# Open or create 'info' file that relates filename to title (if title exists)
				info_file_path = destination_path + "/" + "info.txt"

				if self.run_mode == 'RUN':
					info_file = open(info_file_path, 'a+')

				# Have to assume that there is only one file in origin.
				for f in glob.glob(origin_path+"/*"):
					try:
						filename, file_extension = os.path.splitext(f)
						logging.info("Copying file: %s to %s" % (f, destination_path))
						filename_no_path = f.rsplit('/', 1)[1]
						logging.info("Info File info: Filename: %s\nTitle(Description): %s\n\n" % (filename_no_path, title))
						if self.run_mode == 'RUN':
							shutil.copy(f, destination_path)
							if not title == None and not title == '':
								info_file.write("Filename: %s\nTitle(Description): %s\n\n" % (filename_no_path, title))
					except shutil.Error as err:
						logging.warning(err)

				if self.run_mode == 'RUN':
					info_file.close()

			row = cursor.fetchone()
		
                        
			



