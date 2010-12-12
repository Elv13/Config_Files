# The following lines were added by compinstall

PATH=/usr/local/bin:/usr/bin:/bin:/opt/bin:/usr/x86_64-pc-linux-gnu/gcc-bin/4.4.4:/opt/blackdown-jdk-1.4.2.03/bin:/opt/blackdown-jdk-1.4.2.03/jre/bin:/usr/games/bin:/home/kde-devel/kde/bin

export HISTSIZE=2000
export HISTFILE="$HOME/.zhistory"
export SAVEHIST=$HISTSIZE



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

function precmd {

    local TERMWIDTH
    (( TERMWIDTH = ${COLUMNS} - 1 ))


    ###
    # Truncate the path if it's too long.
    
    PR_FILLBAR=""
    PR_PWDLEN=""
    
    local promptsize=${#${(%):---(%n@%m)---()--}}
    local pwdsize=${#${(%):-%~}}
    
    if [[ "$promptsize + $pwdsize" -gt $TERMWIDTH ]]; then
	    ((PR_PWDLEN=$TERMWIDTH - $promptsize))
    else
	PR_FILLBAR="\${(l.(($TERMWIDTH - ($promptsize + $pwdsize)))..${PR_HBAR}.)}"
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
    if [[ "$TERM" == "screen" ]]; then
	local CMD=${1[(wr)^(*=*|sudo|-*)]}
	echo -n "\ek$CMD\e\\"
    fi
}


setprompt () {
    ###
    # Need this so the prompt will work.

    setopt prompt_subst


    ###
    # See if we can use colors.

    autoload colors zsh/terminfo
    if [[ "$terminfo[colors]" -ge 8 ]]; then
	colors
    fi
    for color in RED GREEN YELLOW BLUE MAGENTA CYAN WHITE; do
      eval PR_$color='%{$terminfo[bold]$fg[${(L)color}]%}'
      eval PR_LIGHT_$color='%{$fg[${(L)color}]%}'
      (( count = $count + 1 ))
    done
    PR_NO_COLOUR="%{$terminfo[sgr0]%}"


    ###
    # See if we can use extended characters to look nicer.
    
    typeset -A altchar
    set -A altchar ${(s..)terminfo[acsc]}
    PR_SET_CHARSET="%{$terminfo[enacs]%}"
    PR_SHIFT_IN="%{$terminfo[smacs]%}"
    PR_SHIFT_OUT="%{$terminfo[rmacs]%}"
    PR_HBAR=${altchar[q]:--}
    PR_ULCORNER=${altchar[l]:--}
    PR_LLCORNER=${altchar[m]:--}
    PR_LRCORNER=${altchar[j]:--}
    PR_URCORNER=${altchar[k]:--}

    
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
    
USERNAME=`whoami`

if [[ $USERNAME == "lepagee" ]]; then
  USERCOLOR=$PR_CYAN
elif [[ $USERNAME == "kde-devel" ]]; then
  USERCOLOR=$PR_GREEN
elif [[ $USERNAME == "root" ]]; then
  USERCOLOR=$PR_RED
else
  USERCOLOR=$PR_YELLOW
fi
    ###
    # Finally, the prompt.

    PROMPT='$PR_SET_CHARSET$PR_STITLE${(e)PR_TITLEBAR}\
$PR_CYAN$PR_SHIFT_IN$PR_ULCORNER$PR_BLUE$PR_HBAR$PR_SHIFT_OUT(\
$USERCOLOR%(!.${PR_RED}%n.%n)$PR_BLUE@%m\
$PR_BLUE)$PR_SHIFT_IN$PR_HBAR$PR_CYAN$PR_HBAR${(e)PR_FILLBAR}$PR_BLUE$PR_HBAR$PR_SHIFT_OUT(\
$PR_LIGHT_GREEN%$PR_PWDLEN<...<%~%<<\
$PR_BLUE)$PR_SHIFT_IN$PR_HBAR$PR_CYAN$PR_URCORNER$PR_SHIFT_OUT \

$PR_CYAN$PR_SHIFT_IN$PR_LLCORNER$PR_BLUE$PR_HBAR$PR_SHIFT_OUT$PR_CYAN:\
$PR_NO_COLOUR '

    RPROMPT=' $PR_CYAN$PR_SHIFT_IN$PR_HBAR$PR_BLUE$PR_HBAR$PR_SHIFT_OUT\
($PR_GREEN%D{%a %H:%M}$PR_BLUE)$PR_SHIFT_IN$PR_HBAR$PR_CYAN$PR_LRCORNER$PR_SHIFT_OUT$PR_NO_COLOUR'

    PS2='$PR_CYAN$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT\
$PR_BLUE$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT(\
$PR_LIGHT_GREEN%_$PR_BLUE)$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT\
$PR_CYAN$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT$PR_NO_COLOUR '
}

setprompt

#$PR_LIGHT_BLUE:%(!.$PR_RED.$PR_WHITE)%#$PR_BLUE)$PR_SHIFT_IN$PR_HBAR$PR_SHIFT_OUT\
#%(?..$PR_LIGHT_RED%?$PR_BLUE:)\
#${(e)PR_APM}\

#KDE stuff
export KDEDIR=$HOME/kde
export KDEHOME=$HOME/.kde4
export KDETMP=/tmp/$USER-kde4
mkdir -p $KDETMP
export KDEDIRS=$KDEDIR
export PREFIX="/home/kde-devel/kde/"
export PKG_CONFIG_PATH=$KDEDIR/lib/pkgconfig:$PKG_CONFIG_PATH
export  CXXFLAGS="-Wpointer-arith -Wcast-align -Wsign-compare -Woverloaded-virtual -Wswitch -Wno-unused-parameter -g -O3 -fopenmp -g -O3 -pipe -msse3 -msse2 -msse -mmmx -march=core2"
export CFLAGS=" -g -O3 -pipe -msse3 -msse2 -msse -mmmx -march=core2" 
alias nano="nano -w"

# XDG
unset XDG_DATA_DIRS # to avoid seeing kde3 files from /usr
unset XDG_CONFIG_DIRS

# you might want to change these:
export KDE_BUILD=$HOME/kde/build
export KDE_SRC=$HOME/kde/src

# make the debug output prettier
export KDE_COLOR_DEBUG=1
export QTEST_COLORED=1

function cs {
   # Make sure source directory exists.
   mkdir -p "$KDE_SRC"
 
   # command line argument
   if test -n "$1"; then
      cd "$KDE_SRC/$1"
   else
      # substitute build dir with src dir
      dest=`pwd | sed -e s,$KDE_BUILD,$KDE_SRC,`
      current=`pwd`
      if [ "$dest" = "$current" ]; then
         cd "$KDE_SRC"
      else
         cd "$dest"
      fi
   fi
}

function cb {
   # Make sure build directory exists.
   mkdir -p "$KDE_BUILD"

   # command line argument
   if test -n "$1"; then
      cd "$KDE_BUILD/$1"
      return
   fi
   # substitute src dir with build dir
   dest=`pwd | sed -e s,$KDE_SRC,$KDE_BUILD,`
   if test ! -d "$dest"; then
      # build directory does not exist, create
      mkdir -p "$dest"
   fi
   cd "$dest"
}

function cmakekde {
   if test -n "$1"; then
      # srcFolder is defined via command line argument
      srcFolder="$1"
   else
      # get srcFolder for current dir
      srcFolder=`pwd | sed -e s,$KDE_BUILD,$KDE_SRC,`
   fi
   # we are in the src folder, change to build directory
   # Alternatively, we could just use makeobj in the commands below...
   current=`pwd`
   if [ "$srcFolder" = "$current" ]; then
      cb
   fi
   # to enable tests, add -DKDE4_BUILD_TESTS=TRUE to the next line.
   # you can also change "debugfull" to "debug" to save disk space.
   cmake "$srcFolder" -GKDevelop3 -DCMAKE_INSTALL_PREFIX=$KDEDIR \
      -DCMAKE_BUILD_TYPE=debugfull

        # uncomment the following two lines to make builds wait after
        # configuration step, so that the user can check configure output
        #echo "Press <ENTER> to continue..."
        #read userinput
 
        # Note: To speed up compiling, change 'make -j2' to 'make -jx',
        #   where x is your number of processors +1
        nice make -j5 && \
        make install;
}
