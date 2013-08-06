clear
source /etc/issue
# The following lines were added by compinstall

PATH=/home/kde-devel/kde/bin:/usr/local/lib/cw:/usr/lib64/perl5/site_perl/5.12.1/auto/share/dist/Cope:/sbin:/usr/sbin:/usr/local/bin:/usr/bin:/bin:/opt/bin:/usr/x86_64-pc-linux-gnu/gcc-bin/4.4.4:/opt/blackdown-jdk-1.4.2.03/bin:/opt/blackdown-jdk-1.4.2.03/jre/bin:/usr/games/bin:/home/kde-devel/kde/bin
XDG_DATA_DIRS=$XDG_DATA_DIRS:/home/kde-devel/kde/share/akonadi/agents 


export HISTSIZE=2000
export HISTFILE="$HOME/.zhistory"
export SAVEHIST=$HISTSIZE

setopt histignoredups
setopt histignorespace
setopt hist_ignore_all_dups
setopt autocd
#setopt correctall
setopt no_case_glob
setopt noequals

alias ls='ls --color=auto -F'
alias ll='ls++'
alias la='ls -lah --color=auto -F'
alias tarc="tar -cjvf "
alias tarx="tax -xpvf "
alias nn="nano -w "
alias n="nano -w "
alias grepkey="xev | grep -A2 --line-buffered '^KeyRelease' | sed -n '/keycode /s/^.*keycode \([0-9]*\).* (.*, \(.*\)).*$/\1 \2/p'"
alias xrags=xargs
alias greo=grep
alias xephyr="Xephyr :1 -screen 1680x996"
alias kdb="sudo killall -9 updatedb"
alias xdg-edit="nano ~/.local/share/applications/mimeapps.list"
alias bell="echo '\a'"
function fawe {; find ~/.config/awesome/ -iname '*.lua' | xargs grep $1 --color;}

#Make ctrl+left/right and ^W work as in any other apps in the universe
zle -N backward-kill-word-bash backward-kill-word-match
zstyle ':zle:backward-kill-word-bash' word-style whitespace
zstyle ':completion:*' matcher-list '' 'm:{a-z}={A-Z}'
bindkey '^Q' quoted-insert '^U' vi-kill-line '^W' backward-kill-word-bash
autoload -U select-word-style
select-word-style bash

bindkey '^P' push-input

source ~/.zshrc.d/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh

eval $( dircolors -b $HOME/.LS_COLORS )
ZLS_COLORS="$LS_COLORS"

