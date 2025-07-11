import PropTypes from 'prop-types';

function LeadCard({ lead }) {
  return (
    <div className="bg-gray-700 rounded-lg p-2 mb-2">
      <p className="text-sm font-semibold">{lead.sender}</p>
      <p className="text-xs">{lead.subject}</p>
      <p className="text-right text-xs opacity-70">{(lead.score*100).toFixed(0)}%</p>
    </div>
  );
}

LeadCard.propTypes = {
  lead: PropTypes.shape({
    sender: PropTypes.string.isRequired,
    subject: PropTypes.string.isRequired,
    score: PropTypes.number.isRequired,
  }).isRequired,
};

export default LeadCard;
