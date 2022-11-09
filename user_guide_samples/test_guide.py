# ====------ test_guide.py---------- *- Python -* ----===##
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

def setup_test():
    return True

def migrate_test():
    return True

def build_test():
    srcs = []
    cmp_opts = []
    link_opts = []
    objects = []

    for dirpath, dirnames, filenames in os.walk(test_config.test_src_dir):
        for filename in [f for f in filenames if re.match('.*(cpp|c|cu)$', f)]:
            srcs.append(os.path.abspath(os.path.join(dirpath, filename)))

    ret = False
    ret = compile_and_link(srcs, cmp_opts)
    return ret

def run_test():
    # change_dir(test_config.current_test)
    # test_driver = test_config.current_test + ".py"
    # options = " \" \""
    # # os.environ['SYCL_DEVICE_FILTER'] = test_config.device_filter
    # call_subprocess("python " + test_driver + options)
    # if "case pass" in test_config.command_output:
    #     return True
    # return False
    args = []
    return run_binary_with_args(args)