function svgz2svg {
  for FILE in "$1";do 
    cp $FILE /tmp/${$(echo $FILE | sed s/svgz/svg.gz/)##*/} && \
    gunzip /tmp/${$(echo $FILE | sed s/svgz/svg.gz/)##*/} && \
    cp /tmp/${$(echo $FILE | sed s/svgz/svg/)##*/} ./;
  done
}

autoload zkbd
if [  "`ls ~/.zkbd/$TERM-${DISPLAY:-$VENDOR-$OSTYPE}`" != "" ];then
else
  zkbd
fi
source ~/.zkbd/$TERM-${DISPLAY:-$VENDOR-$OSTYPE}

#    [[ -n ${key[Left]} ]] && bindkey "${key[Left]}" backward-char
#    [[ -n ${key[Right]} ]] && bindkey "${key[Right]}" forward-char

[[ -n ${key[Backspace]} ]] && bindkey "${key[Backspace]}" backward-delete-char
[[ -n ${key[Insert]} ]] && bindkey "${key[Insert]}" overwrite-mode
[[ -n ${key[Home]} ]] && bindkey "${key[Home]}" beginning-of-line
[[ -n ${key[PageUp]} ]] && bindkey "${key[PageUp]}" history-search-backward #up-line-or-history
[[ -n ${key[Delete]} ]] && bindkey "${key[Delete]}" delete-char
[[ -n ${key[End]} ]] && bindkey "${key[End]}" end-of-line
[[ -n ${key[PageDown]} ]] && bindkey "${key[PageDown]}" history-search-forward #down-line-or-history
[[ -n ${key[Up]} ]] && bindkey "${key[Up]}" up-line-or-history #up-line-or-search
[[ -n ${key[Left]} ]] && bindkey "${key[Left]}" backward-char
[[ -n ${key[Down]} ]] && bindkey "${key[Down]}" down-line-or-history #down-line-or-search
[[ -n ${key[Right]} ]] && bindkey "${key[Right]}" forward-char

#bindkey "^[[5C" forward-word
#bindkey "^[[5D" backward-word
#bindkey "e[5C" forward-word
#bindkey "e[5C" backward-word
bindkey "\eOd" backward-word
bindkey "\eOc" forward-word 


zstyle ':completion:*' completer _expand _complete _ignored _correct _approximate
zstyle ':completion:*' group-name ''
zstyle ':completion:*' list-colors ''
zstyle ':completion:*' menu select=1
zstyle ':completion:*' select-prompt %SScrolling active: current selection at %p%s
zstyle :compinstall filename '/home/lepagee/.zshrc'

autoload -Uz compinit
compinit
# End of lines added by compinstall

USERNAME=`whoami`

if [[ $USERNAME == "lepagee" ]]; then
  USERCOLOR=$PR_CYAN
  BASEC=15
  BASEMUL=6
elif [[ $USERNAME == "kde-devel" ]]; then
  USERCOLOR=$PR_GREEN
  BASEC=22
  BASEMUL=6
elif [[ $USERNAME == "root" ]]; then
  USERCOLOR=$PR_RED
  BASEC=16
  BASEMUL=36
else
  USERCOLOR=$PR_YELLOW
fi

function breadpath {;awk -F'/' -v "baseC=$BASEC" -v "baseMul=$BASEMUL" '{printf "\033[48;5;%sm\033[38;5;232m\033[1m /",baseC+baseMul;for (i=1;i<=NF;i++) {printf "\033[48;5;%sm\033[38;5;232m\033[1m %s \033[%sm\033[38;5;%sm⮀",baseC+(i*baseMul),$i,(i<NF)?"48;5;"(baseC+((i+1)*baseMul)):0,baseC+(i*baseMul)};print "\n"}' <(pwd);}

function precmd {

    local TERMWIDTH
    (( TERMWIDTH = ${COLUMNS} - 1 ))


    ###
    # Truncate the path if it's too long.
    
    PR_FILLBAR=""
    PR_PWDLEN=""
    
    local promptsize=${#${(%):---(%n@%m)---()--}}
    brPwd=$(breadpath)
    local pwdsize=$(echo $(pwd) | awk -F"/" '{print (2*NF)+length($0)}')
    if [[ "$promptsize + $pwdsize" -gt $TERMWIDTH ]]; then
	    ((PR_PWDLEN=$TERMWIDTH - $promptsize))
    else
		PR_FILLBAR="\${(l.(($TERMWIDTH - ($promptsize + $pwdsize)-3))..${PR_HBAR}.)}"
    fi


    ###
    # Get APM info.

    if which ibam > /dev/null; then
	PR_APM_RESULT=`ibam --percentbattery`
    elif which apm > /dev/null; then
	PR_APM_RESULT=`apm`
    fi
}


setopt extended_glob
preexec () {
   echo -n '\033];'$2'\007'
   if [[ "$TERM" == "screen" ]]; then
	   local CMD=${1[(wr)^(*=*|sudo|-*)]}
	   echo -n "\ek$CMD\e\\"
   fi
}

function notifyOver {
   TERMS="$(pgrep urxvt)"
   TMP_PID=$PPID
   while [ "$TMP_PID" != "1" ]; do
      if [ "$(echo $TERMS | grep $TMP_PID)" != "" ]; then
#         echo "naughty.notify_hidden($TMP_PID,'zsh','Command $(printf '%q' $(history -1)) over')" | sudo -u lepagee awesome-client
         break;
      fi
      TMP_PID=`/bin/ps -eo pid,ppid | grep -E "$TMP_PID [ 0-9]" | awk '{print $2}'`
   done
}

postexec () {
   echo '\033]; '$USER: $PWD'\007'
   notifyOver
}

    autoload colors zsh/terminfo
    if [[ "$terminfo[colors]" -ge 8 ]]; then
      colors
    fi


    for color in RED GREEN YELLOW BLUE MAGENTA CYAN WHITE; do
      eval PR_$color='%{$terminfo[bold]$fg[${(L)color}]%}'
      eval PR_${color}BG='%{$terminfo[bold]$bg[${(L)color}]%}'
      eval PR_LIGHT_$color='%{$fg[${(L)color}]%}'
      (( count = $count + 1 ))
    done
    PR_NO_COLOUR="%{$terminfo[sgr0]%}"
PR_GRAYBG=">"#'%{$terminfo[bold]$bg[${(L)RED}]%}'

setprompt () {
    ###
    # Need this so the prompt will work.

    setopt prompt_subst


    ###
    # See if we can use colors.
#    autoload colors zsh/terminfo
#    if [[ "$terminfo[colors]" -ge 8 ]]; then
#		colors
#    fi
#

#    for color in RED GREEN YELLOW BLUE MAGENTA CYAN WHITE; do
#      eval PR_$color='%{$terminfo[bold]$fg[${(L)color}]%}'
#      eval PR_LIGHT_$color='%{$fg[${(L)color}]%}'
#      (( count = $count + 1 ))
#    done
#    PR_NO_COLOUR="%{$terminfo[sgr0]%}"



    ###
    # See if we can use extended characters to look nicer.
    
    typeset -A altchar
    set -A altchar ${(s..)terminfo[acsc]}
    PR_SET_CHARSET="%{$terminfo[enacs]%}"
    PR_SHIFT_IN="%{$terminfo[smacs]%}"
    PR_SHIFT_OUT="%{$terminfo[rmacs]%}"
    PR_HBAR=${altchar[q]:--}
#    PR_ULCORNER=${altchar[l]:--}
#    PR_LLCORNER=${altchar[m]:--}
#    PR_LRCORNER=${altchar[j]:--}
#    PR_URCORNER=${altchar[k]:--}
#╭
#╰ 
    
    ###
    # Decide if we need to set titlebar text.
    
    case $TERM in
	xterm*)
	    PR_TITLEBAR=$'%{\e]0;%(!.-=*[ROOT]*=- | .)%n@%m:%~ | ${COLUMNS}x${LINES} | %y\a%}'
	    ;;
	screen)
	    PR_TITLEBAR=$'%{\e_screen \005 (\005t) | %(!.-=[ROOT]=- | .)%n@%m:%~ | ${COLUMNS}x${LINES} | %y\e\\%}'
	    ;;
	*)
	    PR_TITLEBAR=''
	    ;;
    esac
    
    
    ###
    # Decide whether to set a screen title
    if [[ "$TERM" == "screen" ]]; then
	PR_STITLE=$'%{\ekzsh\e\\%}'
    else
	PR_STITLE=''
    fi
    
    
    ###
    # APM detection
    
    if which ibam > /dev/null; then
	PR_APM='$PR_RED${${PR_APM_RESULT[(f)1]}[(w)-2]}%%(${${PR_APM_RESULT[(f)3]}[(w)-1]})$PR_LIGHT_BLUE:'
    elif which apm > /dev/null; then
	PR_APM='$PR_RED${PR_APM_RESULT[(w)5,(w)6]/\% /%%}$PR_LIGHT_BLUE:'
    else
	PR_APM=''
    fi
    
    ###
    # Finally, the prompt.

BG_HIGH=$(echo -e "\e[48;5;27m")
FG_ARROW=$(echo -e "\e[38;5;27m")
PROMPT='$(postexec &)$PR_SET_CHARSET$PR_STITLE${(e)PR_TITLEBAR}\
$PR_SHIFT_IN$PR_SHIFT_OUT\
┏━$brPwd$PR_SHIFT_IN$PR_HBAR$PR_HBAR${(e)PR_FILLBAR}$PR_HBAR$PR_SHIFT_OUT$FG_ARROW⮂$BG_HIGH \
$USERCOLOR%(!.${PR_RED}%n.%n)@%m \
$PR_SHIFT_IN$PR_NO_COLOUR$FG_ARROW⮀$PR_NO_COLOUR━┓$PR_SHIFT_OUT \

$PR_SHIFT_IN┗━$PR_SHIFT_OUT:\
$PR_NO_COLOUR '

    RPROMPT=' $PR_SHIFT_IN$PR_BLUE⮂$PR_NO_COLOUR$PR_BLUEBG $PR_SHIFT_OUT\
%D{%a %H:%M} $PR_NO_COLOUR$PR_BLUE⮀$PR_SHIFT_IN$PR_NO_COLOUR━┛$PR_SHIFT_OUT$PR_NO_COLOUR'

    PS2='$PR_CYAN$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT\
$PR_BLUE$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT(\
$PR_LIGHT_GREEN%_$PR_BLUE)$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT\
$PR_CYAN$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT$PR_NO_COLOUR '
}

setprompt

#$PR_LIGHT_BLUE:%(!.$PR_RED.$PR_WHITE)%#$PR_BLUE)$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT\
#%(?..$PR_LIGHT_RED%?$PR_BLUE:)\
#${(e)PR_APM}\

