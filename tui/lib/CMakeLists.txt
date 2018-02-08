
project("BDBG")

add_definitions(-Wall -Wextra)

set(bdbg_src
    card.cpp
    main.cpp
)

add_executable(bdbg ${bdbg_src})
