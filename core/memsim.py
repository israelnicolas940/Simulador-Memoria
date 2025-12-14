import pathlib
from typing import Text

from rich.style import Style

import cmd2
import argparse
from argparse import ArgumentParser

from core.memory_service import (
    AllocRes,
    ChooseBlockRes,
    FreeIdRes,
    GenericRes,
    InitRes,
    MemoryService,
    StatsRes,
    ShowRes,
)
from core.welcome import welcome

from cmd2 import Color


def build_init_parser() -> ArgumentParser:
    parser = cmd2.Cmd2ArgumentParser()
    parser.add_argument("tamanho", type=int, help="Tamanho do vetor.")
    return parser


def build_alloc_parser() -> ArgumentParser:
    parser = cmd2.Cmd2ArgumentParser(usage="alloc [-h] tamanho {first,best,worst}")
    parser.add_argument("tamanho", type=int, help="Tamanho do bloco.")
    parser.add_argument(
        "alg",
        choices=["first", "best", "worst"],
        help="Algoritmo de alocação.",
    )
    return parser


def build_free_id_parser() -> ArgumentParser:
    parser = cmd2.Cmd2ArgumentParser()
    parser.add_argument("id", type=int, help="Identificador do bloco.")
    return parser


def build_choose_block_parser() -> ArgumentParser:
    parser = cmd2.Cmd2ArgumentParser()
    parser.add_argument("tamanho", type=int, help="Tamanho do bloco.")
    parser.add_argument(
        "alg",
        choices=("first", "best", "worst"),
        help="Algoritmo de alocação.",
    )
    return parser


class MemSim(cmd2.Cmd):
    """Cmd2 application to demonstrate many common features."""

    CUSTOM_CATEGORY = "Simulador de gerência de memória"

    init_parser = build_init_parser()
    alloc_parser = build_alloc_parser()
    choose_block_parser = build_choose_block_parser()
    free_id_parser = build_free_id_parser()

    def __init__(self) -> None:
        """Initialize the cmd2 application."""
        self.service = MemoryService()

        # Startup script that defines a couple aliases for running shell commands
        alias_script = pathlib.Path(__file__).absolute().parent / ".cmd2rc"

        # Create a shortcut for one of our commands
        super().__init__(
            include_py=False,  # Debugging set to true
            startup_script=str(alias_script),
        )

        # Intro banner
        welcome_msg = welcome()
        style = Style(color=cmd2.colors.Color.CYAN, bold=True)

        lines = welcome_msg.split("\n")
        centered_lines = [cmd2.string_utils.align_center(line) for line in lines]
        welcome_centered = "\n".join(centered_lines)
        welcome_stylized = cmd2.string_utils.stylize(welcome_centered, style)

        self.intro = welcome_stylized

        # Show this as the prompt when asking for input
        self.prompt = "memsim > "

        # Used as prompt for multiline commands after the first line
        self.continuation_prompt = "... "

        # Debugging
        # Allow access to your application in py and ipy via self
        # self.self_in_py = True

        # Set the default category name
        self.default_category = "cmd2 Built-in Commands"

        # Color to output text in with echo command
        self.foreground_color = cmd2.colors.Color.CYAN.value

    @cmd2.with_argparser(init_parser)
    @cmd2.with_category(CUSTOM_CATEGORY)
    def do_init(self, args: argparse.Namespace) -> None:
        """Inicializa o vetor que simula a
        memória física e cria o
        primeiro bloco livre."""
        res: InitRes = self.service.init(args.tamanho)
        self._print_result(res)

    @cmd2.with_argparser(alloc_parser)
    @cmd2.with_category(CUSTOM_CATEGORY)
    def do_alloc(self, args: argparse.Namespace) -> None:
        """Executa a alocação de
        memória usando o algoritmo
        selecionado (First Fit, Best Fit
        ou Worst Fit)."""
        res: AllocRes = self.service.alloc(args.tamanho, args.alg)
        self._print_result(res)

    @cmd2.with_argparser(free_id_parser)
    @cmd2.with_category(CUSTOM_CATEGORY)
    def do_free_id(self, args) -> None:
        """Libera um bloco previamente
        alocado com base em seu
        identificador."""
        res: FreeIdRes = self.service.free_id(args.id)
        self._print_result(res)

    @cmd2.with_argparser(choose_block_parser)
    @cmd2.with_category(CUSTOM_CATEGORY)
    def do_choose_block(self, args) -> None:
        """Seleciona o bloco ideal
        conforme o algoritmo de
        alocação definido."""
        res: ChooseBlockRes = self.service.choose_block(args.tamanho, args.alg)
        self._print_result(res)

    @cmd2.with_category(CUSTOM_CATEGORY)
    def do_show(self, _: cmd2.Statement) -> None:
        """Exibe o estado atual da
        memória em duas linhas: uso
        físico (#/.) e identificadores
        de blocos."""
        res: ShowRes = self.service.show()
        self.poutput(self.intro)

    @cmd2.with_category(CUSTOM_CATEGORY)
    def do_stats(self, _: cmd2.Statement) -> None:
        """Calcula e exibe métricas de
        uso, fragmentação interna e
        externa."""
        res: StatsRes = self.service.stats()
        self.poutput(self.intro)

    def _print_result(self, res: GenericRes):
        if res.success:
            self.poutput(res.message)
        else:
            self.perror("Erro: " + res.message)
