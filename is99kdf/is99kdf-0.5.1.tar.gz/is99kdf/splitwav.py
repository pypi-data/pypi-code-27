def readwav(filename):
    import scipy,numpy
    from scipy.io import wavfile
    fs, x = wavfile.read(filename)

    if x.dtype == numpy.int16:
       print('convert int16 --> float32')
       x = x.astype(numpy.float32)/32768
    elif x.dtype == numpy.int32:
       print('convert int32 --> float32')
       x = x.astype(numpy.float32)/2147483648

    return x,fs

def writewav(filename, x, fs):
    import scipy,numpy
    from scipy.io import wavfile

    x = (x*32768).astype(numpy.int16)
    wavfile.write(filename,fs,x)

def splitdir(srcdir,dstdir):
    wavlist = findwav(srcdir)
    num = len(wavlist)
    for idx,wavfile in enumerate(wavlist):
        print(idx+1,wavfile)
        splitwav(wavfile,srcdir,dstdir)

def splitwav(wavfile,src,dst,db=30,pauinter=0.5,paust=0.15,paued=0.15):

    # 读录音文件
    import librosa
    x,fs = librosa.load(wavfile,None)
    # x = x[0:int(fs*60)]

    # 提取端点信息 
    ints = librosa.effects.split(x,db)

    # 按照停顿分组
    pauinter = int(pauinter*fs) # 句间停顿
    groups = []
    for idx,(st,ed) in enumerate(ints):
        # 和上一段的距离很近，放在同一组里面
        if idx>0 and st-ints[idx-1][1]<pauinter:
           groups[-1].append([st,ed])
        else:
           groups.append([[st,ed]])
    '''
    for gidx,group in enumerate(groups):
        for idx,[st,ed] in enumerate(group):
            print(gidx+1,idx+1,(ed-st)/fs,st/fs,ed/fs)
        print('')
    '''

    # 每个组的长度是否超过最大句长，是则重新切割
    # 不处理

    # 合并组内每一段
    ints = []
    for idx,group in enumerate(groups):
        st = group[0][0] 
        ed = group[-1][1]
        ints.append([st,ed])

    # 给每一段留有开头和结尾的空白段
    paust = int(paust*fs)
    paued = int(paued*fs)
    for idx,(st,ed) in enumerate(ints):

        # 上一段结束点
        if idx==0:
           edlast = 0
        else:
           edlast = ints[idx-1][1]

        # 下一段开始点
        if idx+1<len(ints):
           stnext = ints[idx+1][0]
        else:
           stnext = len(x)

        # 修改当前段开始结束点
        st = max(st - paust, edlast)
        ed = min(ed + paued, stnext)
        # print(idx+1,st/fs,ed/fs)

        # 保存切割结果
        y = x[st:ed]
        wavname = wavfile.split('/')[-1].replace('.wav','')
        dstfile = wavfile.replace(src,dst).replace('.wav','/%s-%03d-%.3f-%.3f.wav'%(wavname,idx+1,st/fs,ed/fs))
        dirname = '/'.join(dstfile.split('/')[0:-1])
        import os
        if not os.path.exists(dirname):
           os.makedirs(dirname)
        print('%03d: save... %s'%(idx+1,dstfile))
        writewav(dstfile,y,fs)

def findwav(dirname):
    import os
    totdir = 0
    result = []
    for maindir, subdir, file_name_list in os.walk(dirname):
        totdir += 1
        print('searching %d: %s'%(totdir, maindir))
        for filename in file_name_list:
            if filename.endswith('.wav'):
               apath = os.path.join(maindir,filename)
               result.append(apath)
    return result


if __name__ == "__main__":

   import sys

   splitdir(sys.argv[1],sys.argv[2])

