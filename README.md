# ComputerOrganization-FinalProject
資工二A 112502502 范昕文

```
su+password
```
```
cd xxx
```

### Q1. GEM5 + NVMAIN BUILD-UP (40%)
(以下為PPT)
1. 編譯工具
```
sudo apt install build-essential git m4 scons zlib1g zlib1g-dev libprotobuf-dev protobuf-compiler
libprotoc-dev libgoogle-perftools-dev python3-dev python3-six python libboost-all-dev pkg-config
```
2. 安裝GEM5
3. 丟資料夾並解壓縮
4. 編譯GEM5
```
scons build/X86/gem5.opt -j8
```
5. 安裝NVMAIN
```
git clone https://github.com/SEAL-UCSB/NVmain
```
6. 修改 SCONSCRIPT，進入nvmain資料夾 點開 SConscript 把36行的from gem5_scons import Transform註解掉
7. 編譯NVMAIN
```
scons --build-type=fast
```
8. 修改GEM5 OPTIONS，在gem5/configs/common/Options.py中第133行加入下段程式
```
for arg in sys.argv:
  if arg[:9] == "--nvmain-":
  parser.add_option(arg, type="string", default="NULL", help="Set NVMain configuration value for a parameter")
```
9. 還原前面nvmain sconscript註解掉的指令
10. 混合編譯GEM5
```
scons EXTRAS=../NVmain build/X86/gem5.opt
```
11. 測試HELLOWORLD
```
./build/X86/gem5.opt configs/example/se.py \
  -c tests/test-progs/hello/bin/x86/linux/hello \
  --cpu-type=TimingSimpleCPU \
  --caches --l2cache \
  --mem-type=NVMainMemory \
  --nvmain-config=../NVmain/Config/PCM_ISSCC_2012_4GB.config
```

### Q2. Enable L3 last level cache in GEM5 + NVMAIN (15%)
1. 修改以下檔案
- `GEM5/configs/common/Caches.py`
- `GEM5/configs/common/Options.py`
- `GEM5/configs/common/CacheConfig.py`
- `GEM5/src/cpu/BaseCPU.py`
- `GEM5/src/mem/XBar.py`
2. 重新compile
```
scons EXTRAS=../NVmain build/X86/gem5.opt
```
3. 測試HELLOWORLD
```
./build/X86/gem5.opt configs/example/se.py \
-c tests/test-progs/hello/bin/x86/linux/hello \
--cpu-type=TimingSimpleCPU --caches --l2cache --l3cache --mem-type=NVMainMemory \
--nvmain-config=../NVmain/Config/PCM_ISSCC_2012_4GB.config
```

### Q3. Config last level cache to 2-way and full-way associative cache and test performance (15%)
1. 編譯quicksort.c
```
gcc --static quicksort.c -o quicksort
```
3. run(fullWays)
```
./build/X86/gem5.opt configs/example/se.py \
-c ../benchmark/quicksort --cpu-type=TimingSimpleCPU \
--caches --l1i_size=32kB --l1d_size=32kB --l2cache --l2_size=128kB \
--l3cache --l3_size=1MB --l3_assoc=16384 --mem-type=NVMainMemory \
--nvmain-config=../NVmain/Config/PCM_ISSCC_2012_4GB.config > cmdlog_full-way.txt
```
4. run(2Ways)
```
./build/X86/gem5.opt configs/example/se.py \
-c ../benchmark/quicksort --cpu-type=TimingSimpleCPU \
--caches --l1i_size=32kB --l1d_size=32kB --l2cache --l2_size=128kB \
--l3cache --l3_size=1MB --l3_assoc=2 --mem-type=NVMainMemory \
--nvmain-config=../NVmain/Config/PCM_ISSCC_2012_4GB.config > cmdlog_2-way.txt
```

### Q4. Modify last level cache policy based on frequency based replacement policy (15%)
1. 進入多重資料夾
```
src/mem/cache/replacement_policies
```
2. 加入以下檔案並修改
```
touch fb_rp.cc
```
```
nano fb_rp.cc
```
```
touch fb_rp.hh
```
```
nano fb_rp.hh
```
`Ctrl+S Ctrl+Z`
3. 修改以下檔案
- `GEM5/src/mem/cache/replacement_policies/ReplacementPolicies.py`
- `GEM5/src/mem/cache/replacement_policies/SConscript`
- `GEM5/configs/common/Caches.py`
4. 重新編譯
```
scons EXTRAS=../NVmain build/X86/gem5.opt
```
5.  run(frequency based policy)
```
./build/X86/gem5.opt configs/example/se.py \
-c ../benchmark/quicksort --cpu-type=TimingSimpleCPU \
--caches --l1i_size=32kB --l1d_size=32kB --l2cache --l2_size=128kB \
--l3cache --l3_size=1MB --l3_assoc=2 --mem-type=NVMainMemory \
--nvmain-config=../NVmain/Config/PCM_ISSCC_2012_4GB.config > cmdlog_FB.txt
```
6. run(orifinal policy)
```
./build/X86/gem5.opt configs/example/se.py \
-c ../benchmark/quicksort --cpu-type=TimingSimpleCPU \
--caches --l1i_size=32kB --l1d_size=32kB --l2cache --l2_size=128kB \
--l3cache --l3_size=1MB --l3_assoc=2 --mem-type=NVMainMemory \
--nvmain-config=../NVmain/Config/PCM_ISSCC_2012_4GB.config > cmdlog_LRU.txt
```

### Q5. Test the performance of write back and write through policy based on 4-way associative cache with isscc_pcm(15%)
1. 編譯multiply.c
```
gcc --static multiply.c -o multiply
```
2. 分別修改writeback, writethrough的檔案
- `GEM5/src/mem/cache/base.cc`
3. 重新編譯
```
scons EXTRAS=../NVmain build/X86/gem5.opt
```
4. run(writeback)
```
./build/X86/gem5.opt configs/example/se.py \
-c ../benchmark/multiply --cpu-type=TimingSimpleCPU \
--caches --l1i_size=32kB --l1i_assoc=4 --l1d_size=32kB --l1d_assoc=4 --l2cache --l2_size=128kB --l2_assoc=4 \
--l3cache --l3_size=1MB --l3_assoc=4 --mem-type=NVMainMemory \
--nvmain-config=../NVmain/Config/PCM_ISSCC_2012_4GB.config > cmdlog_before.txt
```
5. run(writethrough)
```
./build/X86/gem5.opt configs/example/se.py \
-c ../benchmark/multiply --cpu-type=TimingSimpleCPU \
--caches --l1i_size=32kB --l1i_assoc=4 --l1d_size=32kB --l1d_assoc=4 --l2cache --l2_size=128kB --l2_assoc=4 \
--l3cache --l3_size=1MB --l3_assoc=4 --mem-type=NVMainMemory \
--nvmain-config=../NVmain/Config/PCM_ISSCC_2012_4GB.config > cmdlog_after.txt
```
