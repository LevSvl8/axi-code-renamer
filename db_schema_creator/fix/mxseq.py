# coding: utf-8

from sqlalchemy import Column, Sequence, BigInteger, Unicode
from sqlalchemy.ext.declarative import declarative_base

from aconn import AConnector

from axi_renamer.renamer_starter import Renamer

ExtractorBase = declarative_base()  # metadata = ExtractorBase.metadata

class MaxsequenceExtractor(ExtractorBase):
    __tablename__ = 'maxsequence'
    __table_args__ = {'schema': 'maximo'}

    tbname = Column(Unicode(30), nullable=False)  # table
    name = Column(Unicode(30), nullable=False)  # column
    sequencename = Column(Unicode(30), nullable=False)
    maxreserved = Column(BigInteger, nullable=False)  # NOT FUCK!!! current value
    maxsequenceid = Column(BigInteger, primary_key=True)


def copy_max_sequences(src: AConnector, dest: AConnector, seq_lowercase, dbType: str):
    # get maxseq - main sequence
    sequences = {}

    src.log('Extracting sequences')
    for seq in src.con.query(MaxsequenceExtractor).all():  # type: MaxsequenceExtractor
        seq_name = str(seq.sequencename)

        if seq_lowercase:
            seq_name = seq_name.lower()

        sql = 'SELECT MAX(%s) FROM %s' % (seq.name, seq.tbname)
        try:
            cnt = src.sql(sql).fetchone()[0]
            if cnt is None:
                cnt = 0
            cnt = int(cnt)
        except:
            cnt = seq.maxreserved
            src.log('Sequence %s table %s not exist. Using maxreserved %s ' % (seq.sequencename, seq.tbname, seq.maxreserved))

        sequences[seq_name] = cnt + 1

    if seq_lowercase:
        maxseq = 'maxseq'
    else:
        maxseq = 'MAXSEQ'
    sequences[maxseq] = int(src.con.execute(Sequence('maxseq'))) + 1

    dest.log('Creating sequences')
    for seq_name, seq_start in sequences.items():
        if seq_lowercase:
            seq_name = seq_name.lower()
        else:
            seq_name = seq_name.upper()

        seq_name = Renamer().get_axi_val(seq_name)

        print(seq_name, seq_start)

        if str(seq_name).lower() != 'maxseq' and str(seq_name).lower() != 'axiseq':
            try:
                Sequence(seq_name).drop(dest.engine)
                #dest.log('Sequence %s dropped' % seq_name)
            except:
                pass
        try:
            if dbType == 'DB2':
                sql = 'CREATE SEQUENCE "%s" AS BIGINT START WITH %s' % (seq_name, seq_start)
                dest.sql(sql)
            else:
                Sequence(seq_name, start=seq_start).create(dest.engine)
        except Exception as e:
            dest.log('WARNING: Sequence %s not created: %s' % (seq_name, str(e)))
    dest.log('Done!')

# if __name__ == '__main__':
#     db_src = AConnector('src', 'postgresql://maximo:maximo@192.168.10.127/max1')
#     db_dest = AConnector('dest', 'postgresql://maximo:maximo@192.168.10.127/max1')
#
#     copy_max_sequences(db_src, db_dest, True)

#
# def __start():
#     db_src = AConnector('src', 'postgresql://maximo:maximo@192.168.11.77/MAX1')
#     db_dest = AConnector('src', 'postgresql://maximo:maximo@192.168.11.77/MAX2')
#
#     copy_max_sequences(db_src, db_dest, True)
