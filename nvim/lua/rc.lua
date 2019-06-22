local keymap = require("keymap")


local options = setmetatable({}, {
    __newindex = function(_, k, v)
        vim.api.nvim_set_option(k, v)
    end,
    __index = function(_, k)
        return vim.api.nvim_get_option(k)
    end
})

local globals = setmetatable({}, {
    __newindex = function(_, k, v)
        vim.api.nvim_set_var(k, v)
    end,
    __index = function(_, k)
        return vim.api.nvim_get_var(k)
    end
})


-- Little helper functions to execute commands from insert mode
local function cmd(command) return "<cmd>"..command.."<CR>" end
local function norm(command) return cmd("normal! "..command) end

--------------------------------------------------------------------
--                     PLUGIN VARIABLES                           --
--------------------------------------------------------------------

-- Add the gai changes bar
globals.gitgutter_sign_added    = '┃'
globals.gitgutter_sign_modified = '┃'
globals.gitgutter_sign_removed  = '┃'

--------------------------------------------------------------------
--                          OPTIONS                               --
--------------------------------------------------------------------

options.t_Co = "256"

--FIXME
--options.shiftwidth      = 4 -- does nothing
--options.number          = "relativenumber" -- wants a boolean
--options.colorscheme     = "elflord" -- rejected
--options.notermguicolors = true -- rejected

-- Get a string from the command prompt.
local function prompt(message)
    return vim.api.nvim_call_function("input", {message})
end

local function echo(message)
    --vim.api.nvim_call_function("echo", {message})
end

--- Bring sanity back to search, no idiotic magic by default
local function search()
    local res = prompt("Search: "):gsub("/", "\\/")

    -- Cancel when the string is empty
    if (not res) or res == "" then return end

    vim.api.nvim_input("<cmd>/\\V"..res.."/<cr><esc>n")
end

--- Search and replace without idotic magic.
-- no more dozen of backslashes per minute...
local function replace()
    local str = prompt("Search: "):gsub("/", "\\/")

    -- Cancel when the string is empty
    if (not str) or str == "" then return end

    local rep = prompt("Replace " ..str.." with: "):gsub("/", "\\/")


    vim.api.nvim_input("<cmd>%s/\\V"..str.."/"..rep.."/gc<cr>")
end

local function save()
    --print("SAVE\n")
    vim.api.nvim_input("<cmd>:w<cr>")
end

local function select_buffer()
    local bufs = vim.api.nvim_list_bufs()
    local path = vim.api.nvim_buf_get_var(1, ":t") or "DD"
    print(path)
    vim.api.nvim_input(":dd "..path)
end

--------------------------------------------------------------------
--                           KEYMAP                               --
--------------------------------------------------------------------

-- Move to the begening of the line
keymap.insert["<C-e>"] = norm("$i") .. "<right><right>"
keymap.normal["<C-e>"] = norm("$i") .. "i<right><right>"

-- map CTRL-A to beginning-of-line (insert mode)
keymap.insert ["<C-a>"] = norm "0i"
keymap.normal ["<C-a>"] = norm "0i"
keymap.command["<C-a>"] = "<Home>"

-- CTRL-U to paste (insert mode)
keymap.insert["<C-u>"] = norm "Pi"
keymap.normal["<C-u>"] = norm "Pi"

-- CTRL+O to save (insert mode)
keymap.insert["<C-o>"] = cmd ":w"
keymap.normal["<C-o>"] = cmd ":w"
keymap.insert["<C-s>"] = cmd ":w"
keymap.normal["<C-s>"] = cmd ":w"

-- CTRL+W to search (insert mode)
keymap.insert["<C-w>"] = search
keymap.normal["<C-w>"] = search
keymap.insert["<C-f>"] = search

-- map CTRL+R to search and replace
keymap.insert["<C-r>"] = replace
keymap.normal["<C-r>"] = replace

--keymap.normal["<C-f>"] = "<esc>/"

-- CTRL+G goto line (insert mode)
keymap.insert["<C-g>"] = "<esc>:"
keymap.normal ["<C-g>"] = "<esc>:"

