#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import unittest

import tgcrypto


class TestBufferRelease(unittest.TestCase):
    # A bytearray cannot be resized while a buffer exported from it is still held,
    # so a resize after a rejected call proves every argument buffer was released.

    def assertReleased(self, *buffers: bytearray):
        for buffer in buffers:
            buffer.append(0)

    def test_ige256_rejected_arguments(self):
        data, key, iv = bytearray(15), bytearray(32), bytearray(32)

        for function in (tgcrypto.ige256_encrypt, tgcrypto.ige256_decrypt):
            with self.assertRaises(ValueError):
                function(data, key, iv)

        self.assertReleased(data, key, iv)

    def test_ctr256_rejected_arguments(self):
        data, key, iv, state = bytearray(16), bytearray(32), bytearray(16), bytearray([16])

        for function in (tgcrypto.ctr256_encrypt, tgcrypto.ctr256_decrypt):
            with self.assertRaises(ValueError):
                function(data, key, iv, state)

        self.assertReleased(data, key, iv, state)

    def test_ctr256_accepted_arguments(self):
        data, key, iv, state = bytearray(16), bytearray(32), bytearray(16), bytearray(1)

        tgcrypto.ctr256_encrypt(data, key, iv, state)

        self.assertReleased(data, key, iv, state)

    def test_cbc256_rejected_arguments(self):
        data, key, iv = bytearray(16), bytearray(32), bytearray(15)

        for function in (tgcrypto.cbc256_encrypt, tgcrypto.cbc256_decrypt):
            with self.assertRaises(ValueError):
                function(data, key, iv)

        self.assertReleased(data, key, iv)


if __name__ == "__main__":
    unittest.main()
