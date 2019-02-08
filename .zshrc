clear
source /etc/issue
# The following lines were added by compinstall

PATH=/sbin:/usr/sbin:/usr/local/bin:/usr/bin:/bin:$HOME/config_files/scripts/:$HOME/prefix/bin/
XDG_DATA_DIRS=$XDG_DATA_DIRS:/home/kde-devel/kde/share/akonadi/agents:$HOME/prefix/share
QT_STYLE_OVERRIDE="breeze"
export QML2_IMPORT_PATH=/home/lepagee/prefix/lib64/qml/:/usr/lib64/qt5/qml
export QT_STYLE_OVERRIDE="breeze"
export QT_PLUGIN_PATH=$HOME/prefix/lib64/plugins
export QT_SELECT=5
EDITOR=vim
export XDG_CURRENT_DESKTOP=KDE

export XAUTHORITY=$HOME/.Xauthority

export HISTSIZE=2000
export HISTFILE="$HOME/.zhistory"
export SAVEHIST=$HISTSIZE
#export PAGER="most"

setopt histignoredups
setopt histignorespace
setopt hist_ignore_all_dups
setopt autocd
#setopt correctall
setopt no_case_glob
setopt noequals

# Do not close on CTRL+D
setopt IGNORE_EOF
stty stop undef
stty start undef
bindkey '^D' backward-char
bindkey -e
bindkey "^[[1;5C" forward-word
bindkey "^[[1;5D" backward-word

alias gdb='gdb -q'
alias ls='ls --color=auto -F'
alias ll='ls++'
alias la='ls -lah --color=y -F | table'
alias tarc="tar -cjvf "
alias tarx="tax -xpvf "
#alias nano="nano -w"
alias nano=nvim
alias nn="nano -w "
alias n="nano -w "
alias grepkey="xev | grep -A2 --line-buffered '^KeyRelease' | sed -n '/keycode /s/^.*keycode \([0-9]*\).* (.*, \(.*\)).*$/\1 \2/p'"
alias xrags=xargs
alias greo=grep
alias xephyr="Xephyr :1 -screen 1680x996"
alias kdb="sudo killall -9 updatedb"
alias xdg-edit="nano ~/.local/share/applications/mimeapps.list"
alias bell="echo '\a'"
alias lmod="find /lib/modules/`uname -r` -iname '*.ko'"
alias eacapeurl="sed -e's/%\([0-9A-F][0-9A-F]\)/\\\\\x\1/g'"
alias urldecode='python2 -c "import sys, urllib as ul; print ul.unquote_plus(sys.argv[1])"'
alias wttr='curl wttr.in/Montreal,Canada'
alias table="column  -o' │ ' -t"
alias ntable="table | nl"

#./archive/compton/compton -r 9 -l -13 -t -13 -c -C --shadow-blue 1 --shadow-red 0.2 --shadow-green 0.6 -o 0.325 --detect-rounded-corners

function backlight() { sudo su -c "echo $1 > /sys/class/backlight/intel_backlight/brightness"}

function setacpi() { sudo su -c "/home/lepagee/prefix/bin/acpi.sh $1 $2"} 

function fawe {; find ~/.config/awesome/ -iname '*.lua' | xargs grep $1 --color;}

function dnsrestart() {sudo ifconfig eth0 10.10.10.116 && ssh root@10.10.10.1 /etc/init.d/dnsmasq restart}

function killawesome() {/bin/ps aux | grep awesome | grep -v tty | grep -v grep | grep -vE "(vi|vim|nano|kate|emacs)" | awk '{print $2}' | xargs -i kill -9 "{}"}
function fixawperm() {find /usr/share/awesome/ -iname '*.lua' | xargs sudo chmod 777}

function coderename() { git ls-files .. | grep -E '\.(cpp|h)' | xargs sed -i 's/'$1'/'$2'/'}

function getalsa() {echo $( \
	lsof +D /dev -F rt \
	| awk '/^p/ {pid=$1} /^t/ {type=$1} /^r0x(74|e)..$/ && type == "tCHR" {print pid}' \
	| cut -c 2- \
	| uniq \
)}

