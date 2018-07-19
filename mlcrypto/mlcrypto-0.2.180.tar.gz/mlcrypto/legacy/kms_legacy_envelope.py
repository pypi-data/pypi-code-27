from mlcrypto.kms import Kms
from mlcrypto.legacy.aes_ctc import AesCtc
from mlcrypto.envelope import Envelope


class KmsLegacyEnvelope(Envelope):
    KEY = 'KmsEnvelopeTriple'

    def __init__(self, kms_arn):
        super(KmsLegacyEnvelope, self).__init__(Kms(kms_arn), AesCtc)
