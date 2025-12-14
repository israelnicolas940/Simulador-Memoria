# MemSim - Simulador de Gerenciamento de Memória

Um simulador interativo de gerenciamento de memória dinâmica que implementa os algoritmos clássicos de alocação: First Fit, Best Fit e Worst Fit.

## Descrição

MemSim é uma ferramenta educacional desenvolvida em Python que simula o comportamento de um gerenciador de memória. O simulador permite visualizar como diferentes algoritmos de alocação funcionam, além de analisar métricas como fragmentação interna e externa.

## Funcionalidades

- **Três algoritmos de alocação**:
  - First Fit (primeiro bloco que se encaixa)
  - Best Fit (menor bloco que se encaixa)
  - Worst Fit (maior bloco que se encaixa)
  
- **Operações suportadas**:
  - Inicialização de memória
  - Alocação de blocos
  - Liberação de blocos
  - Visualização do estado da memória
  - Estatísticas de uso e fragmentação

- **Interface interativa** via linha de comando (CLI)
- **Coalescência automática** de blocos livres adjacentes
- **Visualização gráfica** do estado da memória

## Instalação

### Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. Clone o repositório:
```bash
git clone <seu-repositorio>
cd Simulador-Memoria
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 💻 Uso

### Iniciando o simulador

```bash
python main.py
```

Você verá o prompt interativo:
```
memsim > 
```

### Comandos disponíveis

#### 1. Inicializar memória
```bash
memsim > init 50
```
Inicializa a memória com 50 unidades.

#### 2. Alocar memória
```bash
memsim > alloc 10 first
memsim > alloc 15 best
memsim > alloc 8 worst
```
Aloca blocos de memória usando o algoritmo especificado:
- `first`: First Fit
- `best`: Best Fit
- `worst`: Worst Fit

#### 3. Visualizar estado da memória
```bash
memsim > show
```
Exibe duas linhas:
- **Físico**: `#` indica espaço ocupado, `.` indica espaço livre
- **IDs**: Mostra o identificador de cada bloco alocado

Exemplo de saída:
```
============================================================
ESTADO DA MEMÓRIA
============================================================
Físico: ##########.....###############........##########..
IDs:    1111111111.....222222222222222........3333333333..
============================================================
```

#### 4. Liberar memória
```bash
memsim > free_id 2
```
Libera o bloco com ID 2 e realiza coalescência com blocos livres adjacentes.

#### 5. Exibir estatísticas
```bash
memsim > stats
```
Mostra métricas detalhadas:
- Tamanho total da memória
- Memória alocada e livre
- Percentuais de uso
- Fragmentação interna e externa

Exemplo de saída:
```
============================================================
ESTATÍSTICAS DE MEMÓRIA
============================================================
Tamanho total:              50 unidades
Memória alocada:            35 unidades (70.0%)
Memória livre:              15 unidades (30.0%)
Fragmentação interna:       0.0%
Fragmentação externa:       3 blocos livres
============================================================
```

#### 6. Escolher bloco (debug/análise)
```bash
memsim > choose_block 10 best
```
Mostra qual bloco seria escolhido pelo algoritmo sem realizar a alocação.

#### 7. Ajuda
```bash
memsim > help
memsim > help alloc
```
Exibe ajuda geral ou específica de um comando.

#### 8. Sair
```bash
memsim > quit
```
ou pressione `Ctrl+D` (Linux/Mac) ou `Ctrl+Z` (Windows)

## Exemplo de sessão completa

```bash
$ python main.py

memsim > init 40
Memória inicializada com 40 unidades

memsim > alloc 10 first
Bloco 1 alocado: 10 unidades no endereço 0

memsim > alloc 5 best
Bloco 2 alocado: 5 unidades no endereço 10

memsim > alloc 8 worst
Bloco 3 alocado: 8 unidades no endereço 15

memsim > show
============================================================
ESTADO DA MEMÓRIA
============================================================
Físico: #######################.................
IDs:    1111111111222223333333.................
============================================================

memsim > free_id 2
Bloco 2 liberado

memsim > show
============================================================
ESTADO DA MEMÓRIA
============================================================
Físico: ##########.....########.................
IDs:    1111111111.....33333333.................
============================================================

memsim > stats
============================================================
ESTATÍSTICAS DE MEMÓRIA
============================================================
Tamanho total:              40 unidades
Memória alocada:            18 unidades (45.0%)
Memória livre:              22 unidades (55.0%)
Fragmentação interna:       0.0%
Fragmentação externa:       2 blocos livres
============================================================

memsim > quit
```

## Estrutura do projeto

```
memsim/
├── main.py                 # Ponto de entrada da aplicação
├── core/
│   ├── memsim.py          # Interface CLI (cmd2)
│   ├── memory_service.py  # Lógica de gerenciamento de memória
│   └── welcome.py         # Mensagem de boas-vindas
├── requirements.txt       # Dependências do projeto
└── README.md             # Este arquivo
```

## Conceitos implementados

### Algoritmos de alocação

1. **First Fit**: Percorre a lista de blocos livres e aloca no primeiro que couber. Rápido, mas pode causar fragmentação no início da memória.

2. **Best Fit**: Procura o menor bloco livre que seja suficiente. Minimiza desperdício, mas pode deixar pequenos fragmentos inutilizáveis.

3. **Worst Fit**: Aloca no maior bloco livre disponível. Tenta evitar fragmentos muito pequenos.

### Coalescência (Coalescing)

Quando um bloco é liberado, o simulador automaticamente mescla blocos livres adjacentes, reduzindo a fragmentação externa.

### Fragmentação

- **Fragmentação Interna**: Espaço desperdiçado dentro de um bloco alocado (nesta implementação = 0%)
- **Fragmentação Externa**: Número de blocos livres separados que não podem ser utilizados por alocações maiores

## Tecnologias utilizadas

- **Python 3.10+**
- **cmd2**: Framework para interfaces de linha de comando
- **click**: Biblioteca para criação de CLIs
- **rich**: Formatação e estilização de texto no terminal

---

Desenvolvido como ferramenta educacional para o estudo de Sistemas Operacionais 
