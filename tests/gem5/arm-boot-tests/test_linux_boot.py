# Copyright (c) 2022 The Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import re

from typing import Optional

from testlib import *

if config.bin_path:
    resource_path = config.bin_path
else:
    resource_path = joinpath(absdirpath(__file__), "..", "resources")


def test_boot(
    cpu: str,
    num_cpus: int,
    cache_type: str,
    memory_class: str,
    length: str,
    to_tick: Optional[int] = None,
):

    name = f"{cpu}-cpu_{num_cpus}-cores_{cache_type}_{memory_class}_\
arm-boot-test"

    verifiers = []

    config_args = [
        "--cpu",
        cpu,
        "--num-cpus",
        str(num_cpus),
        "--mem-system",
        cache_type,
        "--dram-class",
        memory_class,
        "--resource-directory",
        resource_path,
    ]

    if to_tick:
        name += "_to-tick"
        exit_regex = re.compile(
            "Exiting @ tick {} because simulate\(\) limit reached".format(
                str(to_tick)
            )
        )
        verifiers.append(verifier.MatchRegex(exit_regex))
        config_args += ["--tick-exit", str(to_tick)]
    else:
        name += "_m5-exit"

    gem5_verify_config(
        name=name,
        verifiers=verifiers,
        fixtures=(),
        config=joinpath(
            config.base_dir,
            "tests",
            "gem5",
            "configs",
            "arm_boot_exit_run.py",
        ),
        config_args=config_args,
        valid_isas=(constants.all_compiled_tag,),
        valid_hosts=constants.supported_hosts,
        length=length,
    )


#### The long (pre-submit/Kokoro) tests ####

test_boot(
    cpu="atomic",
    num_cpus=1,
    cache_type="classic",
    memory_class="SingleChannelDDR3_1600",
    length=constants.quick_tag,
    to_tick=10000000000,
)

test_boot(
    cpu="timing",
    num_cpus=1,
    cache_type="classic",
    memory_class="SingleChannelDDR3_2133",
    length=constants.quick_tag,
    to_tick=10000000000,
)

test_boot(
    cpu="o3",
    num_cpus=1,
    cache_type="classic",
    memory_class="DualChannelDDR3_1600",
    length=constants.quick_tag,
    to_tick=10000000000,
)

test_boot(
    cpu="timing",
    num_cpus=4,
    cache_type="classic",
    memory_class="DualChannelDDR3_2133",
    length=constants.quick_tag,
    to_tick=10000000000,
)

#### The long (nightly) tests ####

test_boot(
    cpu="atomic",
    num_cpus=1,
    cache_type="classic",
    memory_class="SingleChannelDDR3_1600",
    length=constants.long_tag,
)

test_boot(
    cpu="timing",
    num_cpus=1,
    cache_type="classic",
    memory_class="SingleChannelDDR3_2133",
    length=constants.long_tag,
)

test_boot(
    cpu="o3",
    num_cpus=1,
    cache_type="classic",
    memory_class="DualChannelDDR3_1600",
    length=constants.long_tag,
)

test_boot(
    cpu="timing",
    num_cpus=4,
    cache_type="classic",
    memory_class="HBM2Stack",
    length=constants.long_tag,
)