import hashlib
from zlib import crc32
from time import clock
import argparse

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

parser = argparse.ArgumentParser()
parser.add_argument('input_file', help='Input file name')
parser.add_argument('-a', help='Selects algorithm, while <A> is one of [md5, sha1, sha256, sha512, crc32]')
parser.add_argument('-t', help='Print elapsed time', action='store_true')
args = parser.parse_args()
#print 'Input file is \'%s\'' % args.input_file

t_start = clock()

try:
    f = open(args.input_file, 'rb')
except IOError as e:
    #print 'Input file \'%s\' not found!' % args.input_file
    print "I/O error({0}): {1}: \'{2}\'".format(e.errno, e.strerror, args.input_file)
    exit(1)

if args.a == 'md5':
    hashval_md5 = hashfile(f, hashlib.md5())
    print 'MD5:', hashval_md5
elif args.a == 'sha1':
    hashval_sha1 = hashfile(f, hashlib.sha1())
    print 'SHA1:', hashval_sha1
elif args.a == 'sha256':
    hashval_sha256 = hashfile(f, hashlib.sha256())
    print 'SHA256:', hashval_sha256
elif args.a == 'sha512':
    hashval_sha512 = hashfile(f, hashlib.sha512())
    print 'SHA512:', hashval_sha512
elif args.a == 'crc32':
    hashval_crc32 = crcfile(f, crc32)
    print 'CRC32:', hex(hashval_crc32)[2:]
else:
    print 'Unknown hash algorithm:', args.a
    exit(1)

f.close()

t_delta = clock()-t_start

if args.t:
    print 'Elapsed time: %4.3f s' % t_delta

exit(0)
