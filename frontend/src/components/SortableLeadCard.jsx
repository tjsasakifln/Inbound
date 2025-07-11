import { useSortable } from "@dnd-kit/sortable";
import { CSS } from "@dnd-kit/utilities";
import LeadCard from "./LeadCard";

import PropTypes from 'prop-types';

export default function SortableLeadCard({ lead }) {
  const { attributes, listeners, setNodeRef, transform, transition } = useSortable({ id: lead.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <div ref={setNodeRef} style={style} {...attributes} {...listeners}>
      <LeadCard lead={lead} />
    </div>
  );
}

SortableLeadCard.propTypes = {
  lead: PropTypes.shape({
    id: PropTypes.string.isRequired,
  }).isRequired,
};
