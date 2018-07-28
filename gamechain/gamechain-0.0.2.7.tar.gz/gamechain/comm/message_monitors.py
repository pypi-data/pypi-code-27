import asyncio
from gamechain.lobby import game_shelves, gcl_message

MONITOR_INTERVAL = 0.2


class MessageMonitor:

    def __init__(self, gc_monitor):
        self._monitor = gc_monitor
        self._keep_monitoring = True
        self._response_txid = None
        self._response_gcl_msg = None

    async def _await_response(self):
        while self._keep_monitoring:
            if self._response_txid is not None:
                response_txid = self._response_txid
                self._response_txid = None

                response_gcl_msg = self._response_gcl_msg
                if self._response_gcl_msg is None:
                    response_gcl_msg = gcl_message.receive_message_by_txid(response_txid)

                self._response_gcl_msg = None

                return response_gcl_msg

            await asyncio.sleep(MONITOR_INTERVAL)

    def await_response(self, message_filter):
        self._monitor.register_tx_handler(message_filter)

        loop = asyncio.get_event_loop()
        response_gcl_msg = loop.run_until_complete(self._await_response())

        self._monitor.un_register_tx_handler(message_filter)
        return response_gcl_msg

    def set_response_txid(self, response_txid):
        self._response_txid = response_txid

    def set_response_tx(self, response_txid, gcl_msg):
        self._response_txid = response_txid
        self._response_gcl_msg = gcl_msg


class LfgMonitor(MessageMonitor):

    def __init__(self, gc_monitor, game_id):
        super().__init__(gc_monitor)
        self._game_id = game_id

    def _filter_tx_for_challenge(self, tx):
        if gcl_message.check_if_message_is_for_addr(tx, self._game_id):
            txid = tx['txid']
            # self.set_response(txid)
            # print(f"Challenged offered: {txid}")

            # msg_bytes, sender_addr, receiver_addr = gc_message.receive_message_by_txid(txid)
            # if msg_bytes[0] == gc_message.MSG_LFG:
            #     self.set_response(txid)
            #     print(f"Challenged offered: {txid}")
            received_msg = gcl_message.receive_message_by_txid(txid)
            if received_msg.msg_type == gcl_message.MSG_LFG:
                self.set_response_txid(txid)
                print(f"LFG Found: {txid}")
            # return GclMessage(txid, sender_addr, receiver_addr, msg_type, msg_contents)


    def wait_for_challenge(self):
        print("AWAITING RESPONSE")
        return self.await_response(self._filter_tx_for_challenge)


class WtpMonitor(MessageMonitor):

    def __init__(self, gc_monitor, listener_addr, lfg_txid):
        super().__init__(gc_monitor)

        self._listener_addr = listener_addr
        self._lfg_txid = lfg_txid

    def _filter_tx_for_wtp(self, tx):
        if gcl_message.check_if_message_is_for_addr(tx, self._listener_addr):
            txid = tx["txid"]
            wtp_gcl_msg = gcl_message.receive_message_by_txid(txid)
            if wtp_gcl_msg.msg_type == gcl_message.MSG_WTP:
                # check if self._lfg_tx_id matches expected LFG txid
                self.set_response_tx(txid, wtp_gcl_msg)
                print(f"WTP offered: {tx}")

    def wait_for_wtp(self):
        print("AWAITING WTP")
        return self.await_response(self._filter_tx_for_wtp)


class ChallengeResponseMonitor(MessageMonitor):

    def __init__(self, gc_monitor, listener_addr, wtp_tx_id, sender_public_key):
        super().__init__(gc_monitor)

        self._listener_addr = listener_addr
        self._wtp_tx_id = wtp_tx_id
        self._sender_public_key = sender_public_key

    def _filter_tx_for_challenge_response(self, tx):
        if gcl_message.check_if_message_is_for_addr(tx, self._listener_addr):
            txid = tx['txid']
            print(f"Challenge responded: {txid}")

            challenge_gcl_msg = gcl_message.receive_message_by_txid(txid, self._sender_public_key)
            if challenge_gcl_msg.msg_type == gcl_message.MSG_ACC or challenge_gcl_msg.msg.msg_type == gcl_message.MSG_CAN:
                # check if self._wtp_tx_id matches expected WPT txid
                self.set_response_tx(txid, challenge_gcl_msg)
            # if msg_bytes[0] == gc_message.MSG_LFG:
            #     self.set_response(txid)
            #     print(f"Challenged offered: {txid}")

    def wait_for_challenge_reponse(self):
        print("AWAITING CHALLENGE RESPONSE")
        return self.await_response(self._filter_tx_for_challenge_response)


# class ChallengeMonitor:
#
#     def __init__(self, gc_monitor, game_id):
#         self._monitor = gc_monitor
#         self._game_id = game_id
#         self._challenge_tx = None
#         self._keep_monitoring = True
#
#     def _filter_tx_for_challenge(self, tx):
#         print(f"Got it: {tx}")
#         legacy_dest_addr = next(iter(tx['vout'][1].keys()))
#         dest_addr = cashaddress.convert.to_cash_address(legacy_dest_addr)
#
#         if dest_addr == game_shelves.GAMESHELF_ID_TIC_TAC_TOE:
#             self._challenge_tx = tx
#             print(f"Challenged offered: {tx['txid']}")
#
#     async def _monitor_for_challenge(self):
#         while self._keep_monitoring:
#             if self._challenge_tx is not None:
#                 challenge_tx = self._challenge_tx
#                 self._challenge_tx = None
#                 return challenge_tx
#
#             await asyncio.sleep(MONITOR_INTERVAL)
#
#     def wait_for_challenge(self):
#         self._monitor.register_tx_handler(self._filter_tx_for_challenge)
#         loop = asyncio.get_event_loop()
#         challenge_tx = loop.run_until_complete(self._monitor_for_challenge())
#         return challenge_tx