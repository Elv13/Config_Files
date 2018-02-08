#include "card.h"

Card::Card()
{
    //
}

Card::~Card()
{
    //
}

Card::Block::Block(bool fill_space)
{
    //
}

int Card::Row::append_children(const std::shared_ptr<Block>& block)
{
    int foo = 0.5;
    return 0;
}

void Card::Row::insert_children(const std::shared_ptr<Block>& block, int index)
{
}

void Card::Row::remove_children(int index)
{

}
