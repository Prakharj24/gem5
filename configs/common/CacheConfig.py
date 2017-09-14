# Copyright (c) 2012-2013, 2015 ARM Limited
# All rights reserved
# 
# The license below extends only to copyright in the software and shall
# not be construed as granting a license to any other intellectual
# property including but not limited to intellectual property relating
# to a hardware implementation of the functionality of the software
# licensed hereunder.  You may use the software subject to the license
# terms below provided that you ensure that this notice is replicated
# unmodified and in its entirety in all distributions of the software,
# modified or unmodified, in source code or in binary form.
# 
# Copyright (c) 2010 Advanced Micro Devices, Inc.
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
#
# Authors: Lisa Hsu

# Configure the M5 cache hierarchy config in one place
#

import m5
from m5.objects import *
from Caches import *

def config_cache(options, system):

    if options.cpu_type == "arm_detailed":
        try:
            from O3_ARM_v7a import *
        except:
            print "arm_detailed is unavailable. Did you compile the O3 model?"
            sys.exit(1)

        dcache_class, icache_class, l2_cache_class, l3_cache_class = \
            O3_ARM_v7a_DCache, O3_ARM_v7a_ICache, O3_ARM_v7aL2, O3_ARM_v7aL3
    else:
        dcache_class, icache_class, l2_cache_class, l3_cache_class = \
            L1Cache, L1Cache, L2Cache, L3Cache

    # Set the cache line size of the system
    system.cache_line_size = options.cacheline_size
	
	#This option is for the case that we have just Icache, Dcache and l2cache
    #if options.l2cache:
        # Provide a clock for the L2 and the L1-to-L2 bus here as they
        # are not connected using addTwoLevelCacheHierarchy. Use the
        # same clock as the CPUs.
     #   system.l2 = l2_cache_class(clk_domain=system.cpu_clk_domain,
      #                             size=options.l2_size,
       #                            assoc=options.l2_assoc)

#        system.tol2bus = L2XBar(clk_domain = system.cpu_clk_domain)
 #       system.l2.cpu_side = system.tol2bus.master
#	system.l2.mem_side = system.membus.slave
#	system.l2.prefetcher = BOPrefetcher()

	#This option is added because we want to have a three level hierarchy
	#in multicore system. private Icache, Dcahe and l2cache for each core (cpu[i]) and a shared l3cache
 
    if options.l3cache:
        # Provide a clock for the L3 and the L2-to-L3 bus here as they
        # are not connected using addTwoLevelCacheHierarchy. Use the
        # same clock as the CPUs.
        system.l3 = l3_cache_class(clk_domain=system.cpu_clk_domain,
                                   size=options.l3_size,
                                   assoc=options.l3_assoc)

        system.tol3bus = L2XBar(clk_domain = system.cpu_clk_domain)
        system.l3.cpu_side = system.tol3bus.master
        system.l3.mem_side = system.membus.slave
	
	#we don't use prefetcher for l3cache
        #system.l3.prefetcher = NLPrefetcher()


    if options.memchecker:
        system.memchecker = MemChecker()

    for i in xrange(options.num_cpus):
        if options.caches:

	#here we initialize all cache levels (Icache, Dcache and l2cache which is needed for each core(cpu[i])
            icache = icache_class(size=options.l1i_size,
                                  assoc=options.l1i_assoc)
            dcache = dcache_class(size=options.l1d_size,
                                  assoc=options.l1d_assoc)

	    l2cache = l2_cache_class(size=options.l2_size,
                                     assoc=options.l2_assoc)

	#apply a prefetcher for l2 cache
	#so for each cpu[i] this code makes an Icache, Dcache, l2cache and l2prefetcher
            l2cache.prefetcher = SandboxPrefetcher()

            if options.memchecker:
                dcache_mon = MemCheckerMonitor(warn_only=True)
                dcache_real = dcache

                # Do not pass the memchecker into the constructor of
                # MemCheckerMonitor, as it would create a copy; we require
                # exactly one MemChecker instance.
                dcache_mon.memchecker = system.memchecker

                # Connect monitor
                dcache_mon.mem_side = dcache.cpu_side

                # Let CPU connect to monitors
                dcache = dcache_mon

            # When connecting the caches, the clock is also inherited
            # from the CPU in question
            if buildEnv['TARGET_ISA'] == 'ALPHA':
                system.cpu[i].addPrivateSplitL1Caches(icache, dcache,
                                                      PageTableWalkerCache(),
                                                      PageTableWalkerCache())
            else:
               # system.cpu[i].addPrivateSplitL1Caches(icache, dcache)
		
		#this function makes a hierarchy of icache, dcache and l2cache (for each cpu[i]
		#and also makes all the connections so there is no need to write the codes in lines 162-164
		system.cpu[i].addTwoLevelCacheHierarchy(icache, dcache, l2cache)

            if options.memchecker:
                # The mem_side ports of the caches haven't been connected yet.
                # Make sure connectAllPorts connects the right objects.
                system.cpu[i].dcache = dcache_real
                system.cpu[i].dcache_mon = dcache_mon