-- CTRL+X to save and quit (insert mode)
keymap.insert["<C-x>"] = cmd ":confirm quit"
keymap.normal["<C-x>"] = cmd ":confirm quit"

-- map CTRL+K and CTRL+U to act like nano (insert mode)
keymap.insert["<C-k>"] = norm "ddi"
keymap.normal["<C-k>"] = "<esc><S-v>di"

-- CTRL+BackSpace: remove word to the left
keymap.insert["<C-BS>"] = norm "hdvb"
--keymap.insert <C-h> <esc>dvbi
--map <C-h> <esc>dvbi
keymap.normal ["<C-BS>"] = "dvbi"
keymap.command["<C-Bs>"] = "<C-w>"

-- Undo
keymap.insert["<C-z>"] = norm "ui"
keymap.normal["<C-z>"] = norm "ui"

-- Move line up and down
keymap.insert["<C-S-Up>"  ] = cmd ":m -2"
keymap.insert["<C-S-Down>"] = cmd ":m +1"
keymap.normal["<C-S-Up>"  ] = cmd ":m -2"
keymap.normal["<C-S-Down>"] = cmd ":m +1"

-- Indentation
keymap.insert["<Tab>"  ] = norm ">>"
keymap.insert["<S-Tab>"] = norm "<<"
keymap.normal["<Tab>"  ] = ">>"
keymap.normal["<S-Tab>"] = "<<"

-- Select chars when Shift is pressed
keymap.normal["<S-Right>"] = "vl"
keymap.insert["<S-Right>"] = "<esc>vl"
keymap.normal["<S-Up>"   ] = "vk"
keymap.insert["<S-Up>"   ] = "<esc>vk"
keymap.normal["<S-Down>" ] = "vj"
keymap.insert["<S-Down>" ] = "<esc>vj"
keymap.normal["<S-Left>" ] = "vh"
keymap.insert["<S-Left>" ] = "<esc>vj"

-- Shift+Arrow Select the line above and below
keymap.visual["<S-Up>"   ] = "<Up>"
keymap.visual["<S-Down>" ] = "<Down>"
keymap.visual["<S-Left>" ] = "<Left>"
keymap.visual["<S-Right>"] = "<Right>"

-- Ctrl+Alt+Arrow to duplicate the line
keymap.visual["<C-A-Up>"  ] = norm "yyP"
keymap.visual["<C-A-Down>"] = norm "yyp"

-- Backspace to delete selection in visual mode
keymap.visual["<BS>"] = "d"
keymap.normal["<BS>"] = "dh"

-- Select next word
keymap.normal["<C-S-Right>"] = "vw"
keymap.insert["<C-S-Right>"] = "<esc>vw"
keymap.normal["<C-S-Left>" ] = "v<C-Left>"
keymap.insert["<C-S-Left>" ] = "<esc>v<C-Left>"
keymap.visual["<C-S-Left>" ] = "<C-Left>"
keymap.visual["<C-S-Right>"] = "<C-Right>"

-- Easy buffer switch
keymap.normal["<C-T>"  ] = ":bnext<CR>"
keymap.normal["<C-S-T>"] = ":bprev<CR>"
keymap.insert["<C-T>"  ] = norm(":bnext").."i"
keymap.insert["<C-S-T>"] = norm(":bprev") .. "i"

-- Buffer navigation
keymap.insert["<A-Up>"  ] = cmd ":bNext"
keymap.normal["<A-Up>"  ] = cmd ":bNext"
keymap.insert["<A-Down>"] = cmd ":bprevious"
keymap.normal["<A-Down>"] = cmd ":bprevious"

-- Completion
keymap.insert["<C-Space>"] = "<C-p>"
keymap.normal["<C-Space>"] = "<C-p>"

-- Copy (yank)
keymap.insert["<C-c>"] = cmd ":yank"

-- Paste
keymap.insert["<C-v>"] = cmd ":put" --TODO add vMode

-- Remapped Caps_Lock to normal mode, then to buffer select
keymap.insert["<F14>"] = "<esc>"
keymap.normal["<F14>"] = select_buffer

