
#include <memory>
#include <vector>

class Card
{
public:
    enum class BlockType {
        BLOCK,
        ROW,
        COLUMN,
    };

    class Block {
        public:
            explicit Block(bool fill_space);

        private:
            bool _fill_space {false};

        protected:
            BlockType _type {BlockType::BLOCK};
            std::vector<Block> _children {};
    };

    class Row : public Block {
        public:
            int append_children(const std::shared_ptr<Block>& block);
            void insert_children(const std::shared_ptr<Block>& block, int index);
            void remove_children(int index);

    };

    class Column : public Row {

    };

    class Label : public Block {

    };

    explicit Card();
    virtual ~Card();

private:
    std::shared_ptr<Block> _root_block {nullptr};
};
