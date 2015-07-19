from hachoir_metadata import metadata
#from hachoir_core.cmd_line import unicodeFilename
from hachoir_parser import createParser

# using this example http://archive.org/details/WorkToFishtestwmv
filename = 'media/gpsvideo.MOV' 
#filename, realname = unicodeFilename(filename), filename
parser = createParser(filename)

# See what keys you can extract
for k,v in metadata.extractMetadata(parser)._Metadata__data.iteritems():
    if v.values:
        print v.key, v.values[0].value

# Turn the tags into a defaultdict
metalist = metadata.extractMetadata(parser).exportPlaintext()
meta = defaultdict(defaultdict)
for item in metalist:
    if item.endswith(':'):
        k = item[:-1]
    else:
        tag, value = item.split(': ')
        tag = tag[2:]
        meta[k][tag] = value

print meta['Video stream #1']['Image width'] 