-- Add a color
local function add_highlight(args)
    local param = " "

    for k, v in pairs(args) do
        if k ~= "name" then
            param = param .. k.."="..v.." "
        end
    end

    vim.api.nvim_command("hi "..args.name..param)
end

-- Powerline like mode names
local mode_names = {
    ['n' ] = 'Normal'   ,
    ['no'] = 'Normal·OP',
    ['v' ] = 'Visual'   ,
    ['V' ] = 'V·Line'   ,
    ['^V'] = 'V·Block'  ,
    ['s' ] = 'Select'   ,
    ['S' ] = 'S·Line'   ,
    ['^S'] = 'S·Block'  ,
    ['i' ] = 'Insert'   ,
    ['R' ] = 'Replace'  ,
    ['Rv'] = 'V·Replace',
    ['c' ] = 'Command'  ,
    ['cv'] = 'Vim Ex'   ,
    ['ce'] = 'Ex'       ,
    ['r' ] = 'Prompt'   ,
    ['rm'] = 'More'     ,
    ['r?'] = 'Confirm'  ,
    ['!' ] = 'Shell'    ,
    ['t' ] = 'Terminal' ,
}

globals.currentmode = mode_names

local line_number_color = {
    ['Normal'   ] = {
        LineNr      = {ctermfg = 255, ctermbg = 52 }, PowerColor1 = {ctermfg = 67 , ctermbg = 233},
        PowerColor2 = {ctermfg = 255, ctermbg = 28 }, PowerColor3 = {ctermfg = 255, ctermbg = 52 },
        PowerColor4 = {ctermfg = 255, ctermbg = 28 }, PowerColor5 = {ctermfg = 255, ctermbg = 52 },
    },
    ['Normal·OP'] = {
        LineNr      = {ctermfg = 67 , ctermbg = 233}, PowerColor1 = {ctermfg = 255, ctermbg = 52 },
        PowerColor2 = {ctermfg = 67 , ctermbg = 233}, PowerColor3 = {ctermfg = 255, ctermbg = 52 },
        PowerColor4 = {ctermfg = 255, ctermbg = 28 }, PowerColor5 = {ctermfg = 255, ctermbg = 52 },
    },
    ['Visual'   ] = {
        LineNr      = {ctermfg = 255, ctermbg = 54 }, PowerColor1 = {ctermfg = 255, ctermbg = 54 },
        PowerColor2 = {ctermfg = 16 , ctermbg = 33 }, PowerColor3 = {ctermfg = 255, ctermbg = 52 },
        PowerColor4 = {ctermfg = 255, ctermbg = 28 }, PowerColor5 = {ctermfg = 255, ctermbg = 52 },
    },
    ['V·Line'   ] = {
        LineNr      = {ctermfg = 67 , ctermbg = 233}, PowerColor1 = {ctermfg = 255, ctermbg = 52 },
        PowerColor2 = {ctermfg = 67 , ctermbg = 233}, PowerColor3 = {ctermfg = 255, ctermbg = 52 },
        PowerColor4 = {ctermfg = 255, ctermbg = 28 }, PowerColor5 = {ctermfg = 255, ctermbg = 52 },
    },
    ['V·Block'  ] = {
        LineNr      = {ctermfg = 67 , ctermbg = 233}, PowerColor1 = {ctermfg = 255, ctermbg = 52 },
        PowerColor2 = {ctermfg = 67 , ctermbg = 233}, PowerColor3 = {ctermfg = 255, ctermbg = 52 },
        PowerColor4 = {ctermfg = 255, ctermbg = 28 }, PowerColor5 = {ctermfg = 255, ctermbg = 52 },
    },
    ['Insert'   ] = {
        LineNr      = {ctermfg = 67 , ctermbg = 233}, PowerColor0 = {ctermfg = 67 , ctermbg = 233},
        PowerColor1 = {ctermfg = 16 , ctermbg = 33 }, PowerColor2 = {ctermfg = 255, ctermbg = 201 },
        PowerColor3 = {ctermfg = 255, ctermbg = 28 }, PowerColor4 = {ctermfg = 255, ctermbg = 201 },
    },
}

