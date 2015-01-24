# Converts the search output from Notepad++ to a list of integration
# hooks. (Search for 'call_integration_hook(' in all files and then
# copy the find results)
#
# In the future we will implement some back tracking functionality so
# that we can automatically add a lot more information about an
# integration hook. For example, which function it's called in and
# contextual information about the variables supplied to it/expected
# from it. (Though PHP dynamic typing will make it hard to work it
# out...)

import json
import re

file = {}
hooks = []
unparsed = []

currentFile = '';

with open('rawHooks.txt') as openfileobject:
	for line in openfileobject:
		# Is it a file line?
		dirRe = re.compile(r"[\s]+(?P<directory>[\w]\:\\(?:(?:[^\\^\(]+)\\)*(?P<file>[\w\-\.]+\.php))")
		hookRe = re.compile(r"[\s]+Line (?P<line>[0-9]+)\:[\s]+call_integration_hook\(\'(?P<hook>[\w]+)\'(?P<param>|, .+)\);")
		md = dirRe.match(line);
		mh = hookRe.match(line);
		if mh:
			param = mh.group('param')
			if param[0:2] == ', ':
				param = param[2:]
			file[currentFile] = (mh.group('hook'), mh.group('line'), param)
			hooks.append({
				'hook': mh.group('hook'),
				'line': mh.group('line'),
				'param': param,
				'file': currentFile
			});
		elif md:
			currentFile = md.group('file')
			file[currentFile] = []
		else:
			# Get the line
			linRe = re.compile(r"[\s]*Line (?P<line>[0-9]+)\:.*")
			ml = linRe.match(line)
			if ml:
				unparsed.append({
					'line': ml.group('line'),
					'code': line,
					'file': currentFile
				})
			else:
				# Should probably throw an exception here...
				pass

# Dump it to JSON
jsonOut = json.dumps({'hooks': hooks, 'unparsed': unparsed},indent=4,
	separators=(',', ': '))

out = open("hooks.json", "w")
out.write(jsonOut)
out.close()
