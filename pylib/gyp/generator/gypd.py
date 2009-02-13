#!/usr/bin/python

"""gypd output module

This module produces gyp input as its output.  Output files are given the
.gypd extension to avoid overwriting the .gyp files that they are generated
from.  Internal references to .gyp files (such as those found in
"dependencies" sections) are not adjusted to point to .gypd files instead.

This generator module is intended to be a sample and a debugging aid, hence
the "d" for "debug" in .gypd.  It is useful to inspect the results of the
various merges, expansions, and conditional evaluations performed by gyp
and to see a representation of what would be fed to a generator module.

It's not advisable to rename .gypd files produced by this module to .gyp,
because they will have all merges, expansions, and evaluations already
performed and the relevant constructs not present in the output.  Output
will also be stripped of comments.  This is not intended to be a
general-purpose gyp pretty-printer; for that, you probably just want to
run "pprint.pprint(eval(open('source.gyp').read()))", which will still strip
comments but won't do all of the other things done to this module's output.

The specific formatting of the output generated by this module is subject
to change.
"""


import gyp.common
import errno
import os
import pprint


# These variables should just be spit back out as variable references.
_generator_identity_variables = [
  'EXECUTABLE_PREFIX',
  'EXECUTABLE_SUFFIX',
  'INTERMEDIATE_DIR',
  'PRODUCT_DIR',
]

# gypd doesn't define a default value for OS like many other generator
# modules.  Specify "-D OS=whatever" on the command line to provide a value.
generator_default_variables = {
}

for v in _generator_identity_variables:
  generator_default_variables[v] = '<(%s)' % v


def GenerateOutput(target_list, target_dicts, data):
  output_files = {}
  for qualified_target in target_list:
    [input_file, target] = \
        gyp.common.BuildFileAndTarget('', qualified_target)[0:2]

    if input_file[-4:] != '.gyp':
      continue
    input_file_stem = input_file[:-4]
    output_file = input_file_stem + '.gypd'

    if not output_file in output_files:
      output_files[output_file] = input_file

  for output_file, input_file in output_files.iteritems():
    output = open(output_file, 'w')
    pprint.pprint(data[input_file], output)
    output.close()