line_number_color['Select'   ] = line_number_color.Normal
line_number_color['S·Line'   ] = line_number_color.Normal
line_number_color['S·Block'  ] = line_number_color.Normal
line_number_color['Replace'  ] = line_number_color.Normal
line_number_color['V·Replace'] = line_number_color.Normal
line_number_color['Command'  ] = line_number_color.Normal
line_number_color['Vim Ex'   ] = line_number_color.Normal
line_number_color['Ex'       ] = line_number_color.Normal
line_number_color['Prompt'   ] = line_number_color.Normal
line_number_color['More'     ] = line_number_color.Normal
line_number_color['Confirm'  ] = line_number_color.Normal
line_number_color['Shell'    ] = line_number_color.Normal
line_number_color['Terminal' ] = line_number_color.Normal

-- Change the line number bar color and relative_ln depending on the mode
local function update_numbar(mode)
    if not mode then return end

    local theme = line_number_color[mode]

    add_highlight {
        name    = "LineNr",
        ctermfg = theme.LineNr.ctermfg,
        ctermbg = theme.LineNr.ctermbg,
    }

    -- All powerline colors
    for i=0, 4, 2 do
        local idx = math.floor(i/2) + 1

        add_highlight {
            name    = "StatusLine"..(i+1),
            ctermfg = theme["PowerColor"..idx].ctermfg,
            ctermbg = theme["PowerColor"..idx].ctermbg,
        }
        add_highlight {
            name    = "StatusLine"..(i+2),
            ctermfg = theme["PowerColor"..(idx  )].ctermbg,
            ctermbg = theme["PowerColor"..(idx+1)].ctermbg,
        }
    end

    --vim.api.nvim_command("redraw!") --FIXME doesn't work...

    -- Use relative number for everything but insert mode
    options.relativenumber = mode ~= "Insert"
end

add_highlight {
    name    = "User1",
    ctermfg = 241,
    ctermbg = 28,
}

local prev_mode = ""

local function add_color_section(ret, mode, text, color_idx, char)
    local theme = line_number_color[mode]

    local color1 = "%#StatusLine"..(color_idx+1).."#"
    local color2 = "%#StatusLine"..(color_idx).."#"

    if color_idx > 0 then
        ret = ret..color2..char.." "
    end

    ret = ret..color1..text

    return ret, color_idx+2
end

-- Cheap trick to know when the mode changes...
function status_update_callback(mode_raw)
    local mode = mode_names[mode_raw:gmatch("[ ]*([^ ]+)")()] or "Normal"

    if prev_mode ~= mode then
        update_numbar(mode)
        prev_mode = mode
    end

    local ret, color_idx = add_color_section("", mode, " "..mode:upper().." " , 0)

    ret, color_idx = add_color_section(ret, mode, " %f ", color_idx, "⮀")
    ret, color_idx = add_color_section(ret, mode, "d33333", color_idx, "⮀")
    ret, color_idx = add_color_section(ret, mode, "%r %=", color_idx, "⮀")

    ret = ret .. "⮂  sdfsdf"

    color_idx = 0

    ret, color_idx = add_color_section(ret, mode, "  %p%% ", color_idx, "⮂")
    ret, color_idx = add_color_section(ret, mode, " %l : %c ", color_idx, "⮂")
    ret, color_idx = add_color_section(ret, mode, "  NeoVIM %{SearchCount()} ", color_idx, "⮂")

    --assert(false,ret)
    print(ret)

    --print("%#StatusLine1#"..mode:upper().." %#StatusLine2#⮀ %#StatusLine3# %f %#StatusLine4#⮀ %r %=   ☰ ⮂ %p%% ⮂ %l : %c ⮂ NeoVIM ")

    --print("%#StatusLine2# ⮀ "..mode:upper().." %#StatusLine1# ⮀ %f  %#StatusLine3# %r %=   ☰ ⮂ %p%% ⮂ %l : %c ⮂ NeoVIM ")
    return ""
end

options.statusline = "%!StatusUpdateCallback(mode())"

options.showtabline = 2
options.tabline="%#LineNr# %m %= %f"
