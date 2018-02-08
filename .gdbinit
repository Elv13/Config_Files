set history remove-duplicates 1

set history save on

set pagination off

set extended-prompt \e[100m\n\e[49m\n\e[31m==>\e[39m

set print pretty on

define hook-quit
    set confirm off
end

define hook-run
    set confirm off
end

define mc
    shell mc
end

define tig
   shell tig
end

define ninja
   shell ninja
end

# Don't return on PIPE events
handle SIGPIPE nostop noprint pass

# Add the scripts dir to the PATH to fix the git commands
python
import os
os.environ['PATH'] = os.environ['PATH'] + ':' + os.environ['HOME'] + '/scripts'
end

# Add the `git` command to the GDB shell
define git
    if $argc == 1
        shell git $arg0
    end
    if $argc == 2
        shell git $arg0 $arg1
    end
    if $argc == 3
        shell git $arg0 $arg1 $arg2
    end
    if $argc == 4
        shell git $arg0 $arg1 $arg2 $arg3
    end
    if $argc == 5
        shell git $arg0 $arg1 $arg2 $arg3 $arg4
    end
    if $argc == 6
        shell git $arg0 $arg1 $arg2 $arg3 $arg4	$arg5
    end
    if $argc == 7
        shell git $arg0 $arg1 $arg2 $arg3 $arg4	$arg5 $arg6
    end
    if $argc == 8
        shell git $arg0 $arg1 $arg2 $arg3 $arg4	$arg5 $arg6 $arg7
    end
    if $argc == 9
        shell git $arg0 $arg1 $arg2 $arg3 $arg4 $arg5 $arg6 $arg7 $arg8
    end
end

define ds
    shell git ds
end

define status
    shell git status
end

define diff
    shell git diff
end

# Oh my GDB!!!!11
python
sys.path.insert(0, '/home/lepagee/config_files/tui')
end

source /home/lepagee/config_files/trace.py
source /home/lepagee/config_files/stackoverflow.py
source /home/lepagee/config_files/box.py
source /home/lepagee/config_files/print.py
source /home/lepagee/config_files/assert.py
source /home/lepagee/config_files/make.py
source /home/lepagee/config_files/printers/time.py

python
sys.path.insert(0, '/home/lepagee/config_files/printers')


from qt import register_qt_printers
from kde import register_kde_printers

register_qt_printers (None)
register_kde_printers (None)
end
