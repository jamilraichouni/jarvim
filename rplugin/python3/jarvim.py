"""Neovim plugin JarVim."""
import sys
from pathlib import Path

import pynvim


@pynvim.plugin
class JarVim(object):
    """Plugin class."""

    def __init__(self, nvim):
        self.nvim = nvim

    # @pynvim.function("JarFunction", sync=True)
    # def jarfunction(self, args):
    #     return 3

    @pynvim.command("JARTest", nargs="*", range="")
    def test_command(self, args, range):
        self.nvim.out_write(f"Test args: {args}\n")

    @pynvim.command("JARNewProject", nargs="*", range="")
    def new_project(self, args, range):
        self.nvim.out_write(f"args: {args}\n")
        # MODULE_DIR: Path = Path(__file__).parents[0]
        # self.nvim.out_write(f"MODULE_DIR: {MODULE_DIR}\n")
        # sys.path.insert(0, str(MODULE_DIR / "jarvim"))
        # from jarlsp import JarLsp

    # @pynvim.autocmd("BufEnter", pattern="*.py", eval="expand('<afile>')", sync=False)
    # def on_bufenter(self, filename):
    #     pass
    #     self._setup_pylsp()

    # self.nvim.request(
    #     "nvim_set_keymap",
    #     "n", "<space>q", "<cmd>lua vim.diagnostic.setloclist()<CR>",
    #     {"noremap": True, "silent": True}
    # )
    @pynvim.autocmd("DirChanged", pattern="*", eval="", sync=False)
    def _on_dir_changed(self):
        cwd = self.nvim.call("getcwd")
        msg = f"DirChanged to {cwd}"
        # self.nvim.out_write(msg)
        self.logger.info(msg)
        # self.reload_debug_configuration()

    @pynvim.autocmd("VimEnter", pattern="*", eval="", sync=False)
    def on_vimenter(self):
        MODULE_DIR: Path = Path(__file__).parents[0]
        sys.path.insert(0, str(MODULE_DIR / "jarvim"))

        # from jarlsp import JarLsp
        from log import logger

        self.logger = logger

        self.logger.add(
            Path(self.nvim.funcs.stdpath("data")) / "jarvim.log", level="DEBUG"
        )
        self.logger.info("JarVim plugin has been activated.")
        # self.jarlsp = JarLsp(self.nvim)

    @pynvim.command("JARReloadDebugConfiguration")
    def reload_debug_configuration(self):
        cwd: Path = Path(self.nvim.call("getcwd"))
        debug_cfg_file_path: Path = cwd / ".jarvim/debug.json"
        if not debug_cfg_file_path.is_file():
            return
        # self.nvim.out_write(
        #     f"Reload debug configuration from '{debug_cfg_file_path}'..."
        # )
        self.nvim.exec_lua("require('dap').configurations.python = {}")
        self.nvim.exec_lua("dap_ext_vscode = require('dap.ext.vscode')")
        self.nvim.lua.dap_ext_vscode.load_launchjs(str(debug_cfg_file_path))
