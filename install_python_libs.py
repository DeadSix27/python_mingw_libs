#!/usr/bin/env python2

# #################################################################################################################
# Copyright (C) 2017 DeadSix27 (https://github.com/DeadSix27/python_mingw_libs)
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# #################################################################################################################

import sys,os,urllib

_DEBUG = False

SUPPORTED_VERSIONS = ['3.6.4','3.6.5','3.6.6','3.6.7','3.7.1']
RC_VERS = { '3.6.7' : '3.6.7rc2' }

VERSION_SPECIFICS = { #stupid idea, but works. Too lazy to make it proper with version parser.
	'3.7.1' : {
		'short' : '37',
		'short_dot' : '3.7',
	},
}

PACKAGE_STUFF = {
		'dllzname' : 'python%%SHORT%%',
		'pc_names' : (
			'python-%%SHORT_DOT%%.pc',
			'python3.pc',
			'python-%%SHORT_DOT%%m.pc',
		),
		'libname' : 'libpython%%SHORT%%.a',
		'pcfile' : 
			'prefix=%%PREFIX%%'
			'\nexec_prefix=${prefix}'
			'\nlibdir=${exec_prefix}/lib'
			'\nincludedir=${prefix}/include'
			'\n'
			'\nName: Python'
			'\nDescription: Python library'
			'\nRequires:'
			'\nVersion: %%VERSION%%'
			'\nLibs.private:'
			'\nLibs: -L${libdir} -lpython%%SHORT%%'
			'\nCflags: -I${includedir}/python3',
}

def run_cmd(cmd):
	if _DEBUG:
		print("\n--Running command in '%s': '%s'\n--" % (os.getcwd(),cmd))
	os.system(cmd)

def is_tool(name):
	from distutils.spawn import find_executable
	return find_executable(name) is not None

def exitHelp():
	print("install_python_libs.py install/uninstall <arch> <version> <install_prefix> - e.g install_python_libs.py amd64 3.7.1 /test/cross_compilers/....../")
	exit(1)
def exitVersions():
	print("Only these versions are supported: " + " ".join(SUPPORTED_VERSIONS))
	exit(1)
	
def simplePatch(infile,replacetext,withtext):
	lines = []
	print("Patching " + infile )
	with open(infile) as f:
		for line in f:
			line = line.replace(replacetext, withtext)
			lines.append(line)
	with open(infile, 'w') as f2:
		for line in lines:
			f2.write(line)

if not is_tool("rsync"):
	print("Please make sure that rsync is installed.")
	exit(1)
			
if len(sys.argv) != 7:
	exitHelp()
else:
	if sys.argv[1] == "install":
		arch    = sys.argv[2]
		ver     = sys.argv[3]
		rc_ver  = ver
		if ver in RC_VERS:
			rc_ver = RC_VERS[ver]
		prefix  = sys.argv[4]
		dlltool = sys.argv[5]
		gendef  = sys.argv[6]
		
		ver_short     = "36"
		ver_short_dot = "3.6"
		
		if ver in VERSION_SPECIFICS:
			ver_short     = VERSION_SPECIFICS[ver]["short"]
			ver_short_dot = VERSION_SPECIFICS[ver]["short_dot"]
		
		if ver not in SUPPORTED_VERSIONS:
			exitVersions()
			
		run_cmd("mkdir work")
		run_cmd("mkdir bin")
		os.chdir("work")
		run_cmd("mkdir lib")
		os.chdir("lib")
		
		url,filename = 'https://www.python.org/ftp/python/{0}/python-{2}-embed-{1}.zip'.format(ver,arch,rc_ver), 'python-{0}-embed-{1}.zip'.format(rc_ver,arch)
		print("Downloading: " + url)
		urllib.urlretrieve(url,filename)
		print("Done")
		
		dllname = PACKAGE_STUFF["dllzname"].replace("%%SHORT%%",ver_short)
		
		print("Extracting dll")
		run_cmd('unzip -po {0} {1}.dll >{1}.dll'.format(filename,dllname))
		run_cmd('unzip -po {0} _ctypes.pyd >_ctypes.pyd'.format(filename))
		run_cmd('unzip -po {0} {1}.zip >{1}.zip'.format(filename,dllname))
		print("Local installing dll")
		run_cmd('cp {0}.zip ../../bin'.format(dllname))
		run_cmd('cp {0}.dll ../../bin'.format(dllname))
		run_cmd('cp _ctypes.pyd ../../bin'.format(dllname))
		print("Done")
		print("Deleting archive")
		os.unlink(filename)
		
		print("Creating library")
		run_cmd("{0} {1}.dll".format(gendef,dllname))
		
		defname = dllname + ".def"
		run_cmd("{0} -d {1} -y {2}".format(dlltool,defname,PACKAGE_STUFF["libname"].replace("%%SHORT%%",ver_short)))
		
		print("Done")
		
		os.unlink(defname)
		os.unlink(dllname+".dll")		
		
		run_cmd("mkdir pkgconfig")
		
		os.chdir("pkgconfig")
		
		print("Creating pkgconfig")
		
		pc = PACKAGE_STUFF["pcfile"].replace('%%PREFIX%%',prefix).replace('%%VERSION%%',ver).replace("%%SHORT%%",ver_short)
		
		for fn in PACKAGE_STUFF["pc_names"].replace("%%SHORT_DOT%%",ver_short_dot):
			with open(fn,"w") as f:
				f.write(pc)
		
		os.chdir("..")
		
		os.chdir("..")
		url,filename = 'https://www.python.org/ftp/python/{0}/Python-{1}.tgz'.format(ver,rc_ver), 'Python-{0}.tgz'.format(rc_ver)
				
		print("Downloading: " + url)
		urllib.urlretrieve(url,filename)
		print("Done")
		print("Extracting headers")
		run_cmd("mkdir include")
		run_cmd("tar -xvf {0} Python-{1}/Include".format(filename,rc_ver))
		run_cmd("mv Python-{0}/Include include/python3".format(rc_ver))
		
		
		run_cmd("tar -xvf {0} Python-{1}/PC/pyconfig.h".format(filename,rc_ver))
		
		simplePatch("Python-{0}/PC/pyconfig.h".format(rc_ver),"#define hypot _hypot","#if (__GNUC__<6)\n#define hypot _hypot\n#endif")
		
		run_cmd("mv Python-{0}/PC/pyconfig.h include/python3/".format(rc_ver))
		
		
		
		print("Done")
		os.unlink(filename)
		run_cmd("rm -r Python-{0}".format(rc_ver))
		
		os.chdir("..")
		print("Installing to " + prefix)
		
		if not os.path.isdir(prefix):
			print("ERROR: '" + prefix + "' does not exist")
			run_cmd("rm -r work")
			exit(1)
		
		run_cmd("rsync -aKv work/ {0}".format(prefix))
		
		run_cmd("rm -r work")
		
		
	elif sys.argv[1] == "uninstall":
		pass
	else:
		exitHelp()
