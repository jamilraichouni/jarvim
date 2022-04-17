from pynvim.api.common import NvimError

from log import logger

class JarLsp:

    is_setup = False
 
    def __init__(self, nvim):
        self.nvim = nvim
        self.setup()
    
    def setup(self):
        try:
            self.nvim.exec_lua("lspconfig = require('lspconfig')")
            logger.info("Plugin nvim-lspconfig is installed.")
        except NvimError:
            logger.info("Plugin nvim-lspconfig is not installed.")
            return
        icons = {"Error": " ", "Warning": " ", "Information": " ", "Hint": " "}
        for type_, icon in icons.items():
            hl = f"LspDiagnosticsSign{type_}"
            logger.info("Call sign_define")
            self.nvim.funcs.sign_define(hl, {"text": icon, "texthl": hl, "numhl": ""})
        
        self.nvim.exec_lua("""
vim.lsp.handlers["textDocument/publishDiagnostics"] = vim.lsp.with(
  vim.lsp.diagnostic.on_publish_diagnostics,
  {signs = true}
)

vim.lsp.handlers["textDocument/hover"] = vim.lsp.with(
  vim.lsp.handlers.hover,
  {border = "single"}
)

vim.lsp.handlers["textDocument/signatureHelp"] = vim.lsp.with(
  vim.lsp.handlers.signature_help,
  {border = "single"}
)

local lspconfig = require('lspconfig')
local function on_attach(client, bufnr)
  local function buf_set_keymap(...) vim.api.nvim_buf_set_keymap(bufnr, ...) end
  local function buf_set_option(...) vim.api.nvim_buf_set_option(bufnr, ...) end

  -- Mappings.
  local opts = {noremap=true, silent=true}

  local cap = client.resolved_capabilities
  if cap.completion then
    buf_set_option('omnifunc', 'v:lua.vim.lsp.omnifunc')
    buf_set_keymap('i', '<C-N>', '<C-X><C-O>', opts)
  end

  -- Set some keybinds conditional on server capabilities
  if cap.hover then
    buf_set_keymap('n', 'K', '<CMD>lua vim.lsp.buf.hover()<CR>', opts)
  end
  if cap.declaration then
    buf_set_keymap('n', 'gD', '<CMD>lua vim.lsp.buf.declaration()<CR>', opts)
  end
  if cap.goto_definition then
    buf_set_keymap('n', 'gd', '<CMD>lua vim.lsp.buf.definition()<CR>', opts)
  end

  -- Set autocommands conditional on server_capabilities
  if cap.document_formatting then
    vim.api.nvim_exec([[
      augroup lsp_document_formatting
        autocmd!
        autocmd BufWritePre <buffer> lua vim.lsp.buf.formatting_sync(nil, 1000)
      augroup END
    ]], false)
  end

  if cap.document_highlight then
    vim.api.nvim_exec([[
      augroup lsp_document_highlight
        autocmd!
        autocmd CursorHold <buffer> lua vim.lsp.buf.document_highlight()
        autocmd CursorMoved <buffer> lua vim.lsp.buf.clear_references()
      augroup END
    ]], false)
  end
end

lspconfig.util.default_config.on_attach = on_attach
        """)

        # logger.info("Setup language server 'pyright'...")
        # self.nvim.lua.lspconfig.pyright.setup({})
        
        logger.info("Setup language server 'pylsp'...")
        self.nvim.lua.lspconfig.pylsp.setup({
            "cmd": ["pylsp"],
            "plugins": {
                "flake8": {
                    "enabled": "",
                    "enabled": True
                },
                "jedi_completion": {
                    "enabled": True
                },
                "jedi_definition": {
                    "enabled": True
                }
            }
        })

