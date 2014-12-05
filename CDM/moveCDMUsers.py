import argparse
import shutil
from subprocess import call
import grp

parser = argparse.ArgumentParser(description='This script transfers user accounts from one ContentDM Linux installation to another, given an /etc/shadow file, an /etc/group file, a CDM users.txt file, and a CDM .htpassword file all from the current production server.')
parser.add_argument('-s', '--shadow', dest="shadow_file_path", help="Full path to a COPY of original /etc/shadow file for input", metavar='FILE', required = True)
parser.add_argument('-u', '--users', dest="users_file_path", help="Full path to a COPY of original {cdmServerRoot}/conf/users.txt file for input", metavar='FILE', required = True)
parser.add_argument('-p', '--password', dest="password_file_path", help="Full path to a COPY of original {cdmServerRoot}/conf/.htpassword file for input", metavar='FILE', required = True)
parser.add_argument('--modify_system', action="store_true", help="Warning: Using this option will add user to system and modify you /etc/shadow file.")

args = parser.parse_args()

shadow_file_path = args.shadow_file_path
users_file_path = args.users_file_path
password_file_path = args.password_file_path
add_system_user = False

if args.modify_system:
	add_system_user = True



try:
	orig_shadow_file = open(shadow_file_path, 'r')
except IOError:
	print "The Path to the given Shadow file does not exist, exiting"

try:
	orig_users_file = open(users_file_path, 'r')
except IOError:
	print "The Path to the given Users.txt file does not exist, exiting"

try:
	orig_password_file = open(password_file_path, 'r')
except IOError:
	print "The Path to the given password file does not exist, exiting"

try:
	local_shadow_file = open('/etc/shadow', 'r')
	#local_shadow_lines = local_shadow_file.readlines()
	local_shadow_file.close()
except:
	print "Cannot open local /etc/shadow, make sure you are running as root"

try:
	new_shadow_file = open('new_shadow', 'a')
except:
	print "Cannot create file for shadow copy in "+call('pwd')


try:
        grp.getgrnam('content')
except KeyError:
        call(['groupadd', 'content'])

users = {}

# From CDM Users.txt file, grab each user and their permissions and add to users dict.
for user_line in orig_users_file:
	user_threeple = user_line.partition('\t')
	name = user_threeple[0]
	perms = user_threeple[2]
	users[name] = {}

	users[name]['permissions'] = perms.strip('\n')
	users[name]['cdm_pass'] = ''
	users[name]['shadow_pass'] = ''


# From CDM .htpassword file, grab each username / pass combo and place CDM pass hash
# into the users dict under the matching user name.
for cdm_pass_line in orig_password_file:
	cdm_pass_threeple = cdm_pass_line.partition(':')
	name = cdm_pass_threeple[0]
	password = cdm_pass_threeple[2]
	if not name in users:
		users[name] = {}
		users[name]['permissions'] = ''	
		users[name]['shadow_pass'] = ''
	users[name]['cdm_pass'] = password.strip('\n')

# From a copy of the production system's /etc/shadow file, grab the password hash
# and place it into users dict under the matching user name.
for shadow_pass_line in orig_shadow_file:
	# The following three lines should split the user name from the pass hash, from the
	# rest of the muck.
	shadow_pass_threeple = shadow_pass_line.partition(':')
	name = shadow_pass_threeple[0]
	password = shadow_pass_threeple[2].partition(':')[0]
	if not name in users:
		continue
	users[name]['shadow_pass'] = password.strip('\n')

orig_users_file.close()
orig_shadow_file.close()
orig_password_file.close()

if add_system_user:
	# If flag is set to add system account, make users and add to content group
	# If the user's shadow pass is blank, dont make them!
	for uname in users:
		if (users[uname]['shadow_pass']) and (not users[uname]['shadow_pass'] == ''):
                        
			call(["useradd",  uname])
                        call(["usermod", "-a", "-G", "content", uname])

        
        # I need to find a way to test opening the file early on, but refresh it's contents here.
        # Otherwise, the shadow file wont have all the users I create above
        #local_shadow_file.seek(0)
        #local_shadow_lines = local_shadow_file.readlines()
        #local_shadow_file.close()

        try:
                local_shadow_file = open('/etc/shadow', 'r')
                local_shadow_lines = local_shadow_file.readlines()
                local_shadow_file.close()
        except:
                print "Cannot open local /etc/shadow, make sure you are running as root"

	# Copy local /etc/shadow and create a new one with all passwords (':!!:') replaced
	# with users[name]['shadow_pass']
	# If the user's shadow pass is blank, dont do this!
	for shadow_line in local_shadow_lines:
		shadow_pass_threeple = shadow_line.partition(':')
		uname = shadow_pass_threeple[0]
                if uname in users:
                        print ('Name: '+uname+'\nCDM Pass: '+users[uname]['cdm_pass']+'\nshadow_pass: '+users[uname]['shadow_pass']+'\nPermissions: '+users[uname]['permissions']+'\n\n')
                        if (users[uname]['shadow_pass']) and (not users[uname]['shadow_pass'] == ''):
                                new_pass = users[uname]['shadow_pass']
                                new_line = shadow_line.replace(':!!:', ':'+new_pass+':', 1)
                                new_shadow_file.write(new_line)

# Create new users.txt file by looping and doing the following:
# for user in users:
# 	user+'\t'+user['permissions']
# if permissions = '' or cdm_pass = '', dont give account?

# Create new .htpasswd file by looping and doing the following:
# for user in users:
#	user+':'+user['cdm_pass']
# if permissions = '' or cdm_pass = '', dont do this?

orig_users_file.close()
orig_shadow_file.close()
orig_password_file.close()
new_shadow_file.close()
#for uname in users:
#	print ('Name: '+uname+'\nCDM Pass: '+users[uname]['cdm_pass']+'\nshadow_pass: '+users[uname]['shadow_pass']+'\nPermissions: '+users[uname]['permissions']+'\n\n\n\n')



