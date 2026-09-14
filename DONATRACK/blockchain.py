from datetime import datetime
import hashlib


class Block:

    def __init__(self, index, data, previous_hash=''):
        self.index = index
        self.date = str(datetime.now())
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.create_hash()

    def create_hash(self):
        texto = f"{self.index}{self.date}{self.data}{self.previous_hash}{self.nonce}"

        return hashlib.sha256(
            texto.encode()
        ).hexdigest()

    def mine(self, difficulty):

        while not self.hash.startswith(difficulty):
            self.nonce += 1
            self.hash = self.create_hash()


class BlockChain:

    def __init__(self, genesis, difficulty='00'):

        self.difficulty = difficulty

        bloque = Block(
            0,
            genesis
        )

        bloque.mine(
            self.difficulty
        )

        self.chain = [bloque]

    def add_block(self, data):

        anterior = self.chain[-1]

        bloque = Block(
            anterior.index + 1,
            data,
            anterior.hash
        )

        bloque.mine(
            self.difficulty
        )

        self.chain.append(
            bloque
        )

    def update_block(self, index, data):

        for bloque in self.chain:

            if bloque.index == index:

                # Se modifica el dato,
                # pero NO se recalcula el hash.
                bloque.data = data

                return

    def is_valid(self):

        for i, bloque in enumerate(self.chain):

            # Verificar que el hash corresponda
            # con los datos actuales
            if bloque.hash != bloque.create_hash():

                return False, i, "DATOS ALTERADOS"

            # Verificar conexión con el bloque anterior
            if i > 0:

                if bloque.previous_hash != self.chain[i - 1].hash:

                    return False, i, "ENLACE ALTERADO"

        return True, None, None