#	if options.l2cache:
		#there is no need to make an Xbar for each cpu[i]
		#system.tol2bus = L2XBar(clk_domain = system.cpu_clk_domain)

	       #	system.cpu[i].tol2bus = L2XBar(clk_domain = system.cpu_clk_domain)
#       		system.cpu[i].cpu_side = system.tol2bus.master
#	       	system.cpu[i].mem_side = system.tol3bus.slave

	elif options.external_memory_system:
            # These port names are presented to whatever 'external' system
            # gem5 is connecting to.  Its configuration will likely depend
            # on these names.  For simplicity, we would advise configuring
            # it to use this naming scheme; if this isn't possible, change
            # the names below.
			if buildEnv['TARGET_ISA'] in ['x86', 'arm']:
 		          	system.cpu[i].addTwoLevelCacheHierarchy(
        	                ExternalCache("cpu%d.icache" % i),
   	                        ExternalCache("cpu%d.dcache" % i),
 	                        ExternalCache("cpu%d.l2cache" % i),
                      	        ExternalCache("cpu%d.itb_walker_cache" % i),
 	                        ExternalCache("cpu%d.dtb_walker_cache" % i))
		       	else:
 				system.cpu[i].addTwoLevelCacheHierarchy(icache, dcache, l2cache)
                	#system.cpu[i].addPrivateSplitL1Caches(
                        #	ExternalCache("cpu%d.icache" % i),
                        #	ExternalCache("cpu%d.dcache" % i))

        system.cpu[i].createInterruptController()
        #if options.l2cache:
            #system.cpu[i].connectAllPorts(system.tol2bus, system.membus)
	 #   system.cpu[i].connectAllPorts(system.tol2bus, system.tol3bus)
	if options.l3cache:
            system.cpu[i].connectAllPorts(system.tol3bus, system.membus)
       # elif options.external_memory_system:
       #     system.cpu[i].connectUncachedPorts(system.membus)
        else:
            system.cpu[i].connectAllPorts(system.membus)

    return system

# ExternalSlave provides a "port", but when that port connects to a cache,
# the connecting CPU SimObject wants to refer to its "cpu_side".
# The 'ExternalCache' class provides this adaptation by rewriting the name,
# eliminating distracting changes elsewhere in the config code.
class ExternalCache(ExternalSlave):
    def __getattr__(cls, attr):
        if (attr == "cpu_side"):
            attr = "port"
        return super(ExternalSlave, cls).__getattr__(attr)

    def __setattr__(cls, attr, value):
        if (attr == "cpu_side"):
            attr = "port"
        return super(ExternalSlave, cls).__setattr__(attr, value)

def ExternalCacheFactory(port_type):
    def make(name):
        return ExternalCache(port_data=name, port_type=port_type,
                             addr_ranges=[AllMemory])
    return make
