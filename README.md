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
libprotoc-dev libgoogle-perftools-dev python3-dev python3-six python libboost-all-dev pkgconfig
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
scons build/X86/gem5.opt -j$(nproc)
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

### Q3. Config last level cache to 2-way and full-way associative cache and test performance (15%)
### Q4. Modify last level cache policy based on frequency based replacement policy (15%)
### Q5. Test the performance of write back and write through policy based on 4-way associative cache with isscc_pcm(15%)
