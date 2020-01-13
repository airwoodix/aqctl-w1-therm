import functools
import logging
from os.path import join, basename
import aiofiles


# w1_therm slaves family codes
# https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/Documentation/w1/slaves/w1_therm.rst
THERM_FAMILY_CODES = ["10", "22", "28", "3b", "42"]


logger = logging.getLogger(__name__)
open = functools.partial(aiofiles.open, encoding="ascii")


class SysFSW1Therm:
    def __init__(self, master_name, family_codes=THERM_FAMILY_CODES):
        self.master_path = join("/", "sys", "devices", master_name)
        self.family_codes = family_codes
        assert all(c in THERM_FAMILY_CODES for c in self.family_codes)
        self.slaves = []

    async def list_slaves(self):
        async with open(self.rel_path("w1_master_slaves")) as fp:
            self.slaves = [s.strip() for s in await fp.readlines()
                           if s[:2].lower() in self.family_codes]
        return self.slaves

    async def read_slave(self, slave_name):
        logging.debug("read_slave: %s", slave_name)
        async with open(self.rel_path(slave_name, "w1_slave")) as fp:
            crc_line = (await fp.readline()).strip()
            temp_line = (await fp.readline()).strip()

        if crc_line[-3:] != "YES":
            raise IOError(slave_name)

        return int(temp_line.split("=")[1]) / 1000.

    async def read_all_slaves(self):
        return {name: await self.read_slave(name)
                for name in self.slaves}

    def rel_path(self, *args):
        return join(self.master_path, *args)

    async def setup(self):
        await self.list_slaves()
        logging.info("found %s slave(s)", len(self.slaves))

    async def ping(self):
        try:
            async with open(self.rel_path("w1_master_name")) as fp:
                name = (await fp.readline()).strip()
        except:
            return False

        if name == basename(self.master_path):
            logger.debug("ping successful")
            return True
        else:
            return False
