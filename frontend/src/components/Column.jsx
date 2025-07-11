import { useDroppable } from "@dnd-kit/core";
import { SortableContext, verticalListSortingStrategy } from "@dnd-kit/sortable";
import SortableLeadCard from "./SortableLeadCard";

import PropTypes from 'prop-types';

function Column({ title, cards }) {
  const { setNodeRef } = useDroppable({ id: title });

  return (
    <div ref={setNodeRef} className="bg-gray-800 rounded-xl p-2">
      <h2 className="text-center mb-2">{title}</h2>
      <SortableContext items={cards.map(c => c.id)} strategy={verticalListSortingStrategy}>
        {cards.map(c => <SortableLeadCard key={c.id} lead={c} />)}
      </SortableContext>
    </div>
  );
}

Column.propTypes = {
  title: PropTypes.string.isRequired,
  cards: PropTypes.array.isRequired,
};

export default Column;
