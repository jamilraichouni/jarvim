import sys
from pathlib import Path

import pynvim


@pynvim.plugin
class JarVim(object):

    def __init__(self, nvim):
        self.nvim = nvim

    # @pynvim.function("JarFunction", sync=True)
    # def jarfunction(self, args):
    #     return 3

    @pynvim.command("JarCommand", nargs="*", range="")
    def jarcommand(self, args, range):
        # self.nvim.current.line = f"Command with args: {args}, range: {range}"
        MODULE_DIR: Path = Path(__file__).parents[0]
        self.nvim.out_write(f"MODULE_DIR: {MODULE_DIR}\n")
        sys.path.insert(0, str(MODULE_DIR / "jarvim"))
        from jarlsp import JarLsp

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
    def on_dir_changed(self):
        self.nvim.out_write("DirChanged, yeah!\n")

    @pynvim.autocmd("VimEnter", pattern="*", eval="", sync=False)
    def on_vimenter(self):
        MODULE_DIR: Path = Path(__file__).parents[0]
        self.nvim.out_write(f"MODULE_DIR: {MODULE_DIR}\n")
        sys.path.insert(0, str(MODULE_DIR / "jarvim"))

        from jarlsp import JarLsp
        from log import logger
        logger.add(Path(self.nvim.funcs.stdpath("data")) / "jarvim.log", level="DEBUG")
        logger.info("JarVim plugin has been activated.")
        [logger.info(p) for p in sorted(sys.path)]
        self.jarlsp = JarLsp(self.nvim)
