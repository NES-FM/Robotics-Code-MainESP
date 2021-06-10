Python 3.8.3 (tags/v3.8.3:6f8c832, May 13 2020, 22:37:02) [MSC v.1924 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> "\x01"
'\x01'
>>> int("\x01")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: invalid literal for int() with base 10: '\x01'
>>> atoi("\x01")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'atoi' is not defined
>>> "\x01"[0]
'\x01'
>>> ord("\x01"[0])
1
>>> chr(-2)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: chr() arg not in range(0x110000)
>>> hex(-1)
'-0x1'
>>> 0b10000110
134
>>> int.from_bytes(0b10000110, signed=True)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: from_bytes() missing required argument 'byteorder' (pos 2)
>>> int.from_bytes(0b10000110, byteorder="big", signed=True)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: cannot convert 'int' object to bytes
>>> int.from_bytes("\b10000110", byteorder="big", signed=True)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: cannot convert 'str' object to bytes
>>> int.from_bytes(b"\b10000110", byteorder="big", signed=True)
151118338479942086960
>>> int.from_bytes(b"\b10000110", byteorder="little", signed=True)
888988382903300796680
>>> b"\b10000110"
b'\x0810000110'
>>> int(b"\b10000110")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: invalid literal for int() with base 10: b'\x0810000110'
>>> b"\b10000110"[0]
8
>>> b"\b10000110"[1]
49
>>> b"\b10000110"[2]
48
>>> b"\b10000110"[3]
48
>>> b"\x86"
b'\x86'
>>> int.from_bytes(b"\x86", byteorder="little", signed=True)
-122
>>> int.from_bytes(b"\x86", byteorder="big", signed=True)
-122
>>> int.from_bytes(b"\xE", byteorder="big", signed=True)
  File "<stdin>", line 1
SyntaxError: (value error) invalid \x escape at position 0
>>> int.from_bytes(b"\xe", byteorder="big", signed=True)
  File "<stdin>", line 1
SyntaxError: (value error) invalid \x escape at position 0
>>> int.from_bytes(b"\x0e", byteorder="big", signed=True)
14
>>> -5.to_bytes()
  File "<stdin>", line 1
    -5.to_bytes()
       ^
SyntaxError: invalid syntax
>>> i = -5
>>> i.to_bytes()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: to_bytes() missing required argument 'length' (pos 1)
>>> i.to_bytes(8)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: to_bytes() missing required argument 'byteorder' (pos 2)
>>> i.to_bytes(8, "big")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
OverflowError: can't convert negative int to unsigned
>>> i.to_bytes(8, "big", signed=True)
b'\xff\xff\xff\xff\xff\xff\xff\xfb'
>>> int.from_bytes(i.to_bytes(8, "big", signed=True), byteorder="big", signed=True)
-5
>>> int.from_bytes((5).to_bytes(8, "big", signed=True), byteorder="big", signed=True)
5
>>> int.from_bytes((5).to_bytes(8, "big", signed=True), byteorder="big", signed=True)
5
>>> (5).to_bytes(8, "big", signed=True)
b'\x00\x00\x00\x00\x00\x00\x00\x05'
>>> int.
int.as_integer_ratio( int.conjugate(        int.from_bytes(       int.mro(              int.real
int.bit_length(       int.denominator       int.imag              int.numerator         int.to_bytes(
>>> int.from_bytes("A"
... )
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: from_bytes() missing required argument 'byteorder' (pos 2)
>>> int.from_bytes("A", byteorder="big", signed=True)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: cannot convert 'str' object to bytes
>>> int.from_bytes("\x05", byteorder="big", signed=True)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: cannot convert 'str' object to bytes
>>> int.from_bytes("\x05", byteorder="big", signed=True)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: cannot convert 'str' object to bytes
>>> s = "\x05"
>>> s.
s.capitalize(   s.find(         s.isdecimal(    s.istitle(      s.partition(    s.rstrip(       s.translate(
s.casefold(     s.format(       s.isdigit(      s.isupper(      s.replace(      s.split(        s.upper(
s.center(       s.format_map(   s.isidentifier( s.join(         s.rfind(        s.splitlines(   s.zfill(
s.count(        s.index(        s.islower(      s.ljust(        s.rindex(       s.startswith(
s.encode(       s.isalnum(      s.isnumeric(    s.lower(        s.rjust(        s.strip(
s.endswith(     s.isalpha(      s.isprintable(  s.lstrip(       s.rpartition(   s.swapcase(
s.expandtabs(   s.isascii(      s.isspace(      s.maketrans(    s.rsplit(       s.title(
>>> s.en
s.encode(   s.endswith(
>>> s.encode("UTF-8")
b'\x05'
>>> int.from_bytes("\x05".encode("UTF-8"), byteorder="big", signed=True)
5
>>> (-5).to_bytes(1, byteorder="big", signed=True)
b'\xfb'
>>> int.from_bytes("\xfb".encode("UTF-8"), byteorder="big", signed=True)
-15429
>>> int.from_bytes("\xfb".encode("UTF-8"), byteorder="little", signed=True)
-17469
>>> int.from_bytes("\xfb".encode("UTF-8"), byteorder="big", signed=True)
-15429
>>> "\xfb".encode("UTF-8")
b'\xc3\xbb'
>>> byte
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'byte' is not defined
>>> bytes
<class 'bytes'>
>>> bytes("A")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: string argument without an encoding
>>> bytes("A", "raw")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
LookupError: unknown encoding: raw
>>> bytes("\xfb", "UTF-8")
b'\xc3\xbb'
>>> ord("\xfb")
251
>>> bytes(ord("\xfb"))
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
>>> i = ord("\xfb")
>>> i.
i.as_integer_ratio( i.conjugate(        i.from_bytes(       i.numerator         i.to_bytes(
i.bit_length(       i.denominator       i.imag              i.real
>>> i.to_bytes()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: to_bytes() missing required argument 'length' (pos 1)
>>> i.to_bytes(1)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: to_bytes() missing required argument 'byteorder' (pos 2)
>>> i.to_bytes(1, byteorder="big")
b'\xfb'
>>> i.to_bytes(1, byteorder="big")
b'\xfb'
>>> int.from_bytes(i.to_bytes(1, byteorder="big"), byteorder="big", signed=True)
-5
>>> int.from_bytes(ord("\x02").to_bytes(1, byteorder="big"), byteorder="big", signed=True)
2
>>> bytes.fromhex("fb")
b'\xfb'
>>> hex("\xfb")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'str' object cannot be interpreted as an integer
>>> bytes.fromhex("\xfb")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: non-hexadecimal number found in fromhex() arg at position 0
>>> "\x01"
'\x01'
>>> print("\x01")
☺
>>> print("\x02")
☻
>>> print("\x05")
♣
>>> print("\x07")

>>> print("\x61")
a
>>> print("\x81")

>>> print("\x41")
A
>>> ord("\xfb")
251
>>> ord("\xfb")-0x100000000
-4294967045
>>> ord("\xfb")-0x10000
-65285
>>> ord("\xfb")-0x1000
-3845
>>> ord("\xfb")-0x100
-5
>>> ~0xfb
-252
>>>

_thread.stop(1073623772)
