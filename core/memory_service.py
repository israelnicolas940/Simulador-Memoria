from dataclasses import dataclass
from typing import Generic, List, Optional, Tuple
from abc import ABC, abstractmethod


@dataclass
class Block:
    """Representa um bloco de memória (alocado ou livre)"""

    start: int
    size: int
    is_free: bool
    block_id: Optional[int] = None  # Usado somente por blocos alocados


class MemoryTable:
    def __init__(self, size: int):
        if size <= 0:
            raise ValueError("Tamanho deve ser positivo")
        self.memsize = size
        self.table = [0] * size  # 0 = livre, >0 = ID do bloco
        self.blocks: List[Block] = [Block(0, size, True)]  # Inicia com um bloco livre
        self.next_id = 1  # Contador para IDs de blocos


@dataclass
class GenericRes:
    success: bool
    message: str


@dataclass
class InitRes(GenericRes):
    pass


@dataclass
class AllocRes(GenericRes):
    block_id: Optional[int] = None


@dataclass
class ChooseBlockRes(GenericRes):
    block: Optional[Block] = None


@dataclass
class FreeIdRes(GenericRes):
    pass


@dataclass
class ShowRes:
    physical_representation: str
    ids: str


@dataclass
class StatsRes:
    total_size: int
    allocated: int
    free: int
    fragmentation_internal: float
    fragmentation_external: int


class Error:
    def __init__(self, message: str):
        self.message = message


class AllocAlgorithm:
    """
    Tenta alocar um bloco na memória.
    """

    @abstractmethod
    def choose_block(self, table: MemoryTable, block_size: int) -> Optional[Block]:
        pass


class FirstFitAlgorithm(AllocAlgorithm):
    def choose_block(self, table: MemoryTable, block_size: int) -> Optional[Block]:
        return None


class BestFitAlgorithm(AllocAlgorithm):
    def choose_block(self, table: MemoryTable, block_size: int) -> Optional[Block]:
        best_block = None
        best_rmng = None

        """Percorre todos os blocos, seleciona o bloco livre que terá menor fragmentação interna"""
        for block in table.blocks:
            if block.is_free and block.size >= block_size:
                remaining = block.size - block_size

                if best_block is None or remaining < best_rmng:
                    best_block = block
                    best_rmng = remaining

        return best_block


class WorstFitAlgorithm(AllocAlgorithm):
    def choose_block(self, table: MemoryTable, block_size: int) -> Optional[Block]:
        return None


