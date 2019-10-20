import argparse
import hashlib
from zlib import crc32
from time import perf_counter

def hashfile(in_file, hasher, blocksize=65536):
    in_file.seek(0)
    for block in iter(lambda: in_file.read(blocksize), b""):
        hasher.update(block)
    return hasher.hexdigest()

def crcfile(in_file, crcfunc, blocksize=65536):
    crcval = 0
    in_file.seek(0)
    for block in iter(lambda: in_file.read(blocksize), b""):
        crcval = crcfunc(block, crcval)
    return crcval

t_start = perf_counter()

parser = argparse.ArgumentParser()
parser.add_argument('input_file', help='Input file name')
parser.add_argument('-a', help='Selects algorithm while A is one of <md5, sha1, sha256, crc32>')
args = parser.parse_args()
#print 'Input file is \'%s\'' % args.input_file

try:
    f = open(args.input_file, 'rb')
except IOError as e:
    #print 'Input file \'%s\' not found!' % args.input_file
    print("I/O error({0}): {1}".format(e.errno, e.strerror))
    exit(1)

hashval_md5 = hashfile(f, hashlib.md5())
hashval_sha1 = hashfile(f, hashlib.sha1())
hashval_sha256 = hashfile(f, hashlib.sha256())
#hashval_sha512 = hashfile(f, hashlib.sha512())
hashval_crc32 = crcfile(f, crc32)

print('MD5:   ', hashval_md5)
print('SHA1:  ', hashval_sha1)
print('SHA256:', hashval_sha256)
#print 'SHA512:', hashval_sha512
print('CRC32: ', hex(hashval_crc32)[2:])

t_delta = perf_counter()-t_start
print('Elapsed time: %4.3f s' % t_delta)

f.close()
exit(0)