#Make ctrl+left/right and ^W work as in any other apps in the universe
zle -N backward-kill-word-bash backward-kill-word-match
zstyle ':zle:backward-kill-word-bash' word-style whitespace
zstyle ':completion:*' matcher-list '' 'm:{a-z}={A-Z}'
bindkey '^Q' quoted-insert '^U' vi-kill-line '^W' backward-kill-word-bash
autoload -U select-word-style
select-word-style bash
autoload -Uz url-quote-magic; zle -N self-insert url-quote-magic

bindkey '^P' push-input

source ~/.zshrc.d/external/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
source ~/.zshrc.d/external/history-search-multi-word/history-search-multi-word.plugin.zsh
eval $( dircolors -b $HOME/.LS_COLORS )
ZLS_COLORS="$LS_COLORS"

function svgz2svg {
  for FILE in "$1";do 
    cp $FILE /tmp/${$(echo $FILE | sed s/svgz/svg.gz/)##*/} && \
    gunzip /tmp/${$(echo $FILE | sed s/svgz/svg.gz/)##*/} && \
    cp /tmp/${$(echo $FILE | sed s/svgz/svg/)##*/} ./;
  done
}

function git_status() {
    #Return 0 if the folder is not versionned, branch name otherwise
    GIT_BRANCH=$(git rev-parse  --abbrev-ref HEAD 2> /dev/null)

    if [ $? -eq 0 ]; then
        dfs=$(git diff --shortstat | sed "s/ file changed/⭡/;s/ insertion//;s/ deletion//;s/ files changed/⭡/")
        DIFF_STAT=$(echo $dfs | sed "s/(+)/$PR_GREEN%B+$PR_WHITE%B/;s/(-)/$PR_RED%B-/;s/,//;s/,//")
        dfs=$(echo $dfs | sed "s/(+)/+/;s/(-)/-/;s/,//;s/,//") #Do the same thing without colors
        echo -e "⭠ $GIT_BRANCH$DIFF_STAT"
        return $(( ${#dfs} + 23 )) #String length
    else
        HOSTN=$(whoami)@$(hostname)
        echo $HOSTN
        return $(( ${#HOSTN} + 11 )) #String length
    fi
}

autoload zkbd
if [  "`ls ~/.zkbd/$TERM-${DISPLAY:-$VENDOR-$OSTYPE}`" != "" ];then
  source ~/.zkbd/$TERM-${DISPLAY:-$VENDOR-$OSTYPE}
else
  zkbd
fi

#    [[ -n ${key[Left]} ]] && bindkey "${key[Left]}" backward-char
#    [[ -n ${key[Right]} ]] && bindkey "${key[Right]}" forward-char

[[ -n ${key[Backspace]} ]]  && bindkey "${key[Backspace]}" backward-delete-char
[[ -n ${key[Insert]} ]]     && bindkey "${key[Insert]}"    overwrite-mode
[[ -n ${key[Home]} ]]       && bindkey "${key[Home]}"      beginning-of-line
[[ -n ${key[PageUp]} ]]     && bindkey "${key[PageUp]}"    history-search-backward #up-line-or-history
[[ -n ${key[Delete]} ]]     && bindkey "${key[Delete]}"    delete-char
[[ -n ${key[End]} ]]        && bindkey "${key[End]}"       end-of-line
[[ -n ${key[PageDown]} ]]   && bindkey "${key[PageDown]}"  history-search-forward #down-line-or-history
[[ -n ${key[Up]} ]]         && bindkey "${key[Up]}"        up-line-or-history #up-line-or-search
[[ -n ${key[Left]} ]]       && bindkey "${key[Left]}"      backward-char
[[ -n ${key[Down]} ]]       && bindkey "${key[Down]}"      down-line-or-history #down-line-or-search
[[ -n ${key[Right]} ]]      && bindkey "${key[Right]}"     forward-char

zstyle ':completion:*' completer _expand _complete _ignored _correct _approximate
zstyle ':completion:*' group-name ''
zstyle ':completion:*' list-colors ''
zstyle ':completion:*' menu select=1
zstyle ':completion:*' select-prompt %SScrolling active: current selection at %p%s
zstyle ":history-search-multi-word" page-size "5"
zstyle :compinstall filename '/home/lepagee/.zshrc'

autoload -Uz compinit
compinit
# End of lines added by compinstall

USERNAME=`whoami`

#Source all files in ~/.zshrc.d/groups/$USERNAME
if [ -d ~/.zshrc.d/groups/$USERNAME ]; then
    for files in $(ls ~/.zshrc.d/groups/$USERNAME); do
        source ~/.zshrc.d/groups/$USERNAME/$files
    done
fi

if [ -e ~/.zshrc.d/usercolor/$USERNAME ]; then
  source ~/.zshrc.d/usercolor/$USERNAME
else
  USERCOLOR=$PR_YELLOW
fi

function breadpath {;awk -F'/' -v "baseC=$BASEC" -v "baseMul=$BASEMUL" '{
    printf "\033[48;5;%sm\033[38;5;232m\033[1m /",baseC+baseMul;
    for (i=1;i<=NF;i++) {
        printf "\033[48;5;%sm\033[38;5;232m\033[1m %s \033[%sm\033[38;5;%sm⮀",baseC+(i*baseMul),$i,(i<NF)?"48;5;"(baseC+((i+1)*baseMul)):0,baseC+(i*baseMul)
    };
    print "\n"}' <(pwd);}

function precmd {

    local TERMWIDTH
    (( TERMWIDTH = ${COLUMNS} - 1 ))


    ###
    # Truncate the path if it's too long.
    
    PR_FILLBAR=""
    PR_PWDLEN=""
    git_status 2> /dev/null > /dev/null
    local promptsize=$(( $? ))
    brPwd=$(breadpath)
    local pwdsize=$(echo $(pwd) | awk -F"/" '{print (2*NF)+length($0)}')
    if [[ "$promptsize + $pwdsize" -gt $TERMWIDTH ]]; then
	    ((PR_PWDLEN=$TERMWIDTH - $promptsize))
    else
		PR_FILLBAR="\${(l.(($TERMWIDTH - ($promptsize + $pwdsize)-3))..${PR_HBAR}.)}"
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

    setopt prompt_subst

    ###
    # See if we can use extended characters to look nicer.
    
    typeset -A altchar
    set -A altchar ${(s..)terminfo[acsc]}
    PR_SET_CHARSET="%{$terminfo[enacs]%}"
    PR_SHIFT_IN="%{$terminfo[smacs]%}"
    PR_SHIFT_OUT="%{$terminfo[rmacs]%}"
    PR_HBAR=${altchar[q]:--}
    
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

if [ "$TERM" != "linux" ]; then

BG_HIGH=$(echo -e "\e[48;5;$(($BASEC + $BASEMUL + $BASEMUL ))m\e[38;5;231m\033[1m")
FG_ARROW=$(echo -e "\e[38;5;$(($BASEC + $BASEMUL + $BASEMUL ))m")
PROMPT='$(postexec &)$PR_SET_CHARSET$PR_STITLE${(e)PR_TITLEBAR}\
$PR_SHIFT_IN$PR_SHIFT_OUT\
┏━$brPwd$FG_ARROW$PR_SHIFT_IN$PR_HBAR$PR_HBAR${(e)PR_FILLBAR}$PR_HBAR$PR_SHIFT_OUT$FG_ARROW⮂$BG_HIGH \
$USERCOLOR$(git_status) \
$PR_SHIFT_IN$PR_NO_COLOUR$FG_ARROW⮀$PR_NO_COLOUR━┓$PR_SHIFT_OUT \

$PR_SHIFT_IN┗━$PR_SHIFT_OUT:\
$PR_NO_COLOUR '

RPROMPT=' $PR_SHIFT_IN$PR_LIGHT_BLUE⮂$PR_NO_COLOUR$PR_BLUEBG$PR_YELLOW$PR_SHIFT_OUT\
%D{%a %H:%M} $PR_NO_COLOUR$PR_BLUE⮀$PR_SHIFT_IN$PR_NO_COLOUR━┛$PR_SHIFT_OUT$PR_NO_COLOUR'

PS2='$PR_CYAN$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT\
$PR_BLUE$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT(\
$PR_LIGHT_GREEN%_$PR_BLUE)$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT\
$PR_CYAN$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT$PR_NO_COLOUR '

else

PS1='>'

fi

}

setprompt

