# 📄 Documentação do Projeto — Simulador de Gerenciamento de Memória

## 1. Visão Geral

O projeto **Simulador de Gerenciamento de Memória** é um simulador educacional desenvolvido em **Python** com o objetivo de representar o funcionamento básico de um gerenciador de memória dinâmica. Ele permite experimentar diferentes algoritmos clássicos de alocação de memória e observar seus impactos sobre o uso do espaço, fragmentação e liberação de blocos.

O simulador opera por meio de uma **interface de linha de comando (CLI)**, onde o usuário pode inicializar a memória, alocar e liberar blocos, visualizar o estado atual da memória e obter estatísticas.

---

## 2. Objetivos do Projeto

* Simular o gerenciamento de memória dinâmica.
* Implementar e comparar algoritmos clássicos de alocação.
* Demonstrar conceitos como fragmentação interna e externa.
* Facilitar o aprendizado de sistemas operacionais por meio de experimentação prática.

---

## 3. Funcionalidades Principais

* Inicialização da memória com tamanho definido pelo usuário.
* Alocação de blocos de memória utilizando:

  * **First Fit**
  * **Best Fit**
  * **Worst Fit**
* Liberação de blocos por identificador único (ID).
* Coalescência automática de blocos livres adjacentes.
* Visualização do estado atual da memória.
* Exibição de estatísticas de uso e fragmentação.

---

## 4. Estrutura Geral do Projeto

O projeto é organizado de forma modular, separando a interface do usuário da lógica principal do simulador:

* **main.py**

  * Ponto de entrada da aplicação.
  * Responsável por interpretar comandos do usuário.
  * Atua como controlador da aplicação.

* **core/**

  * Contém a lógica de gerenciamento de memória.
  * Implementa as estruturas de dados e algoritmos de alocação.

Essa separação melhora a legibilidade, manutenção e extensibilidade do código.

---

## 5. Estruturas de Dados Utilizadas

### 5.1 Estrutura de Bloco de Memória

Cada bloco de memória (livre ou alocado) é representado por uma estrutura que contém informações essenciais para controle e gerenciamento.

Campos típicos de um bloco:

* **id**: identificador único do bloco.
* **start**: posição inicial do bloco na memória.
* **size**: tamanho do bloco (em unidades de memória).
* **allocated**: indica se o bloco está alocado ou livre.

Exemplo conceitual:

```python
class Block:
    def __init__(self, id, start, size, allocated):
        self.id = id
        self.start = start
        self.size = size
        self.allocated = allocated
```

Essa estrutura permite:

* Identificação precisa de blocos para liberação.
* Cálculo de fragmentação.
* Coalescência de blocos livres adjacentes.

---

### 5.2 Estrutura da Memória

A memória simulada é representada como uma **lista ordenada de blocos**, mantendo a ordem física dos endereços.

Essa escolha permite:

* Percorrer a memória de forma sequencial.
* Identificar blocos adjacentes.
* Implementar facilmente os algoritmos de alocação.

---

## 6. Algoritmos de Alocação

### 6.1 First Fit

Seleciona o **primeiro bloco livre** que possui tamanho suficiente para a alocação solicitada.

**Vantagens**:

* Simplicidade
* Menor tempo de busca

**Desvantagens**:

* Pode gerar fragmentação externa.

---

### 6.2 Best Fit

Seleciona o **menor bloco livre** que seja capaz de atender à solicitação.

**Vantagens**:

* Reduz desperdício imediato de espaço.

**Desvantagens**:

* Pode gerar muitos blocos pequenos inutilizáveis.

---

### 6.3 Worst Fit

Seleciona o **maior bloco livre disponível**.

**Vantagens**:

* Evita criação de blocos muito pequenos.

**Desvantagens**:

* Pode desperdiçar grandes áreas de memória.

---

## 7. Liberação de Memória e Coalescência

Ao liberar um bloco por meio do comando `free_id`, o simulador:

1. Marca o bloco como livre.
2. Verifica se blocos adjacentes também estão livres.
3. Realiza a **coalescência**, unificando blocos livres contíguos em um único bloco maior.

Essa decisão reduz a fragmentação externa e melhora futuras alocações.

---

## 8. Decisões de Implementação

### 8.1 Uso de Identificadores Únicos (ID)

Cada bloco alocado recebe um **ID incremental**, permitindo:

* Liberação direta do bloco correto.
* Visualização clara no estado da memória.
* Controle simples de alocações.

---

### 8.2 Interface de Linha de Comando (CLI)

A escolha por uma CLI foi motivada por:

* Simplicidade de implementação.
* Foco educacional.
* Facilidade de testes manuais.

Os comandos são interpretados em tempo de execução e mapeados para operações internas do simulador.

---

### 8.3 Separação de Responsabilidades

O projeto segue o princípio de **Separation of Concerns**, separando:

* Interface (CLI)
* Lógica de negócio (gerenciamento de memória)

Isso facilita manutenção e futuras extensões.

---

## 9. Padrões de Projeto

### Strategy (implícito)

Os algoritmos de alocação funcionam como estratégias que podem ser escolhidas dinamicamente pelo usuário.

### MVC Simplificado

* **Model**: blocos de memória e lista de memória.
* **Controller**: interpretação dos comandos.
* **View**: saída textual no terminal.

---

## 10. Considerações Finais

O Simulador de Gerenciamento de Memória é um projeto didático bem estruturado que demonstra, de forma prática, conceitos fundamentais de sistemas operacionais. A utilização de estruturas simples, como listas de blocos com identificadores e tamanhos bem definidos, torna o simulador claro, extensível e adequado para fins educacionais.

---

## 11. Possíveis Extensões

* Implementação de novos algoritmos (Buddy System, Slab).
* Simulação de memória virtual e paginação.
* Interface gráfica.
* Coleta automática de métricas comparativas entre algoritmos.
