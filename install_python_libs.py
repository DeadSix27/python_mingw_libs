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
SUPPORTED_VERSIONS = ('3.6.3',)

VERSION_SPECIFICS = {
	'3.6.3' : {
		'dllname' : 'python36.dll',
		'pc_names' : (
			'python-3.6.pc',
			'python3.pc',
			'python-3.6m.pc',
			'python-3.5.pc', # yes we fake being 3.5, what could possibly go wrong! (mpv/vapoursynth seems to want 35 but also works with 36... ???)
		),
		'libname' : 'libpython36.a',
		'pcfile' : 
			'prefix=%%PREFIX%%'
			'\nexec_prefix=${prefix}'
			'\nlibdir=${exec_prefix}/lib'
			'\nincludedir=${prefix}/include'
			'\n'
			'\nName: Python'
			'\nDescription: Python library'
			'\nRequires:'
			'\nVersion: 3.6.3'
			'\nLibs.private: -lpthread -ldl -lutil'
			'\nLibs: -L${libdir} -lpython36'
			'\nCflags: -I${includedir}/python3',
	},
}

def exitHelp():
	print("install_python_libs.py install/uninstall <arch> <version> <install_prefix> - e.g install_python_libs.py amd64 3.6.1 /test/cross_compilers/....../")
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


if len(sys.argv) != 7:
	exitHelp()
else:
	if sys.argv[1] == "install":
		arch    = sys.argv[2]
		ver     = sys.argv[3]
		prefix  = sys.argv[4]
		dlltool = sys.argv[5]
		gendef  = sys.argv[6]
		
		if ver not in SUPPORTED_VERSIONS:
			exitVersions()
			
		os.system("mkdir work")
		os.system("mkdir bin")
		os.chdir("work")
		os.system("mkdir lib")
		os.chdir("lib")
		
		url,filename = 'https://www.python.org/ftp/python/{0}/python-{0}-embed-{1}.zip'.format(ver,arch), 'python-{0}-embed-{1}.zip'.format(ver,arch)
		print("Downloading: " + url)
		urllib.urlretrieve(url,filename)
		print("Done")
		
		dllname = VERSION_SPECIFICS[ver]["dllname"]
		
		print("Extracting dll")
		os.system('unzip -po {0} {1} >{1}'.format(filename,dllname))
		print("Local installing dll")
		os.system('cp {0} ../../bin'.format(dllname))
		print("Done")
		print("Deleting archive")
		os.unlink(filename)
		
		print("Creating library")
		os.system("{0} {1}".format(gendef,dllname))
		
		defname = "".join(dllname.split(".")[:1]) + ".def"
		os.system("{0} -d {1} -l {2}".format(dlltool,defname,VERSION_SPECIFICS[ver]["libname"]))
		
		print("Done")
		
		os.unlink(defname)
		os.unlink(dllname)
		
		
		
		os.system("mkdir pkgconfig")
		
		os.chdir("pkgconfig")
		
		print("Creating pkgconfig")
		
		pc = VERSION_SPECIFICS[ver]["pcfile"].replace('%%PREFIX%%',prefix)
		
		for fn in VERSION_SPECIFICS[ver]["pc_names"]:
			with open(fn,"w") as f:
				f.write(pc)
		
		os.chdir("..")
		
		os.chdir("..")
				
		url,filename = 'https://www.python.org/ftp/python/{0}/Python-{0}.tgz'.format(ver), 'Python-{0}.tgz'.format(ver)
		print("Downloading: " + url)
		urllib.urlretrieve(url,filename)
		print("Done")
		print("Extracting headers")
		os.system("mkdir include")
		os.system("tar -xvf {0} Python-{1}/Include".format(filename,ver))
		os.system("mv Python-{0}/Include include/python3".format(ver))
		
		
		os.system("tar -xvf {0} Python-{1}/PC/pyconfig.h".format(filename,ver))
		
		simplePatch("Python-{0}/PC/pyconfig.h".format(ver),"#define hypot _hypot","#if (__GNUC__<6)\n#define hypot _hypot\n#endif")
		
		os.system("mv Python-{0}/PC/pyconfig.h include/python3/".format(ver))
		
		
		
		print("Done")
		os.unlink(filename)
		os.system("rm -r Python-{0}".format(ver))
		
		os.chdir("..")
		print("Installing to " + prefix)
		
		if not os.path.isdir(prefix):
			print("ERROR: '" + prefix + "' does not exist")
			os.system("rm -r work")
			exit(1)
		
		os.system("rsync -aKv work/ {0}".format(prefix))
		
		os.system("rm -r work")
		
		
	elif sys.argv[1] == "uninstall":
		pass
	else:
		exitHelp()
