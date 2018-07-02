import sys

import rlp
import state.util.utils as utils
from state.db.db import BaseDB
from storage.kv_store import KeyValueStorage

DEATH_ROW_OFFSET = 2**62
ZERO_ENCODED = utils.encode_int(0)
ONE_ENCODED = utils.encode_int(1)


class RefcountDB(BaseDB):

    def __init__(self, keyValueStorage: KeyValueStorage):
        self._keyValueStorage = keyValueStorage
        self.journal = []
        self.death_row = []
        self.ttl = 500
        self.logging = False

    # Increase the reference count associated with a key
    def inc_refcount(self, k, v):
        # raise Exception("WHY AM I CHANGING A REFCOUNT?!:?")
        try:
            node_object = rlp.decode(self._keyValueStorage.get(b'r:' + k))
            refcount = utils.decode_int(node_object[0])
            self.journal.append([node_object[0], k])
            if refcount >= DEATH_ROW_OFFSET:
                refcount = 0
            new_refcount = utils.encode_int(refcount + 1)
            self._keyValueStorage.put(b'r:' + k, rlp.encode([new_refcount, v]))
            if self.logging:
                sys.stderr.write('increasing %s %r to: %d\n' % (
                    utils.encode_hex(k), v, refcount + 1))
        except BaseException:
            self._keyValueStorage.put(b'r:' + k, rlp.encode([ONE_ENCODED, v]))
            self.journal.append([ZERO_ENCODED, k])
            if self.logging:
                sys.stderr.write('increasing %s %r to: %d\n' % (
                    utils.encode_hex(k), v, 1))

    put = inc_refcount

    # Decrease the reference count associated with a key
    def dec_refcount(self, k):
        # raise Exception("WHY AM I CHANGING A REFCOUNT?!:?")
        node_object = rlp.decode(self._keyValueStorage.get(b'r:' + k))
        refcount = utils.decode_int(node_object[0])
        if self.logging:
            sys.stderr.write('decreasing %s to: %d\n' % (
                utils.encode_hex(k), refcount - 1))
        if not refcount > 0:
            raise ValueError(
                "node object for key {} has {} number "
                "of references, expected > 0"
                .format(k, refcount)
            )
        self.journal.append([node_object[0], k])
        new_refcount = utils.encode_int(refcount - 1)
        self._keyValueStorage.put(
            b'r:' + k, rlp.encode([new_refcount, node_object[1]]))
        if new_refcount == ZERO_ENCODED:
            self.death_row.append(k)

    delete = dec_refcount

    def get_refcount(self, k):
        try:
            o = utils.decode_int(self._keyValueStorage.get(b'r:' + k))[0]
            if o >= DEATH_ROW_OFFSET:
                return 0
            return o
        except BaseException:
            return 0

    # Get the value associated with a key
    def get(self, k):
        return rlp.decode(self._keyValueStorage.get(b'r:' + k))[1]

    # Kill nodes that are eligible to be killed, and remove the associated
    # deathrow record. Also delete old journals.
    def cleanup(self, epoch):
        try:
            death_row_node = self._keyValueStorage.get(
                'deathrow:' + str(epoch))
        except BaseException:
            death_row_node = rlp.encode([])
        death_row_nodes = rlp.decode(death_row_node)
        pruned = 0
        for nodekey in death_row_nodes:
            try:
                refcount, val = rlp.decode(
                    self._keyValueStorage.get(b'r:' + nodekey))
                if utils.decode_int(refcount) == DEATH_ROW_OFFSET + epoch:
                    self._keyValueStorage.remove(b'r:' + nodekey)
                    pruned += 1
            except BaseException:
                pass
        sys.stderr.write('%d nodes successfully pruned\n' % pruned)
        # Delete the deathrow after processing it
        try:
            self._keyValueStorage.remove('deathrow:' + str(epoch))
        except BaseException:
            pass
        # Delete journals that are too old
        try:
            self._keyValueStorage.remove('journal:' + str(epoch - self.ttl))
        except BaseException:
            pass

    # Commit changes to the journal and death row to the database
    def commit_refcount_changes(self, epoch):
        # Save death row nodes
        timeout_epoch = epoch + self.ttl
        try:
            death_row_nodes = rlp.decode(
                self._keyValueStorage.get('deathrow:' + str(timeout_epoch)))
        except BaseException:
            death_row_nodes = []
        for nodekey in self.death_row:
            refcount, val = rlp.decode(
                self._keyValueStorage.get(b'r:' + nodekey))
            if refcount == ZERO_ENCODED:
                new_refcount = utils.encode_int(
                    DEATH_ROW_OFFSET + timeout_epoch)
                self._keyValueStorage.put(
                    b'r:' + nodekey, rlp.encode([new_refcount, val]))
        if len(self.death_row) > 0:
            sys.stderr.write('%d nodes marked for pruning during block %d\n' %
                             (len(self.death_row), timeout_epoch))
        death_row_nodes.extend(self.death_row)
        self.death_row = []
        self._keyValueStorage.put('deathrow:' + str(timeout_epoch),
                                  rlp.encode(death_row_nodes))
        # Save journal
        try:
            journal = rlp.decode(
                self._keyValueStorage.get('journal:' + str(epoch)))
        except BaseException:
            journal = []
        journal.extend(self.journal)
        self.journal = []
        self._keyValueStorage.put('journal:' + str(epoch), rlp.encode(journal))

    # Revert changes made during an epoch
    def revert_refcount_changes(self, epoch):
        timeout_epoch = epoch + self.ttl
        # Delete death row additions
        try:
            self._keyValueStorage.remove('deathrow:' + str(timeout_epoch))
        except BaseException:
            pass
        # Revert journal changes
        try:
            journal = rlp.decode(
                self._keyValueStorage.get('journal:' + str(epoch)))
            for new_refcount, hashkey in journal[::-1]:
                node_object = rlp.decode(
                    self._keyValueStorage.get(b'r:' + hashkey))
                k = b'r:' + hashkey
                v = rlp.encode([new_refcount, node_object[1]])
                self._keyValueStorage.put(k, v)
        except BaseException:
            pass

    def _has_key(self, key):
        return b'r:' + key in self._keyValueStorage

    def __contains__(self, key):
        return self._has_key(key)
