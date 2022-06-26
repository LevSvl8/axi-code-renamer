print("importing model")
from ora41_ORA_model import SCHEMA_TABLES
print("starting")
from sqlalchemy import Column

from sqlalchemy import LargeBinary, Text

def fix_packet_size(dest_class, packet_size):
    BLOB_PACKET_SIZE = 5
    CLOB_DIVIDER = 10


    has_clobs = False
    has_blobs = False

    if dest_class.__tablename__ != 'reportdesign':
        return None

    for col in dest_class.__table__.columns:  # type: Column
        print(col.name, col.type)
        if isinstance(col.type, LargeBinary):
            has_blobs = True
            break
        elif isinstance(col.type, Text):
            has_clobs = True
    if has_blobs:
        return BLOB_PACKET_SIZE
    elif has_clobs:
        return packet_size // CLOB_DIVIDER
    else:
        return packet_size



if __name__ == '__main__':
    packet_size = 1000
    for tab, cls in SCHEMA_TABLES.items():
        ps = fix_packet_size(cls, packet_size)
        # print(tab, ps)