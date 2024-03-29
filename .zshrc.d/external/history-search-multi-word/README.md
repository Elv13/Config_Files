# Introduction

Binds `Ctrl-R` to a widget that searches for multiple keywords in `AND` fashion.
In other words, you can enter multiple words, and history entries that match
all of them will be found. The entries are syntax highlighted.

Video – view on [asciinema](https://asciinema.org/a/88954). You can resize the video by pressing `Ctrl-+` or `Cmd-+`.

[![asciicast](https://asciinema.org/a/88954.png)](https://asciinema.org/a/88954)

HSMW is **FAST** – highlighting 20 concurrent complex history entries does not cause real slow down:

[![asciicast](https://asciinema.org/a/89406.png)](https://asciinema.org/a/89406)

# News

* 12-11-2016
  - HSMW can now show context of selected history entry! Just hit `Ctrl-K`, [video](https://asciinema.org/a/92516)
  - More performance optimizations

* 31-10-2016
  - Newlines do not disturb the parser anymore, and are also highlighted with a dark color – [video](https://asciinema.org/a/91159)

* 27-10-2016
  - New optimizations – **30%** speed up of syntax highlighting!
  - Architectural change – syntax highlighting is now computed rarely, so any possible performance problems are now solved, in advance!

* 24-10-2016
  - Workaround for Zsh versions like 5.0.2 has been added – **Ctrl-V** and **ESC** cancel search. On such Zsh
    versions Ctrl-C might not work. Fully problem-free Zsh version will be the upcoming 5.3, where
    I have together with Zsh Hackers fully fixed the Ctrl-C issue.

* 22-10-2016
  - Search process has been optimized by 20%! History sizes like 100000 are now supported.
  - Active history entry can be `underline`, `standout` (i.e. inverse video), `bold`, `bg=blue`, etc. with
    the new Zstyle `:plugin:history-search-multi-word / active` (see Zstyles section) – [video](https://asciinema.org/a/90214).

* 16-10-2016
  - More optimizations of syntax highlighting (40% in total for the two days) – new video above.

* 15-10-2016
  - The compact, already optimized (by me) [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting) part has been further optimized by 21%!
    Also, more tokens are highlighted – variable expressions like `"${(@)var[1,3]}"` (when quoted).

* 11-10-2016
  - Syntax highlighting of history – adapted, fine crafted, **small** part of [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting)
    to color what `hsmw` shows:

    ![syntax highlighting](http://imagizer.imageshack.us/a/img921/1503/bMAF59.gif)

* 20-09-2016
  - Keys Page Up and Page Down work and page-wise move along history. Also, `Ctrl-P`, `Ctrl-N`
    move to previous and next entries.

* 19-09-2016
  - Better immunity to [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions)
    and [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting) – home,
    end, left and right cursor keys now work smoothly.

* 25-05-2016
  - Cooperation with
    [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions)
    plugin
  - Configuration option to set page size, example use:

    ```zsh
    zstyle ":history-search-multi-word" page-size "5"
    ```

# Installation

**The plugin is "standalone"**, which means that only sourcing it is needed. So to
install, unpack `history-search-multi-word` somewhere and add

```zsh
source {where-hsmw-is}/history-search-multi-word.plugin.zsh
```

to `zshrc`.

If using a plugin manager, then `Zplugin` is recommended, but you can use any
other too, and also install with `Oh My Zsh` (by copying directory to
`~/.oh-my-zsh/custom/plugins`).


### [Zplugin](https://github.com/psprint/zplugin)

Add `zplugin load psprint/history-search-multi-word` to your `.zshrc` file.
Zplugin will handle cloning the plugin for you automatically the next time you
start zsh.

### Antigen

Add `antigen bundle psprint/history-search-multi-word` to your `.zshrc` file.
Antigen will handle cloning the plugin for you automatically the next time you
start zsh. You can also add the plugin to a running zsh with `antigen bundle
psprint/history-search-multi-word` for testing before adding it to your
`.zshrc`.

### Oh-My-Zsh

1. `cd ~/.oh-my-zsh/custom/plugins`
2. `git clone git@github.com:psprint/history-search-multi-word.git`
3. Add `history-search-multi-word` to your plugin list

### Zgen

Add `zgen load psprint/history-search-multi-word` to your .zshrc file in the same
place you're doing your other `zgen load` calls in.

# Customizing

## Zstyles

```zsh
zstyle ":history-search-multi-word" page-size "8"                      # Number of entries to show (default is $LINES/3)
zstyle ":history-search-multi-word" highlight-color "fg=yellow,bold"   # Color in which to highlight matched, searched text (default bg=17 on 256-color terminals)
zstyle ":plugin:history-search-multi-word" synhl "yes"                 # Whether to perform syntax highlighting (default true)
zstyle ":plugin:history-search-multi-word" active "underline"          # Effect on active history entry. Try: standout, bold, bg=blue (default underline)
zstyle ":plugin:history-search-multi-word" check-paths "yes"           # Whether to check paths for existence and mark with magenta (default true)
```

## Syntax highlighting

Syntax highlighting is customized via `HSMW_HIGHLIGHT_STYLES` associative array.
It has keys like `reserved-word`, `alias`, `command`, `path`, which are assigned
with strings like `fg=blue,bold`, to configure how given elements are to be
colored. If you assign this array before loading `hsmw` you will change the defaults. Complete list
of available keys is [at the beginning](https://github.com/psprint/history-search-multi-word/blob/master/hsmw-highlight#L34-L62)
of `hsmw-highlight` file. Example `~/.zshrc` addition that sets `path` key –
paths that exist will be highlighted with background magenta, foreground white, bold:

```zsh
typeset -gA HSMW_HIGHLIGHT_STYLES
HSMW_HIGHLIGHT_STYLES[path]="bg=magenta,fg=white,bold"
```

Following code will enable coloring of options of form "-o" and "--option", with cyan:

```zsh
typeset -gA HSMW_HIGHLIGHT_STYLES
HSMW_HIGHLIGHT_STYLES[single-hyphen-option]="fg=cyan"
HSMW_HIGHLIGHT_STYLES[double-hyphen-option]="fg=cyan"
```

Following code will use 256 colors to highlight command separators (like ";" or "&&"):

```zsh
HSMW_HIGHLIGHT_STYLES[commandseparator]="fg=241,bg=17"
```

# IRC Channel

Channel `#zplugin@freenode` is a support place for all author's projects. Connect to:
[chat.freenode.net:6697](ircs://chat.freenode.net:6697/%23zplugin) (SSL) or [chat.freenode.net:6667](irc://chat.freenode.net:6667/%23zplugin)
 and join #zplugin.

Following is a quick access via Webchat [![IRC](https://kiwiirc.com/buttons/chat.freenode.net/zplugin.png)](https://kiwiirc.com/client/chat.freenode.net:+6697/#zplugin)
