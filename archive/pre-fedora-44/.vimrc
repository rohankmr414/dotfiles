" ================================
" Welcome to Rohan's vimrc file
" ================================

" --------------------------------
" Plugins
" --------------------------------
set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'

" Plugins
Plugin 'tpope/vim-fugitive'
Plugin 'tpope/vim-surround'
Plugin 'tpope/vim-commentary' " gc to comment out
Plugin 'pangloss/vim-javascript'
Plugin 'ctrlpvim/ctrlp.vim'
let g:ctrlp_working_path_mode = 0 " make ctrlp work from current dir
Plugin 'vim-airline/vim-airline'
Plugin 'vim-airline/vim-airline-themes'
Plugin 'luochen1990/rainbow'
Plugin 'scrooloose/nerdtree'
Plugin 'kana/vim-textobj-user'
Plugin 'kana/vim-textobj-line'
Plugin 'kana/vim-textobj-entire'
Plugin 'vim-scripts/vim-auto-save'
Plugin 'szw/vim-g'
Plugin 'jiangmiao/auto-pairs'
Plugin 'fatih/vim-go' " golang development 
Plugin 'jamesroutley/vim-logbook'
Plugin 'sheerun/vim-polyglot'   " syntax highlighting in most languages
"Plugin 'joshdick/onedark.vim'   " Atom-style dark theme
"Plugin 'Valloric/YouCompleteMe'

" All of your Plugins must be added before the following line
call vundle#end()
filetype plugin indent on

" --------------------------------
" Pretty things
" --------------------------------
syntax on
"colorscheme onedark

" Set Airline bar theme
let g:airline_theme='bubblegum'

"rainbow Plugin Options (luochen1990/rainbow)
let g:rainbow_active = 1    " 0 if you want to enable it later via :RainbowToggle


" Enabling autosave
let g:auto_save = 1
imap <Tab> <C-P>
" --------------------------------
" Basic stuff
" --------------------------------
let g:mapleader = " " " Set leader to spacebar 
set spelllang=en_gb
set backspace=indent,eol,start " Bring backspace to life
set number          " Line numberswq
set hlsearch        " Highlight whole word when searching
set ignorecase      " Ignore case when searching...
set smartcase       " ...except when serach query contains a capital letter
set autoread        " Auto load files if they change on disc
map <Leader>p :set paste<CR><esc>"*]p:set nopaste<cr>
map <Leader>y "*y  )
map <Leader><Leader> :w<CR>
inoremap jj <ESC>:w<CR>
let g:go_version_warning = 0
     
" Pasting - indent last pasted
nnoremap gz '[='] 

" Disable highlight when <leader><cr> is pressed
map <silent> <leader><ESC> :noh<cr>

"Cursor
if exists('$TMUX')
  let &t_SI = "\<Esc>Ptmux;\<Esc>\<Esc>]50;CursorShape=1\x7\<Esc>\\"
  let &t_EI = "\<Esc>Ptmux;\<Esc>\<Esc>]50;CursorShape=0\x7\<Esc>\\"
else
  let &t_SI = "\<Esc>]50;CursorShape=1\x7"
  let &t_EI = "\<Esc>]50;CursorShape=0\x7"
endif

" Open current file in a new vertical split with '='
nnoremap = :vsplit<cr>

" Easy split navigation
map <C-j> <C-w>j
map <C-k> <C-W>k
map <C-h> <C-W>h
map <C-l> <C-W>l

" Simplify using tabs
nnoremap <C-Left> gT
nnoremap <C-Right> gt
nnoremap T :tabnew<cr>

" Open new splits to right and bottom 
set splitbelow
set splitright

"Tab completion
set wildmenu
set wildmode=list:longest,list:full
function! InsertTabWrapper()
  let col = col('.') - 1
  if !col || getline('.')[col - 1] !~ '\k'
    return "\<tab>"
  else
    return "\<c-p>"
  endif
    endfunction
inoremap <Tab> <c-r>=InsertTabWrapper()<cr>
inoremap <S-Tab> <c-n>

" Tab size
set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab

" Disable swap files
set noswapfile


" Vim's default autocomplete
set complete=.,b,u,]

" Nerdtree Toggle
map <C-n> :NERDTreeToggle<CR>
