# ====------ test_feature.py---------- *- Python -* ----===##
#
# Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
# See https://llvm.org/LICENSE.txt for license information.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
#
#
# ===----------------------------------------------------------------------===#
import os
import re
import sys
from pathlib import Path

parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent)

from test_utils import *

exec_tests = ['thrust-vector-2', 'thrust-binary-search', 'thrust-count', 'thrust-copy',
             'thrust-qmc', 'thrust-transform-if', 'thrust-policy', 'thrust-list', 'module-kernel',
             'kernel-launch', 'thrust-gather', 'thrust-scatter', 'thrust-unique_by_key_copy', 'thrust-for-hypre',
             'thrust-rawptr-noneusm', 'driverStreamAndEvent', 'grid_sync', 'deviceProp', 'gridThreads', 'cub_block_p2',
             'cub_device', 'cub_device_reduce_sum', 'cub_device_reduce', 'cub_device_reduce_by_key',
             'cub_device_scan_inclusive_scan', 'cub_device_scan_exclusive_scan',
             'cub_device_scan_inclusive_sum','cub_device_scan_exclusive_sum','cub_device_select_unique',
             'cub_device_select_flagged','cub_device_run_length_encide_encode', 'cub_counting_iterator',
             'cub_transform_iterator', 'activemask', 'complex',
             'user_defined_rules', 'math-exec', 'math-saturatef', 'math-habs', 'cudnn-activation',
             'cudnn-fill', 'cudnn-lrn', 'cudnn-memory', 'cudnn-pooling', 'cudnn-reorder', 'cudnn-scale', 'cudnn-softmax',
             'cudnn-sum', 'math-funnelshift', 'ccl', 'thrust-sort_by_key', 'thrust-find', 'thrust-inner_product', 'thrust-reduce_by_key',
             'math-bfloat16', 'libcu_atomic', 'test_shared_memory', 'cudnn-reduction', 'cudnn-binary', 'cudnn-bnp1', 'cudnn-bnp2', 'cudnn-bnp3',
             'cudnn-normp1', 'cudnn-normp2', 'cudnn-normp3', 'cudnn-convp1', 'cudnn-convp2', 'cudnn-convp3', 'cudnn-convp4', 'cudnn-convp5',
             'thrust-unique_by_key', 'cufft_test', "pointer_attributes", 'math_intel_specific', 'math-drcp']

oneDNN_related = ['cudnn-activation', 'cudnn-fill', 'cudnn-lrn', 'cudnn-memory',
             'cudnn-pooling', 'cudnn-reorder', 'cudnn-scale', 'cudnn-softmax', 'cudnn-sum', 'cudnn-reduction',
             'cudnn-binary', 'cudnn-bnp1', 'cudnn-bnp2', 'cudnn-bnp3', 'cudnn-normp1', 'cudnn-normp2', 'cudnn-normp3',
             'cudnn-convp1', 'cudnn-convp2', 'cudnn-convp3', 'cudnn-convp4', 'cudnn-convp5']

thrust_related = ['thrust-vector-2', 'thrust-binary-search', 'thrust-count', 'thrust-copy', 'thrust-transform-if',
                'thrust-policy', 'thrust-list', 'thrust-gather', 'thrust-scatter', 'thrust-unique_by_key_copy', 
                'thrust-for-hypre', 'thrust-find', 'thrust-sort_by_key', 'thrust-inner_product', 'thrust-reduce_by_key']

oneDPL_related = ['thrust-vector', 'thrust-for-h2o4gpu', 'thrust-for-RapidCFD', 'cub_device',
             'cub_block_p2', 'DplExtrasDpcppExtensions_api_test1', 'DplExtrasDpcppExtensions_api_test2',
             'DplExtrasDpcppExtensions_api_test3', 'DplExtrasDpcppExtensions_api_test4']


def setup_test():
    return True

def migrate_test():
    return True

def build_test():
    if test_config.current_test in oneDNN_related:
        return True
    if test_config.current_test in thrust_related:
        return True
    srcs = []
    cmp_options = []
    link_opts = []
    objects = []

    if test_config.current_test == 'ccl':
        link_opts.append('-lccl -lmpi')

    for dirpath, dirnames, filenames in os.walk(test_config.test_src_dir):
        for filename in [f for f in filenames if re.match('.*(cpp|c|cu)$', f)]:
            srcs.append(os.path.abspath(os.path.join(dirpath, filename)))

    print("before_link_opts: {}".format(link_opts))
    if platform.system() == 'Linux':
        link_opts.append(' -lpthread ')
    print("after_link_opts: {}".format(link_opts))

    ret = False
    if test_config.current_test == 'cufft_test':
        ret = compile_and_link([os.path.join(test_config.out_root, 'cufft_test.dp.cpp')], cmp_options, objects, link_opts)
    elif test_config.current_test in exec_tests:
        ret = compile_and_link(srcs, cmp_options, objects, link_opts)
    elif re.match('^cufft.*', test_config.current_test) and platform.system() == 'Linux':
        ret = compile_and_link(srcs, cmp_options, objects, link_opts)
    else:
        ret = compile_files(srcs, cmp_options)
    return ret


def run_test():
    if test_config.current_test not in exec_tests:
        return True
    # skip DNN
    if test_config.current_test in oneDNN_related:
        return True
    if test_config.current_test in thrust_related:
        return True

    if test_config.current_test == 'ccl':
        return call_subprocess('mpirun -n 2 ' + os.path.join(os.path.curdir, test_config.current_test + '.run '))
    return run_binary_with_args()

