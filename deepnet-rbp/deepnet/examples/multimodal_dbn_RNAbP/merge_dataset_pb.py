from deepnet import util
from deepnet import deepnet_pb2
import sys, os
from google.protobuf import text_format

proto1 = sys.argv[1]
proto2 = sys.argv[2]
proto3 = sys.argv[3]
output_pbtxt = sys.argv[4]
prefix = sys.argv[5]

out_dir = '/'.join(output_pbtxt.split('/')[:-1])
if out_dir and not os.path.isdir(out_dir):
  os.makedirs(out_dir)
dataset1 = util.ReadData(proto1)
name1 = dataset1.name
dataset2 = util.ReadData(proto2)
name2 = dataset2.name
dataset3 = util.ReadData(proto3)
name3 = dataset3.name

dataset1_prefix = dataset1.prefix
dataset2_prefix = dataset2.prefix
dataset3_prefix = dataset3.prefix
#prefix = os.path.commonprefix([dataset1_prefix, dataset2_prefix,dataset3_prefix,prefix])
prefix = os.path.commonprefix([dataset1_prefix, dataset2_prefix,dataset3_prefix,prefix+'/dbn_reps/'])

if dataset1_prefix != dataset2_prefix:
  for dataset in [dataset1, dataset2, dataset3]:
    _prefix = dataset.prefix[len(prefix)+1:]
    for d in dataset.data:
      if d.file_pattern:
        d.file_pattern = os.path.join(_prefix, d.file_pattern)
      #if d.stats_file:
      #  d.file_pattern = os.path.join(_prefix, d.stats_file)

dataset1.MergeFrom(dataset2)
dataset1.MergeFrom(dataset3)
dataset1.name = '%s_%s_%s' % (name1, name2, name3)
dataset1.prefix = prefix

with open(output_pbtxt, 'w') as f:
  text_format.PrintMessage(dataset1, f)
