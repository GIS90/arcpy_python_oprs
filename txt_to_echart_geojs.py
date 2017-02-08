# -*- coding: utf-8 -*-

import codecs
import os


def TransferJson(txtFile):
    fwDir = os.path.abspath(os.path.basename(txtFile))
    fwName = os.path.splitext(txtFile)[0] + '.json'
    fwPath = os.path.join(fwDir, fwName)
    if os.path.exists(fwPath):
        os.unlink(fwPath)
    fw = codecs.open(fwPath, 'w', 'utf-8')
    fw.write('var populationDayData={')
    fw.write('\n')
    fCont = open(txtFile).readlines()
    fNum = 1
    for line in fCont:
        try:
            fw.write('\t')
            day = line.split('\t')[0].decode('utf-8')
            fw.write('"%s":' % day)
            fw.write('\r\t')
            population = int(float(line.split('\t')[1]))
            resident = int(float(line.split('\t')[2]))
            noworker = int(float(line.split('\t')[3]))
            workder = int(float(line.split('\t')[4]))
            outlander = int(float(line.split('\t')[5]))
            passer = int(float(line.split('\t')[6]))
            tourist = int(float(line.split('\t')[7]))
            outlandresident = int(float(line.split('\t')[8].split('\n')[0]))
            info = '{"population":"%s","resident":"%s","noworker":"%s","workder":"%s","outlander":"%s","passer":"%s","tourist":"%s","outlandresident":"%s"}' % (
            population, resident, noworker, workder, outlander, passer, tourist, outlandresident)
            fw.write(info)
            fw.write(',') if fNum < len(fCont) else 0
            fNum += 1
            fw.write('\r\n')
        except Exception as e:
            print e.message
    fw.write('}')
    fw.close()


if __name__ == '__main__':
    print
    txt = r'E:\data\qdsjxl\population_day.txt'
    TransferJson(txtFile=txt)