class MemoryService:
    def __init__(self):
        self.memory: Optional[MemoryTable] = None

    def init(self, mem_size: int) -> InitRes:
        """Inicializa memória com o respectivo tamanho"""
        try:
            if mem_size <= 0:
                return InitRes(False, "Tamanho deve ser positivo")

            self.memory = MemoryTable(mem_size)
            return InitRes(True, f"Memória inicializada com {mem_size} unidades")
        except Exception as e:
            return InitRes(False, f"Erro ao inicializar: {str(e)}")

    def choose_block(self, block_size: int, alg: str) -> ChooseBlockRes:
        """Encontra o bloco de acordo com o algoritmo"""
        if not self.memory:
            return ChooseBlockRes(False, "Memória não inicializada", None)

        if block_size <= 0:
            return ChooseBlockRes(False, "Tamanho deve ser positivo", None)

        alloc_alg: AllocAlgorithm = self._get_algorithm(alg)
        chosen_block: Optional[Block] = alloc_alg.choose_block(self.memory, block_size)

        if chosen_block:
            return ChooseBlockRes(
                True,
                f"Bloco selecionado ({alg.upper()}): início={chosen_block.start}, tamanho={chosen_block.size}",
                chosen_block,
            )

        return ChooseBlockRes(
            False, f"Nenhum bloco livre com tamanho >= {block_size}", None
        )

    def alloc(self, block_size: int, alg: str) -> AllocRes:
        """Allocate memory using specified algorithm"""
        if not self.memory:
            return AllocRes(False, "Memória não inicializada", None)

        # Encontrar bloco
        result = self.choose_block(block_size, alg)
        if not result.success or not result.block:
            return AllocRes(False, result.message, None)

        chosen_block = result.block
        block_id = self.memory.next_id
        self.memory.next_id += 1

        # Preenche tabela de memória com o id
        for i in range(chosen_block.start, chosen_block.start + block_size):
            self.memory.table[i] = block_id

        # Remove o bloco que foi utilizado
        # Adiciona o bloco ocupado e o espaço livre restante
        block_idx = self.memory.blocks.index(chosen_block)

        self.memory.blocks[block_idx] = Block(
            chosen_block.start, block_size, False, block_id
        )

        # Se sobra espaço no bloco escolhido, insere a "sobra" após o bloco alocado
        if chosen_block.size > block_size:
            leftover = Block(
                chosen_block.start + block_size, chosen_block.size - block_size, True
            )
            self.memory.blocks.insert(block_idx + 1, leftover)

        return AllocRes(
            True,
            f"Bloco {block_id} alocado: {block_size} unidades no endereço {chosen_block.start}",
            block_id,
        )

    def free_id(self, block_id: int) -> FreeIdRes:
        """Libera bloco previamente alocado"""
        if not self.memory:
            return FreeIdRes(False, "Memória não inicializada")

        bid = block_id

        # Encontra bloco com o id
        block_to_free = None
        block_to_free_idx = -1

        for block_idx, block in enumerate(self.memory.blocks):
            if not block.is_free and block.block_id == bid:
                block_to_free = block
                block_to_free_idx = block_idx
                break

        if not block_to_free:
            return FreeIdRes(False, f"Bloco {bid} não encontrado")

        # Limpa tabela de memória
        for i in range(block_to_free.start, block_to_free.start + block_to_free.size):
            self.memory.table[i] = 0

        # Libera bloco alocado
        self.memory.blocks[block_to_free_idx].is_free = True
        self.memory.blocks[block_to_free_idx].block_id = None

        # Housekeeping: mescla blocos adjacentes livres
        self._merge_free_blocks()

        return FreeIdRes(True, f"Bloco {bid} liberado")

    def _merge_free_blocks(self):
        """Mescla blocos adjacentes livres"""
        if not self.memory:
            return

        merged = []
        i = 0
        while i < len(self.memory.blocks):
            current = self.memory.blocks[i]

            if current.is_free:
                # Percorre blocos adjacentes para tetar fazer merge
                while (
                    i + 1 < len(self.memory.blocks)
                    and self.memory.blocks[i + 1].is_free
                ):
                    next_block = self.memory.blocks[i + 1]
                    current = Block(current.start, current.size + next_block.size, True)
                    i += 1

            merged.append(current)
            i += 1

        self.memory.blocks = merged

    def _get_algorithm(self, alg: str) -> AllocAlgorithm:
        match alg.lower():
            case "first":
                return FirstFitAlgorithm()
            case "best":
                return BestFitAlgorithm()
            case "worst":
                return WorstFitAlgorithm()
            case _:
                return FirstFitAlgorithm()

    def show(self) -> ShowRes:
        """Display current memory state"""
        physical = "["
        ids = "["
        for block in self.memory.blocks:
            if(block.is_free):
                physical += "." * block.size
                ids += "." * block.size
            else:
                physical += "#" * block.size
                ids += str(block.block_id) * block.size
        physical += "]"
        ids += "]"

        return ShowRes(physical, ids)

    def stats(self) -> StatsRes:
        """Calcula e mostra estatísticas sobre a memória"""
        print("Blocos ativos:")
        total_external_frag, total_internal_frag, total_free = 0, 0, 0
        for block in self.memory.blocks:
            """Se o bloco estiver livre ele conta como fragmentação externa e como espaço livre"""
            if block.is_free:
                total_external_frag += 1
                total_free += block.size
            else:
                """Caso contrário, percorremos todo ele identificando bytes iguais a 0..."""
                print(f"[id={block.block_id}] @{block.start} +{block.size}B (usado={block.size}) |")
        total_allc = self.memory.memsize - total_free
        return StatsRes(self.memory.memsize, total_allc, total_free, total_internal_frag, total_external_frag)
